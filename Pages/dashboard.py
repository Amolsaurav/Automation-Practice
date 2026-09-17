from Pages.basePage import BasePage
from playwright.sync_api import Page
from Pages.products import Products
from Pages.cart import Cart
from utilities.constants import TEXT_CART, TEXT_DELETE_ACCOUNT, TEXT_LOGOUT, TEXT_PRODUCTS


class Dashboard(BasePage):
    def __init__(self,page:Page):
        super().__init__(page)
        self.product_link = self.page.get_by_role('link',name=TEXT_PRODUCTS)
        self.cart_link = self.page.get_by_role('link',name=TEXT_CART).first
        self.logoutLink = self.page.get_by_role('link',name=TEXT_LOGOUT)
        self.delete_account_link = self.page.get_by_role('link',name = TEXT_DELETE_ACCOUNT)
    
    def navigate_to_products_page(self):
        self.click(self.product_link)
        productPage = Products(self.page)
        return productPage
    
    def navigate_to_cart_page(self):
        self.click(self.cart_link)
        cartPage = Cart(self.page)
        return cartPage
    
    def logout_user(self):
        self.click(self.logoutLink)
    
    def delete_account(self):
        self.click(self.delete_account_link)
        
        