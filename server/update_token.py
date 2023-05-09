import datetime
import json

import dotenv
import asyncio
import logging
import requests

from logs.logs import logging_config
from config import Config


dotenv.load_dotenv()

logging.basicConfig(**logging_config)
logger = logging.getLogger('update_token')

GET_TOKEN_INTERVAL = 4  # time interval to get new token, hours
GET_TOKEN_URL = "https://iam.api.cloud.yandex.net/iam/v1/tokens"


async def update_token(config: Config):
    while True:

        current_time = datetime.datetime.now()

        # token expired
        if (config.update_time + datetime.timedelta(hours=GET_TOKEN_INTERVAL)) <= current_time:
            logger.info("Updating token...")

            try:

                dotenv_file = dotenv.find_dotenv(raise_error_if_not_found=True)

                new_token = get_token(config)

                dotenv.set_key(dotenv_file, key_to_set="IAM_TOKEN", value_to_set=new_token)
                dotenv.set_key(dotenv_file,
                               key_to_set="UPDATE_TIME",
                               value_to_set=datetime.datetime.strftime(current_time, config.datetime_format))

                config.update_token(new_token, current_time)

            # TODO
            except Exception as e:
                logger.critical("Error while updating token.")
                logger.critical(e)
                raise e

            logger.info("Token updated.")

        else:
            logger.info("Token is active, no update needed.")

        await asyncio.sleep(3600 * GET_TOKEN_INTERVAL)


def get_token(config):
    logger.info("Requesting new token...")

    headers = {"Content-Type": "application/json"}
    payload = {"yandexPassportOauthToken": config.oauth_token}

    response = requests.post(GET_TOKEN_URL, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        logger.info("Successful answer from YC.")

        response_data = json.loads(response.text)
        print(response_data)
        return response_data['iamToken']
    else:
        raise NotImplementedError(f"Error obtaining IAM token: {response.text}.")


def initiate_token_loop(config):
    loop = asyncio.get_event_loop()
    task = loop.create_task(update_token(config))

    try:
        loop.run_until_complete(task)
    except Exception as e:
        logger.critical("Token loop error, closing...")
        task.cancel()
        raise e

