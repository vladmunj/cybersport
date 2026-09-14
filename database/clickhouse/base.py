from abc import ABC, abstractmethod

class Migration(ABC):
    @abstractmethod
    def upgrade(self, client):
        pass

    @abstractmethod
    def downgrade(self, client):
        pass