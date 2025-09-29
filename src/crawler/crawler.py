from src.crawler.commands.command import Command

class Crawler:
    """
    Orquestrador que executa os comandos de crawling.
    """

    def __init__(self):
        self._command: Command = None

    def set_command(self, command: Command):
        self._command = command

    async def run(self):
        if self._command:
            return await self._command.execute()
        else:
            print("Nenhum comando para executar.")
            return []