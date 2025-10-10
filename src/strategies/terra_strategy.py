from src.steps import *
import asyncio

class Terra():
    def __init__(self, page):
        self.page = page
        self.base_url = "https://www.terra.com.br/"
        self.news_data = []
        self.getLinksSteps = [
            GoToURLStep(browser=self.page, url=self.base_url),
            GetLinksStep(browser=self.page, selector="a.card-news__text--title") 
        ]   
        
    async def run(self):
        links = []
        
        print("Iniciando a coleta de links Terra...")
        for step in self.getLinksSteps:
            result = await step.run()
            if isinstance(step, GetLinksStep):
                links = result
                
        print(f"Total de links coletados: {len(links)}")
        
        for i, link in enumerate(links, 1):
            if not link:
                continue
            
            print(f"\n[Terra] Processando notícia {i}/{len(links)}: {link}")
            
            try:
                await GoToURLStep(browser=self.page, url=link).run()
                
                get_content_step = GetContentStep(
                    browser=self.page,
                    title_selector="h1",
                    content_selector="p.text"
                )
                content_data = await get_content_step.run()
                
                if content_data:
                    content_data['link'] = link
                    self.news_data.append(content_data)
                    
            except Exception as e:
                print(f"Erro ao processar a notícia Terra: {e}")