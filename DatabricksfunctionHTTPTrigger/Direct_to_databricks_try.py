import logging
import azure.functions as func
from databricks import sql
from azure.identity import DefaultAzureCredential
from azure.identity import ClientSecretCredential
from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv
import os
import json
import requests

def get_data(user_id, credential):
    # Acquire a token using the managed identity
    #2ff814a6-3304-4ab8-85cb-cd0e6f879c1d
    #"https://databricks.azure.com/.default"
    # token = credential.get_token()  # Databricks resource ID for Azure
    token ="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6InoxcnNZSEhKOS04bWdndDRIc1p1OEJLa0JQdyIsImtpZCI6InoxcnNZSEhKOS04bWdndDRIc1p1OEJLa0JQdyJ9.eyJhdWQiOiJodHRwczovL21hbmFnZW1lbnQuY29yZS53aW5kb3dzLm5ldC8iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9lYWEyZmNjOS1iYTdlLTRkNGYtYmRkNi01ZmU4ZWU1ZTY3MDIvIiwiaWF0IjoxNzM2NDQyMDA5LCJuYmYiOjE3MzY0NDIwMDksImV4cCI6MTczNjQ0NjM3NCwiYWNyIjoiMSIsImFpbyI6IkFaUUFhLzhZQUFBQVBJNmpVZFBYRkpJQWF5WFJYWkRybU13SVNpWDNxdzUvWmozQ0ZzdktNU1RMNkM2bFF3SFVaMFpPczc3ZTh3KzR3NFFLNWhMM0V6emE3MjYydFFqU2hicUxxVHNQMyt5aW8xOSt5QklkMWdNT1FTVmdXQ0p3Wm1OTGhJUGJEQmRZZk1wb2NGRTU3djBpQ1RPR1MrbHVmcXJtV29PV3BPS0RvRU1jZFJyNlV3OXlqK1lVT05KbXVBbHpGbmJ1N0Y3SCIsImFsdHNlY2lkIjoiMTpsaXZlLmNvbTowMDAzN0ZGRTY2REFDQjFEIiwiYW1yIjpbInB3ZCIsIm1mYSJdLCJhcHBpZCI6IjA0YjA3Nzk1LThkZGItNDYxYS1iYmVlLTAyZjllMWJmN2I0NiIsImFwcGlkYWNyIjoiMCIsImVtYWlsIjoiYW5kcmV3Lmxvbmcta2V0dGVuaG9mZW5Ab3V0bG9vay5jb20iLCJmYW1pbHlfbmFtZSI6IkxvbmctS2V0dGVuaG9mZW4iLCJnaXZlbl9uYW1lIjoiQW5kcmV3IiwiZ3JvdXBzIjpbImU4MTk2NmQxLThmMDktNDY5NC04M2RjLTRiMjNmM2Q0ZDM3YyJdLCJpZHAiOiJsaXZlLmNvbSIsImlkdHlwIjoidXNlciIsImlwYWRkciI6IjI2MDA6ODgwMDo0ODk1OmIxMDA6YzQxNDo2YmU3OmU0YjI6Y2I5MCIsIm5hbWUiOiJBbmRyZXcgTG9uZy1LZXR0ZW5ob2ZlbiIsIm9pZCI6ImZkN2U4YzA3LTA0NTUtNDRiZC1iZWYwLTNkMjI3NTlkMWY2NCIsInB1aWQiOiIxMDAzMjAwMzVBRDg0NjhFIiwicmgiOiIxLkFjb0F5ZnlpNm42NlQwMjkxbF9vN2w1bkFrWklmM2tBdXRkUHVrUGF3ZmoyTUJQNkFGREtBQS4iLCJzY3AiOiJ1c2VyX2ltcGVyc29uYXRpb24iLCJzdWIiOiJMYS10dE01b0FOX1NzYjVZcW9QajNiNzBJWmV2Q3dkRHktMm5xTVpGcnJvIiwidGlkIjoiZWFhMmZjYzktYmE3ZS00ZDRmLWJkZDYtNWZlOGVlNWU2NzAyIiwidW5pcXVlX25hbWUiOiJsaXZlLmNvbSNhbmRyZXcubG9uZy1rZXR0ZW5ob2ZlbkBvdXRsb29rLmNvbSIsInV0aSI6IkpkQjMxcDB5QTBXaEFaczVCRFIzQUEiLCJ2ZXIiOiIxLjAiLCJ3aWRzIjpbIjYyZTkwMzk0LTY5ZjUtNDIzNy05MTkwLTAxMjE3NzE0NWUxMCIsImI3OWZiZjRkLTNlZjktNDY4OS04MTQzLTc2YjE5NGU4NTUwOSJdLCJ4bXNfY2FlIjoiMSIsInhtc19jYyI6WyJDUDEiXSwieG1zX2Vkb3YiOnRydWUsInhtc19pZHJlbCI6IjEgMjIiLCJ4bXNfdGNkdCI6MTcwOTE2MjQ2OX0.VmJE0KvQlPLmrhuyd-C4ATEyA8yi00HIQokHZ-W_AOnE0wG8Iiv63sbl5N-iTX0kdFqlX2bAxUF24CYDKpwx0_zZOtyFkwVNsGTbUaW7cBoHx1zfBteYx96haExoZBGfWpsOblBbfNuNoSZ9FrORHHnKFlRQoXDn3L3o0VSa7Kpu0cKVHyRy-jXStVEiWYfZXrZ5CgNIIN0Jnt9fOicQnFFwOvZNhTd4oWVemIJCrKxBudlLQ3VBz-dxI57VgMID98wCjxBP6qt7FEj5Q8ylVf9Prpd-WYyWLn1YwuRBivzyXGfZIpyrZPN8aSPpRhP--GE33BRhz0_WcKVKrd76MA"
    connection = sql.connect(
        server_hostname="adb-768728587798803.3.azuredatabricks.net",
        http_path="/sql/1.0/warehouses/7796604622e5d344",
        access_token=token,  # Use the token from managed identity
        timeout=10
    )

    cursor = connection.cursor()

    query = "SELECT * FROM mydatabase.mockdata WHERE id = ?"
    cursor.execute(query, (user_id,))
    data = cursor.fetchall()

    cursor.close()
    connection.close()
    return data

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logging.info('Processing HTTP trigger.')

        # Get the user ID from the request body
        req_body = req.get_json()
        user_id = req_body.get('id')

        if not user_id:
            return func.HttpResponse(
                "Please provide a valid 'id' in the request body.",
                status_code=400
            )

        # Fetch data for the given user ID
        data = get_data(user_id, credential)

        if data:
            first_name = data[0].first_name
            return func.HttpResponse(
                f"The first name of the user with ID {user_id} is: {first_name}",
                status_code=200
            )
        else:
            return func.HttpResponse(
                f"No user found with ID {user_id}.",
                status_code=404
            )

    except Exception as e:
        logging.error(f"Function execution failed: {e}")
        return func.HttpResponse(
            "An error occurred during function execution.",
            status_code=500
        )

if __name__ == "__main__":
    load_dotenv()
    credential = ClientSecretCredential(
        tenant_id=os.getenv('AZURE_TENANT_ID'),
        # client_id=os.getenv('AZURE_CLIENT_ID'),
        # client_secret=os.getenv('AZURE_CLIENT_SECRET')
        client_id='36c5f037-49f2-4c3a-bc6b-c8476ca8446b',
        client_secret='dosef5098c1a6b5a56f3ad6aff262d3c8cf1'
    )

    print(credential._tenant_id)
    print(credential._client_id)    
    print("ahufuhfa")

    response=get_data(7, credential)
    print(response)


    #This one works
    # w = WorkspaceClient(
    #     host          = "https://adb-768728587798803.3.azuredatabricks.net/",
    #     client_id     = "c341771e-e5ce-48ca-8894-f505de398164",
    #     client_secret = "dose319ed5276743c9d049d95c956aa354bc"
    # )

    # # for table in w.tables.list("databricksforapps", "mydatabase"):
    # #     print(f"Cluster Name: {table}")
    
    # response = w.statement_execution.execute_statement("SELECT * FROM mydatabase.mockdata limit 5", "7796604622e5d344")
    # print(response)