from abc import ABC, abstractmethod
from typing import List, Dict

class CrawlingStrategy(ABC):
    """
    Define a interface para as estratégias de crawling.
    """

    @abstractmethod
    async def crawl(self) -> List[Dict[str, str]]:
        """
        Executa o crawling e retorna uma lista de dicionários com os dados coletados.
        """
        pass