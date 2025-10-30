import re
from openai import OpenAI
from settings import LLM_BASE_URL, LLM_API_KEY, LLM_MODEL_NAME, LLM_MAX_TOKENS

class LLMClient:
    def __init__(self, api_key: str = None, base_url: str = None, model: str = None):
        self.api_key = api_key or LLM_API_KEY
        self.base_url = base_url or LLM_BASE_URL
        self.model = model or LLM_MODEL_NAME
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def load_system_prompt(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def load_user_prompt(self, path: str, **kwargs):
        with open(path, "r", encoding="utf-8") as f:
            template = f.read()
        return template.format(**kwargs)

    def chat(self, system_prompt: str, user_prompt: str, max_tokens: int = None, temperature: float = 0.1):
        max_tokens = int(max_tokens or LLM_MAX_TOKENS)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content.strip()

    def clean_sql(self, text: str):
        return re.sub(r"```sql|```", "", text, flags=re.IGNORECASE).strip()
