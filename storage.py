from abc import ABC, abstractmethod
class Storage(ABC):

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def add(self, expense):
        pass

    @abstractmethod
    def update(self, expense_id, expense):
        pass

    @abstractmethod
    def delete(self, expense_id):
        pass