from .g1_strategy import G1
from .cnn_strategy import CNN
from .portal6_strategy import Portal6

class StrategyManager:
    def __init__(self, page):
        self.page = page
        self.strategies = {
            "G1": G1(self.page),
            "Portal6": Portal6(self.page),
            "CNN": CNN(self.page)
        }
        self.all_news_data = []
        
    async def run_all(self):
        "Executa todas as estratégias de crawling."
        
        for strategy in self.strategies.values():
            try:
                await strategy.run()
                self.all_news_data.extend(strategy.news_data)
            except Exception as e:
                print(f"Erro ao executar a estratégia {strategy}: {e}")
            
        
    
