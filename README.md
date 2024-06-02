# WGSE-NG Telegram BOT

This is a CDK project that deploy a stack with an API Gateway and a lambda on AWS that is used to send a message in a Telegram group.
The API Gateway endpoint can be added as a webhook to a GitHub project to trigger the notification.
The lambda will process only `released` and `prereleased` actions from GitHub.

The only thing that needs to be configure manually is a secret named `TelegramBOTAPIKey` containing the API Key of the [telegram bot](https://core.telegram.org/bots/tutorial).

Logging from API Gateway is disabled.

Configure and deploy with:
```bash
python -m venv .venv
source .venv/bin/activate # Linux
.venv\Scripts\activate.bat # Windows
pip install -r requirements.txt
cdk bootstrap
$ cdk deploy
```
