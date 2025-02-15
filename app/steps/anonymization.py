from app.steps.base import ProcessingStep
from typing import Dict, Any

class AnonymizationStep(ProcessingStep):
    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        context["query"] = context["query"].replace("John Doe", "[REDACTED]")
        context["anonymized"] = True
        return context