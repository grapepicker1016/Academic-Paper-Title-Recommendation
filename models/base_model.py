from abc import ABC, abstractmethod

class BaseModel(ABC):
    """
    Abstract base class for all models.
    """

    def __init__(self, config):
        self.config = config

    @abstractmethod
    def build(self):
        """
        Builds the model architecture.
        """
        pass

    @abstractmethod
    def train(self, X_train, y_train, X_val=None, y_val=None):
        """
        Trains the model.
        """
        pass

    @abstractmethod
    def summarize(self, text):
        """
        Generates a summary for the given text.
        """
        pass
