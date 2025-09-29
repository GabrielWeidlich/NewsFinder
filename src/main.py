import asyncio
import traceback
from src.crawler.crawler import Crawler
from src.strategies.g1_strategy import G1Strategy
from src.crawler.commands.crawl_command import CrawlCommand
# ... e as importações do banco de dados
from database.setup import get_db
from database.models.news import News
from sqlalchemy.exc import IntegrityError

async def main():
    db_session = None
    try:
        crawler = Crawler()
        g1_strategy = G1Strategy()
        crawl_g1_command = CrawlCommand(g1_strategy)
        
        crawler.set_command(crawl_g1_command)
        news_list = await crawler.run()

        if not news_list:
            print("Nenhuma notícia encontrada.")
            return

        print(f"\n--- {len(news_list)} Notícias Coletadas ---")
        for item in news_list:
            print(f"  - Título: {item['title']}")
            print(f"    Link: {item['link']}")

        # Lógica para salvar no banco de dados
        print("\n--- A salvar no Banco de Dados ---")
        db_session = next(get_db())
        saved_count = 0
        for item in news_list:
            news_article = News(
                title=item['title'],
                link=item['link']
            )
            db_session.add(news_article)
            try:
                db_session.commit()
                saved_count += 1
                db_session.refresh(news_article) # Atualiza o objeto após o commit
            except IntegrityError:
                db_session.rollback() # Desfaz se o link já existir

        print(f"--- {saved_count} novas notícias salvas com sucesso! ---")

    except Exception as e:
        print("Ocorreu um erro ao executar o crawler:")
        print(traceback.format_exc())
    finally:
        # Garante que a sessão com o banco seja fechada
        if db_session:
            db_session.close()

if __name__ == "__main__":
    asyncio.run(main())