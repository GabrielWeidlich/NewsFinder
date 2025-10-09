from src.steps import *
import asyncio

class Portal6():
    def __init__(self, page):
        self.page = page
        self.base_url = "https://portal6.com.br/"
        self.news_data = []
        self.getLinksSteps = [
            GoToURLStep(browser=self.page, url=self.base_url),
            GetLinksStep(browser=self.page, selector="a.style_pri") 
        ]
        
    async def run(self):
        links = []
        
        print("Iniciando a coleta de links Portal6...")
        for step in self.getLinksSteps:
            result = await step.run()
            if isinstance(step, GetLinksStep):
                links = result
                
        print(f"Total de links coletados: {len(links)}")
        
        for i, link in enumerate(links, 1):
            if not link:
                continue
            
            print(f"\n[Portal6] Processando notícia {i}/{len(links)}: {link}")
            
            try:
                await GoToURLStep(browser=self.page, url=link).run()
                
                get_content_step = GetContentStep(
                    browser=self.page,
                    title_selector="h1.titulo",
                    content_selector="div.p__single--content p:not(.data)"
                )
                content_data = await get_content_step.run()
                
                if content_data:
                    content_data['link'] = link
                    self.news_data.append(content_data)
                    
            except Exception as e:
                print(f"Erro ao processar a notícia Portal6: {e}")