from playwright.sync_api import Playwright, sync_playwright
from playwright.async_api import async_playwright
import json

class Browser :

    def __init__(self,**kwargs) :
        self.__dict__.update(kwargs)


    def run(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            return context


            
    
    
    
    
