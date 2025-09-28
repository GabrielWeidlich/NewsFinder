from .command import Command
from strategies.crawling_strategy import CrawlingStrategy

class CrawlCommand(Command):
    """
    Comando que executa uma estratégia de crawling.
    """

    def __init__(self, strategy: CrawlingStrategy):
        self._strategy = strategy

    async def execute(self):
        """
        Executa a estratégia de crawling.
        """
        return await self._strategy.crawl()