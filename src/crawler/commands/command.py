from abc import ABC, abstractmethod

class Command(ABC):
    """
    Define a interface para os comandos.
    """

    @abstractmethod
    async def execute(self):
        """
        Executa o comando.
        """
        pass