from core.sql_agent.agent import SQLAgent
from tabulate import tabulate

agent = SQLAgent()

try:
    response = agent.handle_query_intent(input("Tanya sesuatu: "))
    result = response["result"]
    if result["rows"]:
        print(tabulate(result["rows"], headers=result["columns"], tablefmt="psql"))
    else:
        print("Query berhasil, tapi tidak ada hasil.")
except Exception as e:
    print("Failed to generate:", str(e))
