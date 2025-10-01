import asyncio
import pyppeteer
import traceback
from sqlalchemy.exc import IntegrityError

from src.strategies.g1_strategy import G1
from src.database.setup import get_db
from src.database.models.news import News

async def main():
    """
    Função principal que orquestra o processo de crawling e armazenamento de notícias.
    """
    browser = None
    db_session = next(get_db())
    
    try:
        print("--- Iniciando o Crawler ---")
        browser = await pyppeteer.launch(
            headless=True,  # Mude para False se quiser ver o navegador abrindo
            args=['--no-sandbox']
        )
        page = await browser.newPage()

        # 1. Executa a estratégia de crawling para o G1
        g1_strategy = G1(page)
        await g1_strategy.run()
        
        # news_list = g1_strategy.links
        
        # if not news_list:
        #     print("Nenhuma notícia encontrada.")
        #     return

        # print("\n--- Notícias Coletadas ---")
        # for i, link in enumerate(news_list, 1):
        #     print(f"  {i}. Link: {link}")

        # # 2. Salva as notícias no banco de dados
        # print("\n--- A salvar no Banco de Dados ---")
        # saved_count = 0
        # for link_url in news_list:
        #     # Simplificação: Usando o próprio link como título por enquanto
        #     # O ideal seria extrair o título real na estratégia de crawling
        #     news_article = News(
        #         title=f"Notícia de {link_url}", 
        #         link=link_url,
        #         content="" # O conteúdo pode ser extraído em um passo futuro
        #     )
            
        #     try:
        #         db_session.add(news_article)
        #         db_session.commit()
        #         db_session.refresh(news_article)
        #         saved_count += 1
        #     except IntegrityError:
        #         # Ignora erros de integridade (links duplicados) e continua
        #         db_session.rollback()
        #     except Exception as e:
        #         print(f"Erro ao salvar notícia {link_url}: {e}")
        #         db_session.rollback()

        # print(f"\n--- {saved_count} novas notícias salvas com sucesso! ---")

    except Exception as e:
        print(f"\nOcorreu um erro ao executar o crawler: {e}")
        print(traceback.format_exc())
        
    finally:
        # 3. Fecha os recursos
        if browser:
            await browser.close()
        # if db_session:
        #     db_session.close()
        # print("\n--- Crawler finalizado ---")


if __name__ == "__main__":
    # Executa a função principal assíncrona
    asyncio.run(main())