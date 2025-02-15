import json
import logging
from typing import Dict, Any
from app.steps.validation import ValidationStep
from app.steps.anonymization import AnonymizationStep
from app.steps.tokenization import TokenizationStep
from app.steps.token_limit import TokenLimitCheckStep

STEP_REGISTRY = {
    "ValidationStep": ValidationStep,
    "AnonymizationStep": AnonymizationStep,
    "TokenizationStep": TokenizationStep,
    "TokenLimitCheckStep": TokenLimitCheckStep
}

class PreProcessingPipeline:
    def __init__(self, config_path: str):
        self.steps = self.load_steps(config_path)

    def load_steps(self, config_path: str):
        with open(config_path, "r") as file:
            config = json.load(file)

        steps = []
        for step_cfg in config.get("steps", []):
            if step_cfg.get("enabled", False):
                step_class = STEP_REGISTRY.get(step_cfg["name"])
                if step_class:
                    params = step_cfg.get("params", {})
                    step_instance = step_class(**params)
                    steps.append({
                        "instance": step_instance, 
                        "condition": step_cfg.get("condition"), 
                        "on_error": step_cfg.get("on_error", "halt")
                    })
        return steps

    def evaluate_condition(self, condition: str, context: dict) -> bool:
        if not condition:
            return True  
        
        local_vars = context.copy()
        local_vars["tokens_length"] = len(local_vars.get("tokens", []))

        try:
            return eval(condition, {"__builtins__": {}}, local_vars)
        except Exception as e:
            logging.error(f"Condition evaluation failed: {e}")
            return False  

    def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:
        context = {"query": request["query"], "errors": []}

        for step in self.steps:
            condition = step["condition"]
            if self.evaluate_condition(condition, context):
                try:
                    context = step["instance"].process(context)
                except Exception as e:
                    error_message = f"Error in {step['instance'].__class__.__name__}: {str(e)}"
                    context["errors"].append(error_message)
                    logging.error(error_message)

                    if step["on_error"] == "halt":
                        raise ValueError(f"Pipeline stopped due to error: {error_message}")

        return context