import asyncio
import pyppeteer
import traceback
from sqlalchemy.exc import IntegrityError

# A importação direta do G1 não é mais necessária, o Manager cuida disso
from src.database.setup import get_db
from src.database.models.news import News
from src.strategies.strategy_manager import StrategyManager

async def main():
    """
    Função principal que orquestra o processo de crawling e armazenamento de notícias.
    """
    browser = None
    db_session = next(get_db())
    
    # CORREÇÃO 1: Declarar as variáveis aqui para garantir que existem no bloco 'finally'
    saved_count = 0
    all_news_data = []
    
    try:
        print("A conectar-se ao browser remoto...")
        browser = await pyppeteer.connect(
            browserURL="http://browser:3000"
        )
        print("Conectado com sucesso!")

        page = await browser.newPage()
        
        strategy_manager = StrategyManager(page)
        await strategy_manager.run_all()
        
        all_news_data = strategy_manager.all_news_data
        
        if not all_news_data:
            print("Nenhuma notícia coletada.")
            # return não é ideal aqui, pois queremos que o 'finally' execute corretamente
        else:
            print(f"\nA salvar {len(all_news_data)} notícias no banco de dados...")
            for news in all_news_data:
                try:
                    # CORREÇÃO 2: Usar o método .get() para aceder ao dicionário
                    # CORREÇÃO 3: Usar 'summary' em vez de 'content' para corresponder ao modelo
                    news_entry = News(
                        title=news.get('title', "Título não disponível"),
                        summary=news.get('content', ""), # O GetContentStep retorna 'content', mas guardamos em 'summary'
                        link=news.get('link')
                    )
                    
                    if news_entry.link: # Garante que não tenta salvar notícias sem link
                        db_session.add(news_entry)
                        db_session.commit()
                        saved_count += 1
                    
                except IntegrityError:
                    db_session.rollback()
                    # A mensagem foi removida para não poluir o log com notícias que já existem
                except Exception as e:
                    db_session.rollback()
                    print(f"Erro ao salvar notícia: {e}")
                    
    except Exception as e:
        print(f"\nOcorreu um erro ao executar o crawler: {e}")
        print(traceback.format_exc())

    finally:
        if browser:
            await browser.disconnect()
        if db_session:
            db_session.close()
        print("\n--- Crawler finalizado ---")
        # Agora esta linha funcionará sempre, mesmo que ocorra um erro
        print(f"Total de notícias salvas nesta execução: {saved_count}")
        
if __name__ == "__main__":
    asyncio.run(main())