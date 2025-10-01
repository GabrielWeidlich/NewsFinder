import asyncio
from src.steps import *

class G1():
    def __init__(self, browser):
        self.browser = browser
        self.base_url = "https://g1.globo.com/"
        self.links = []
        
        self.getLinksSteps = [
            # Passo para ir para a URL principal do G1
            GoToURLStep(browser=self.browser, url=self.base_url),
            # Passo para pegar os links das notícias usando um seletor CSS
            GetLinksStep(browser=self.browser, selector="a.feed-post-link") 
        ]
        self.getContentByLinks = []
        
        
    async def run(self):
        for step in self.getLinksSteps:
            if isinstance(step, GetLinksStep): #trocar get links para a classe que vai pegar os links
                self.links = await step.run()
            else:
                await step.run()
                
        print(f"Links encontrados: {self.links}")
        # for step in self.getContentByLinks:
        #     await step.run()
            