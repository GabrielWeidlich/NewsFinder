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
        print("A conectar-se ao browser remoto...")
        browser = await pyppeteer.connect(
            browserURL="http://browser:3000"
        )
        print("Conectado com sucesso!")

        page = await browser.newPage()
        
        # 1. Executa a estratégia de crawling para o G1
        g1_strategy = G1(page)
        await g1_strategy.run()
        
        # --- CÓDIGO CORRIGIDO E DESCOMENTADO ABAIXO ---

        # Aceder aos dados recolhidos pela estratégia
        news_list_data = g1_strategy.news_data
        
        if not news_list_data:
            print("Nenhuma notícia foi extraída com sucesso.")
            return

        # 2. Salva as notícias no banco de dados
        print("\n--- A salvar no Banco de Dados ---")
        saved_count = 0
        for news_data in news_list_data:
            # Cria um objeto News com o título, link e resumo extraídos
            news_article = News(
                title=news_data.get("title", "Título não encontrado"), 
                link=news_data.get("link"),
                summary=news_data.get("content", "")
            )
            
            try:
                db_session.add(news_article)
                db_session.commit()
                db_session.refresh(news_article)
                saved_count += 1
            except IntegrityError:
                # Ignora erros de links duplicados e continua
                db_session.rollback()
            except Exception as e:
                print(f"Erro ao salvar notícia {news_data.get('link')}: {e}")
                db_session.rollback()

        print(f"\n--- {saved_count} novas notícias salvas com sucesso! ---")

    except Exception as e:
        print(f"\nOcorreu um erro ao executar o crawler: {e}")
        print(traceback.format_exc())
        
    finally:
        # 3. Fecha os recursos
        if browser:
            await browser.disconnect() # Usa disconnect para o browser remoto
        if db_session:
            db_session.close()
        print("\n--- Crawler finalizado ---")


if __name__ == "__main__":
    asyncio.run(main())