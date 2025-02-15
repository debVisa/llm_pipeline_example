from abc import ABC, abstractmethod
from typing import Dict, Any

class ProcessingStep(ABC):
    @abstractmethod
    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Modify the context dictionary and return it."""
        pass