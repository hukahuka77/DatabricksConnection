from databricks import sql
import os
from dotenv import load_dotenv

load_dotenv()

connection = sql.connect(
                        server_hostname = "adb-768728587798803.3.azuredatabricks.net",
                        http_path = "/sql/1.0/warehouses/7796604622e5d344",
                        access_token = os.getenv('DATABRICKS_ACCESS_TOKEN'),
                        timeout = 10)

cursor = connection.cursor()

cursor.execute("SELECT * from mydatabase.mockdata WHERE id = '3'")
print(cursor.fetchall())

cursor.close()
connection.close()