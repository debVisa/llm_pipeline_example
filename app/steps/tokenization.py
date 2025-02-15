from app.steps.base import ProcessingStep
from typing import Dict, Any

class TokenizationStep(ProcessingStep):
    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        context["tokens"] = context["query"].split()
        context["tokenized"] = True
        return context