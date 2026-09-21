from pathlib import Path
from playwright.sync_api import Page,Locator
from utilities.constants import (
    SCREENSHOT_CLICK_ERROR,
    SCREENSHOT_DIRECTORY,
    SCREENSHOT_FILL_ERROR,
    SCREENSHOT_CHECK_ERROR,
    SCREENSHOT_SELECT_OPTION_ERROR,
)

class BasePage:
    def __init__(self,page:Page):
        self.page = page
    
    def wait_for_visible(self,locator:Locator) -> None:
        locator.wait_for(state='visible')
    
    def take_screenshot(self, file_name: str) -> None:
        screenshot_dir = Path(SCREENSHOT_DIRECTORY)
        screenshot_dir.mkdir(exist_ok=True)

        self.page.screenshot(
            path=str(screenshot_dir / file_name),
            full_page=True
        )
    
    def click(self, locator: Locator) -> None:

        try:
            self.wait_for_visible(locator)
            locator.scroll_into_view_if_needed()
            locator.click()

        except Exception:
            self.take_screenshot(SCREENSHOT_CLICK_ERROR)
            raise

    def fill(self, locator: Locator, value: str) -> None:
    
        try:
            self.wait_for_visible(locator)
            locator.fill(value)

        except Exception:
            self.take_screenshot(SCREENSHOT_FILL_ERROR)
            raise

    def check(self, locator: Locator) -> None:
  
        try:
            self.wait_for_visible(locator)
            locator.scroll_into_view_if_needed()
            locator.check()

        except Exception:
            self.take_screenshot(SCREENSHOT_CHECK_ERROR)
            raise

    def select_option(self, locator: Locator, value: str) -> None:

        try:
            self.wait_for_visible(locator)
            locator.select_option(value=value)

        except Exception:
            self.take_screenshot(SCREENSHOT_SELECT_OPTION_ERROR)
            raise

    def get_text(self,locator:Locator) -> str:
        self.wait_for_visible(locator)
        return locator.inner_text().strip()
    
    def is_visible(self,locator:Locator) ->bool:
        return locator.is_visible()
    
    def get_url(self) ->str:
        return self.page.url
    
    def get_title(self) ->str:
        return self.page.title()
    