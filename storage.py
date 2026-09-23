from abc import ABC, abstractmethod

class Storage(ABC):

    @abstractmethod
    def get_expenses(self, limit, offset):
        pass

    @abstractmethod
    def get_by_id(self, expense_id):
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

    @abstractmethod
    def total_spending(self):
        pass

    @abstractmethod
    def category_wise_spending(self):
        pass