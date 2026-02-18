from backend.modules.base import AIModule
from jinja2 import Template
import json

class AmbiguityResolver(AIModule):
    async def process(self, structured_intent: dict, history: list) -> dict:
        prompt_template = self.load_prompt("ambiguity_resolver.txt")
        prompt = Template(prompt_template).render(
            structured_intent=json.dumps(structured_intent),
            history=json.dumps(history)
        )
        return await self._generate_structured_json(prompt)
