import asyncio
from src.steps import *

class G1():
    # ALTERAÇÃO AQUI: Recebe 'page' em vez de 'browser'
    def __init__(self, page):
        self.page = page # Armazena o objeto da página
        self.base_url = "https://g1.globo.com/"
        self.news_data = [] 
        
        self.getLinksSteps = [
            # Usa self.page em vez de self.browser
            GoToURLStep(browser=self.page, url=self.base_url),
            GetLinksStep(browser=self.page, selector="a.feed-post-link") 
        ]
        
    async def run(self):
        links = []
        for step in self.getLinksSteps:
            result = await step.run()
            if isinstance(step, GetLinksStep):
                links = result 
                
        print(f"Total de links coletados: {len(links)}")
        
        for i, link in enumerate(links, 1):
            if not link:
                continue
            
            print(f"\nProcessando notícia {i}/{len(links)}: {link}")
            
            try:
                go_to_news_step = GoToURLStep(browser=self.page, url=link)
                await go_to_news_step.run()
                get_content_step = GetContentStep(
                    browser=self.page,
                    title_selector="h1.content-head__title",
                    content_selector="p.content-text__container"
                )
                content_data = await get_content_step.run()
                
                if content_data:
                    content_data['link'] = link
                    self.news_data.append(content_data)
                
            except Exception as e:
                print(f"Erro ao processar a notícia: {e}")
    
                
        
        
        
