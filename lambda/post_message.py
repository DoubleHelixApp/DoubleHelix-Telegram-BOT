from telegram import Bot
from telegram.ext import ApplicationBuilder
import asyncio

import boto3
from botocore.exceptions import ClientError
import json


def get_secret():

    secret_name = "TelegramBOTAPIKey"
    region_name = "eu-north-1"

    session = boto3.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e

    secret = json.loads(get_secret_value_response["SecretString"])
    return secret["TELEGRAM_TOKEN"]


def handler(event, lambda_context) -> None:
    token = get_secret()
    event = json.loads(event["body"])

    if event["action"] != "prereleased" and event["action"] != "released":
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/plain"},
        }
    if "release" not in event:
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/plain"},
        }
    body = event["release"]["body"]
    version = event["release"]["name"]
    url = event["release"]["html_url"]

    message = (
        f"Hi!\nI'm glad to inform that version [{version}]({url}) of WGSE-NG was released. \U0001F389\U0001F389 "
    )
    message += f"\n\n*Description*:\n"
    message += f"{body}"
    if event["action"] == "prereleased":
        message += "\n\n*NOTE*: This is a pre-release!\n"
    print(message)
    bot = Bot(token)
    asyncio.run(bot.send_message("@DoubleHelixApp", message, parse_mode="markdown"))
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/plain"},
    }


if __name__ == "__main__":
    token = get_secret()
    builder = ApplicationBuilder()
    app = builder.token(token).build()
    app.run_polling()