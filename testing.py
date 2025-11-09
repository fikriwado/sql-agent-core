from core.sql_agent.agent import SQLAgent
from tabulate import tabulate
from core.database import DatabaseClient


db_url = DatabaseClient.build_database_url(
    db_type="mysql",
    host="127.0.0.1:3306",
    username="root",
    password="",
    db_name="testing_bos"
)

agent = SQLAgent(db_url)

try:
    response = agent.handle_query_intent(input("Tanya sesuatu: "))
    result = response["result"]
    # print(result["info"])
    if result["rows"]:
        print(tabulate(result["rows"], headers=result["columns"], tablefmt="psql"))
    else:
        print("Query berhasil, tapi tidak ada hasil.")
except Exception as e:
    print("Failed to generate:", str(e))
