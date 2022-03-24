from playwright.sync_api import Playwright, sync_playwright
import json

class Browser :

    def __init__(self):
        pass

    def lunch_browser(self,) :
        browser = sync_playwright().chromium.launch()
        return browser