from app.steps.base import ProcessingStep
from typing import Dict, Any

class TokenLimitCheckStep(ProcessingStep):
    def __init__(self, max_tokens: int = 100):
        self.max_tokens = max_tokens

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if len(context.get("tokens", [])) > self.max_tokens:
            raise ValueError("Token limit exceeded")
        context["token_check_passed"] = True
        return context