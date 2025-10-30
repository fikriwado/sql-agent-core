from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError
from core.log import logger
from settings import DATABASE_URL

class DatabaseClient:
    def __init__(self, url: str = None):
        self.url = url or DATABASE_URL
        self.engine = create_engine(self.url)

        try:
            self.test_connection()
            self.inspector = inspect(self.engine)
        except SQLAlchemyError as e:
            logger.critical(f"Cannot connect to database: {e}")
            raise SystemExit(1)

    def test_connection(self):
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Database connection OK.")
        except SQLAlchemyError as e:
            logger.error(f"Connection test failed: {e}")
            raise

    def execute(self, query: str):
        try:
            with self.engine.connect() as conn:
                return conn.execute(text(query))
        except SQLAlchemyError as e:
            logger.error(f"Query failed: {e}")
            raise

    def get_schema(self):
        result_data = {"total_tables": 0, "tables": {}}

        try:
            table_names = self.inspector.get_table_names()
            result_data['total_tables'] = len(table_names)

            for table_name in table_names:
                table_data = {
                    "columns": [],
                    "primary_keys": [],
                    "foreign_keys": [],
                    "indexes": []
                }

                table_data["columns"] = [
                    {
                        "name": column["name"],
                        "type": column["type"],
                        "nullable": column["nullable"],
                        "default": column["default"]
                    }
                    for column in self.inspector.get_columns(table_name)
                ]

                pk = self.inspector.get_pk_constraint(table_name)
                table_data["primary_keys"] = pk.get("constrained_columns", [])

                table_data["foreign_keys"] = [
                    {
                        "constrained_columns": fk["constrained_columns"],
                        "referred_table": fk["referred_table"],
                        "referred_columns": fk["referred_columns"]
                    }
                    for fk in self.inspector.get_foreign_keys(table_name)
                ]

                table_data["indexes"] = [
                    {
                        "name": idx["name"],
                        "columns": idx["column_names"],
                        "unique": idx["unique"]
                    }
                    for idx in self.inspector.get_indexes(table_name)
                ]

                result_data["tables"][table_name] = table_data

            logger.info("Database schema retrieved successfully.")
        except SQLAlchemyError as e:
            logger.error(f"Failed to retrieve schema: {e}")
            raise

        return result_data
