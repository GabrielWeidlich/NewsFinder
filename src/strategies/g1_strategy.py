import asyncio
from typing import Dict, List
from .crawling_strategy import CrawlingStrategy
from pyppeteer import launch

class G1Strategy(CrawlingStrategy):
    """
    Implementa a estratégia de crawling para o site G1.
    """

    def __init__(self, url: str = "https://g1.globo.com/"):
        self.url = url

    async def crawl(self) -> List[Dict[str, str]]:
        print("Iniciando crawling no G1...")
        browser = await launch()
        page = await browser.newPage()
        await page.goto(self.url)

        # Exemplo: extrai os títulos das notícias da página inicial do G1
        # IMPORTANTE: Este seletor CSS pode mudar. Ajuste conforme necessário.
        news_elements = await page.querySelectorAll('.feed-post-link')
        
        news_list = []
        for element in news_elements:
            title = await page.evaluate('(element) => element.textContent', element)
            link = await page.evaluate('(element) => element.href', element)
            news_list.append({"title": title, "link": link})

        await browser.close()
        print(f"Encontradas {len(news_list)} notícias no G1.")
        return news_list
    