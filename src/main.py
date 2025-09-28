import asyncio 
from crawler.crawler import Crawler
from strategies.g1_strategy import G1Strategy
from crawler.commands.crawl_command import CrawlCommand

async def main():
    # Cria o orquestrador de crawling
    crawler = Crawler()
    
    # Define a estratégia de crawling (G1 neste caso)
    g1_strategy = G1Strategy()
    
    # Cria o comando de crawling com a estratégia definida
    crawl_g1_command = CrawlCommand(g1_strategy)
    
    # Configura o comando no orquestrador
    crawler.set_command(crawl_g1_command)
    news = await crawler.run()
    
    # Imprime as noticias coletadas
    for item in news:
        print(f" - Título: {item['title']}")
        print(f"   Link: {item['link']}\n")
    