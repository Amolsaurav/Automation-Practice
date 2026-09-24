import asyncio
import os
import re
import requests

from google import genai
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_env_file():
    env_path = os.path.join(PROJECT_DIR, ".env")
    if not os.path.exists(env_path):
        return

    try:
        with open(env_path, "r", encoding="utf-8") as env_file:
            for line in env_file:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key == "GEMINI_API_KEY":
                    os.environ[key] = value
                else:
                    os.environ.setdefault(key, value)
    except OSError as exc:
        raise RuntimeError(f"Could not read .env file: {exc}") from exc


load_env_file()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set. Add it to the terminal environment or playwright-gemini/.env."
    )


def read_spec_bundle():
    base_files = ["spec.md", "ui_test_requirements.md", "api_test_requirements.md"]
    parts = []

    for file_name in base_files:
        file_path = os.path.join(PROJECT_DIR, file_name)
        if not os.path.exists(file_path):
            continue
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content:
            continue
        parts.append(f"===== FILE: {file_name} =====\n{content}")

    return "\n\n".join(parts)


spec_text = read_spec_bundle()
gemini = genai.Client(api_key=api_key)

server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@playwright/mcp@latest", "--headless"],
)


call_api_declaration = {
    "name": "call_api",
    "description": "Call a backend API endpoint to inspect its real response shape.",
    "parameters": {
        "type": "object",
        "properties": {
            "method": {"type": "string"},
            "url": {"type": "string"},
            "body": {"type": "object"},
        },
        "required": ["method", "url"],
    },
}


def call_api(method, url, body=None):
    resp = requests.request(method, url, json=body, timeout=10)
    return {"status": resp.status_code, "body": resp.text[:2000]}


def save_multi_file_output(text, output_dir="."):
    protected_paths = {
        os.path.normcase(os.path.normpath("generated/conftest.py")),
        os.path.normcase(os.path.normpath("generated/__init__.py")),
    }
    blocks = re.split(r"### FILE:\s*(.+)", text)
    for i in range(1, len(blocks), 2):
        path = blocks[i].strip()
        relative_path = os.path.normcase(os.path.normpath(path))
        code = blocks[i + 1]
        code = re.sub(r"^```[a-z]*\n|```$", "", code.strip(), flags=re.MULTILINE)
        full_path = os.path.join(output_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        if relative_path in protected_paths and os.path.exists(full_path):
            print("Preserved", full_path)
            continue
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(code.strip() + "\n")
        print("Wrote", full_path)


def ensure_generated_package_markers(output_dir):
    for relative_path in (
        "generated/__init__.py",
        "generated/pages/__init__.py",
        "generated/tests/__init__.py",
        "generated/tests/ui/__init__.py",
        "generated/tests/api/__init__.py",
    ):
        file_path = os.path.join(output_dir, relative_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as marker_file:
                marker_file.write("")


async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            response = await gemini.aio.models.generate_content(
                model="gemini-3.6-flash",
                contents=(
                    f"{spec_text}\n\n"
                    "Use the browser tools to inspect UI flows from ui_test_requirements.md and "
                    "API flows from api_test_requirements.md. "
                    "The project must keep UI logic and API logic separated under generated/tests/ui and "
                    "generated/tests/api. Keep the same generation workflow and follow the exact Output format."
                ),
            )

    save_multi_file_output(response.text, output_dir=PROJECT_DIR)
    ensure_generated_package_markers(PROJECT_DIR)
    print("Review the files under ./generated before running them.")

asyncio.run(main())