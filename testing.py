# ----------------------------------------------
# ------------------ TEST LLM ------------------
# ----------------------------------------------
from core.sql_agent.agent import SQLAgent
import pandas as pd
from tabulate import tabulate

agent = SQLAgent()

# ------------------------
# ------- Classify -------
# ------------------------
# try:
#     question = "Tampilkan 10 karyawan pertama dari departemen IT"
#     # question = "Ada table apa aja"
#     result = agent.classify_intent(question)
#     print("Koneksi berhasil, response:")
#     print(result)
# except Exception as e:
#     print("Failed to calssify:", str(e))
# ------------------------

# ------------------------
# ----- Generate SQL -----
# ------------------------
# try:
#     from core.database import DatabaseClient
#     db = DatabaseClient()

#     question = "Tampilkan karyawan yang tahun lahirnya 2000"
#     result = agent.generate_sql(db.get_schema(), question)

#     print(result)
# except Exception as e:
#     print("Failed to generate:", str(e))
# ------------------------

# ------------------------
# ----- Generate SQL -----
# ------------------------
try:
    result = agent.handle_query_intent(input("Tanya sesuatu: "))
    rows = result.mappings().all()
    df = pd.DataFrame(rows)
    print(tabulate(df, headers='keys', tablefmt='psql'))
except Exception as e:
    print("Failed to generate:", str(e))
# ------------------------
# ----------------------------------------------

# ----------------------------------------------
# ------------------ TEST DB -------------------
# ----------------------------------------------
# from core.database import DatabaseClient

# db = DatabaseClient()

# # ------------------------
# # -------- Query ---------
# # ------------------------
# # users = db.execute("SELECT * FROM users")
# # rows = users.mappings().all()

# # for row in rows:
# #     print(dict(row))
# # ------------------------

# # ------------------------
# # -------- Schema --------
# # ------------------------
# schema = db.get_schema()
# print(schema)
# # ------------------------
