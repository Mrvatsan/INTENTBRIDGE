from backend.modules.base import AIModule
from jinja2 import Template
import json

class ExecutionPlanner(AIModule):
    async def process(self, structured_intent: dict) -> dict:
        prompt_template = self.load_prompt("execution_planner.txt")
        prompt = Template(prompt_template).render(
            structured_intent=json.dumps(structured_intent)
        )
        return await self._generate_structured_json(prompt)
