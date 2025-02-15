from app.steps.base import ProcessingStep
from typing import Dict, Any

class ValidationStep(ProcessingStep):
    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if "query" not in context or not context["query"]:
            raise ValueError("Query cannot be empty")
        context["is_valid"] = True
        return context