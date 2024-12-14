import logging
import azure.functions as func
from databricks import sql
import os
from dotenv import load_dotenv
import json

def get_data(user_id):
    load_dotenv()
    connection = sql.connect(
                            server_hostname = "adb-768728587798803.3.azuredatabricks.net",
                            http_path = "/sql/1.0/warehouses/7796604622e5d344",
                            access_token = os.getenv('DATABRICKS_ACCESS_TOKEN'),
                            timeout = 10)

    cursor = connection.cursor()

    query = "SELECT * FROM mydatabase.mockdata WHERE id = ?"
    cursor.execute(query, (user_id,))
    data= cursor.fetchall()

    cursor.close()
    connection.close()
    return data
import logging
import azure.functions as func

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
        data = get_data(user_id)

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
    req = func.HttpRequest(
        method='POST',
        url='/api/test',
        headers={},
        params={'id': '3'},  # Simulate query parameters
        body=json.dumps({"id": "3"}).encode('utf-8')  # Simulate request body
    )

    response=main(req)
    print(response.get_body())  # Print the HTTP response object
    print(response.get_body().decode())  # Print the HTTP response body