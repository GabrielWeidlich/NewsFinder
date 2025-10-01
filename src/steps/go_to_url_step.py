from .base_step import BaseStep
from pyppeteer.page import Page

class GoToURLStep(BaseStep):
    def __init__(self, browser: Page, url: str):
        super().__init__(browser)
        self.url = url

    async def run(self):
        """
        Navega até a URL especificada.
        """
        print(f"Navegando para: {self.url}")
        await self.browser.goto(self.url)