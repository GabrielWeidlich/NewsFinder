from .base_step import BaseStep
from pyppeteer.page import Page
from typing import List

class GetLinksStep(BaseStep):
    def __init__(self, browser: Page, selector: str):
        super().__init__(browser)
        self.selector = selector

    async def run(self) -> List[str]:
        """
        Encontra todos os elementos que correspondem ao seletor CSS e
        retorna uma lista de seus atributos 'href'.
        """
        print(f"Buscando links com o seletor: '{self.selector}'")
        
        # Espera o seletor aparecer na página para garantir que o conteúdo carregou
        await self.browser.waitForSelector(self.selector)

        # Executa um script na página para extrair os links
        links = await self.browser.querySelectorAll(self.selector)
        
        hrefs = []
        for link in links:
            href = await self.browser.evaluate('(element) => element.href', link)
            hrefs.append(href)
            
        print(f"Encontrados {len(hrefs)} links.")
        return hrefs