import re
import pandas as pd
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
            logger.info("[SQLAgent::classify_intent] Start classify intent")
            system_prompt = self.llm.load_system_prompt(f"{self.__base_dir}/system/classify_intent.txt")
            user_prompt = self.llm.load_user_prompt(f"{self.__base_dir}/user/classify_intent.txt", question=question)

            result = self.llm.chat(system_prompt, user_prompt, 10)
            if result not in ["query", "schema_info"]:
                logger.warning(f"[SQLAgent::classify_intent] Unexpected result: {result!r}")
                return "wrong_classify"

            logger.info(f"[SQLAgent::classify_intent] Classified intent: {result}")
            return result
        except Exception as e:
            logger.exception(f"[SQLAgent::classify_intent] Failed to classify intent: {e}")
            return "failed"

    def generate_sql(self, question: str):
        try:
            logger.info("[SQLAgent::generate_sql] Start generating SQL")

            filename = "generate_sql.txt"
            schema_data = self.db.get_schema()

            system_prompt = self.llm.load_system_prompt(f"{self.__base_dir}/system/{filename}")
            user_prompt = self.llm.load_user_prompt(f"{self.__base_dir}/user/{filename}", schema_data=schema_data, question=question)

            result = self.llm.chat(system_prompt, user_prompt, temperature=0.2)
            logger.debug(f"[SQLAgent::generate_sql] Raw LLM response: {repr(result[:200])}")

            result = self.llm.clean_sql(result)
            logger.debug(f"[SQLAgent::generate_sql] After clean_sql: {repr(result[:200])}")

            if not result or len(result.strip()) == 0:
                raise ValueError("Empty SQL result from LLM")

            select_pattern = r"(SELECT\s+.*?)(?:;|\Z)"
            match = re.search(select_pattern, result, re.IGNORECASE | re.DOTALL)

            if match:
                result = match.group(1).strip()
                logger.debug(f"[SQLAgent::generate_sql] Extracted query via regex: {repr(result[:200])}")
                logger.info("[SQLAgent::generate_sql] Successfully extracted SQL query")
                return result

            logger.info("[SQLAgent::generate_sql] No SELECT match found, returning cleaned SQL")
            return result
        except Exception as e:
            logger.exception(f"[SQLAgent::generate_sql] Failed to generate SQL: {e}")
            return None

    def generate_schema_info(self, question: str):
        try:
            logger.info("[SQLAgent::generate_schema_info] Start generating schema info")

            filename = "generate_schema_info.txt"
            schema_data = self.db.get_schema()

            system_prompt = self.llm.load_system_prompt(f"{self.__base_dir}/system/{filename}")
            user_prompt = self.llm.load_user_prompt(f"{self.__base_dir}/user/{filename}", schema_data=schema_data, question=question)

            result = self.llm.chat(system_prompt, user_prompt, temperature=0.3)
            logger.debug(f"[SQLAgent::generate_schema_info] Raw LLM response: {repr(result[:200])}")

            if not result or len(result) < 10:
                logger.warning("[SQLAgent::generate_schema_info] Weak or empty LLM response, returning fallback message")
                return f"The database contains {schema_data.get('total_tables', 0)}. Please ask a more specific question about the database structure."

            logger.info("[SQLAgent::generate_schema_info] Successfully generated schema info")
            return result
        except Exception as e:
            logger.exception(f"[SQLAgent::generate_schema_info] Failed to generate schema info: {e}")
            return None

    def handle_query_intent(self, question: str):
        try:
            logger.info("[SQLAgent::handle_query_intent] Start handling query intent")

            query = self.generate_sql(question)
            logger.debug(f"[SQLAgent::handle_query_intent] Generated SQL: {repr(query[:200])}")

            if not query.lower().startswith('select'):
                logger.warning(f"[SQLAgent::handle_query_intent] Invalid query generated: {query!r}")
                raise ValueError("Invalid query")

            result = self.db.execute(query)
            logger.info("[SQLAgent::handle_query_intent] Query executed successfully")

            response = {
                "type": "query",
                "result": {
                    "query": query,
                    "columns": list(result.keys()),
                    "rows": [tuple(row) for row in result.fetchall()]
                }
            }

            logger.debug(f"[SQLAgent::handle_query_intent] Response prepared with {len(response['result']['rows'])} rows")
            return response
        except Exception as e:
            logger.exception(f"[SQLAgent::handle_query_intent] Failed to handle query intent: {e}")
            return {"type": "query", "error": str(e)}

    def handle_schema_info_intent(self, question: str):
        try:
            logger.info("[SQLAgent::handle_schema_info_intent] Start handling schema info intent")

            result = self.generate_schema_info(question)
            logger.debug(f"[SQLAgent::handle_schema_info_intent] Generated schema info: {repr(result[:200])}")

            logger.info("[SQLAgent::handle_schema_info_intent] Successfully handled schema info intent")
            return {
                "type": "schema_info",
                "result": { "info": result }
            }
        except Exception as e:
            logger.exception(f"[SQLAgent::handle_schema_info_intent] Failed to handle schema info intent: {e}")
            return {"type": "schema_info", "error": str(e)}
