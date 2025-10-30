import re
from core.llm import LLMClient
from core.log import logger
from core.database import DatabaseClient

class SQLAgent:
    __base_dir = "core/sql_agent/prompts"

    def __init__(self):
        self.llm = LLMClient()
        self.db = DatabaseClient()

    def classify_intent(self, question: str):
        try:
            system_prompt = self.llm.load_system_prompt(f"{self.__base_dir}/system/classify_intent.txt")
            user_prompt = self.llm.load_user_prompt(f"{self.__base_dir}/user/classify_intent.txt", question=question)

            result = self.llm.chat(system_prompt, user_prompt, 10)
            if result not in ["query", "schema_info"]:
                return "wrong classify"

            return result
        except Exception as e:
            logger.error(f"Failed to classify intent: {e}")

    def generate_sql(self, schema_data: str, question: str):
        try:
            system_prompt = self.llm.load_system_prompt(f"{self.__base_dir}/system/generate_sql.txt")
            user_prompt = self.llm.load_user_prompt(f"{self.__base_dir}/user/generate_sql.txt", schema_data=schema_data, question=question)

            result = self.llm.chat(system_prompt, user_prompt)
            logger.info(f"[DEBUG] Raw LLM response: {repr(result[:200])}")

            result = self.llm.clean_sql(result)
            logger.info(f"[DEBUG] After clean_sql: {repr(result[:200])}")

            select_pattern = r"(SELECT\s+.*?)(?:;|\Z)"
            match = re.search(select_pattern, result, re.IGNORECASE | re.DOTALL)

            if match:
                result = match.group(1).strip()
                print(f"[DEBUG] Extracted query via regex: {repr(result[:200])}")
                return result

            return result
        except Exception as e:
            logger.error(f"Failed to generate sql: {e}")

    def handle_query_intent(self, question: str):
        try:
            query = self.generate_sql(self.db.get_schema(), question)

            if not query.lower().startswith('select'):
                raise ValueError("Invalid query")

            return self.db.execute(query)
        except Exception as e:
            logger.error(f"Failed to handle query intent: {e}")


    def handle_schema_info_intent(self):
        pass
