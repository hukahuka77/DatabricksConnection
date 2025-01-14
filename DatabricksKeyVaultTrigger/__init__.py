import os
import logging
from datetime import datetime, timezone
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import azure.functions as func
from dotenv import load_dotenv


def main(mytimer: func.TimerRequest) -> None:
    logging.info('Python timer trigger function executed at %s', datetime.now(timezone.utc))

    load_dotenv()
    # Load configuration from environment variables
    keyvault_url = os.getenv("DB_KEYVAULT_URL")
    keyvault_secret_name = os.getenv("DB_KEYVAULT_SECRET_NAME")

    if not keyvault_secret_name:
        logging.error("DB_KEYVAULT_SECRET_NAME is not set in environment variables.")
        return

    # Initialize SecretClient with DefaultAzureCredential
    try:
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=keyvault_url, credential=credential)

        # Get the secret from Key Vault
        secret = client.get_secret(keyvault_secret_name)
        print(f"Secret Value retrieved from Key Vault: {secret.value}")
    except Exception as e:
        logging.error(f"Error accessing Key Vault: {str(e)}")

if __name__ == "__main__":
    main(None)