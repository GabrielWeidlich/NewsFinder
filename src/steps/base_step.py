from abc import ABC, abstractmethod

class BaseStep(ABC):
    def __init__(self, browser):
        self.browser = browser

    @abstractmethod
    async def run(self):
        """
        Executa a ação principal do passo.
        Este método deve ser implementado por todas as subclasses.
        """
        pass