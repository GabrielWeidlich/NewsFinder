from .base_step import BaseStep
from pyppeteer.page import Page
from typing import Dict, Optional

class GetContentStep(BaseStep):
    def __init__(self, browser: Page, title_selector: str, content_selector: str):
        super().__init__(browser)
        self.title_selector = title_selector
        self.content_selector = content_selector

    async def run(self) -> Optional[Dict[str, str]]:
        """
        Encontra o título e o conteúdo da notícia na página atual
        e retorna-os num dicionário.
        """
        try:
            print("A extrair título e conteúdo...")
            
            # Espera pelos seletores para garantir que a página carregou
            await self.browser.waitForSelector(self.title_selector)
            await self.browser.waitForSelector(self.content_selector)

            # Extrai o texto do título
            title_element = await self.browser.querySelector(self.title_selector)
            title = await self.browser.evaluate('(element) => element.textContent', title_element)

            # Extrai o texto do conteúdo/resumo
            content_element = await self.browser.querySelector(self.content_selector)
            content = await self.browser.evaluate('(element) => element.textContent', content_element)
            
            print("Conteúdo extraído com sucesso.")
            return {"title": title.strip(), "content": content.strip()}
        
        except Exception as e:
            print(f"Não foi possível extrair o conteúdo: {e}")
            return None