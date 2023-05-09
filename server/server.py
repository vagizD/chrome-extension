import json
import logging
import requests
import uvicorn
import multiprocessing

from dotenv import load_dotenv
from update_token import initiate_token_loop
from logs.logs import logging_config
from config import config
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

logging.basicConfig(**logging_config)
logger = logging.getLogger('server')

app = FastAPI()

texts = []

body = {
    "targetLanguageCode": config.target_language,
    "texts": texts,
    "folderId": config.folder_id,
}

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/gettrans")
def transResponse(data=Body()):
    ...


@app.post("/api/totrans")
def transRequest(data=Body()):
    texts.append(data["word"])
    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                             json=body,
                             headers=config.headers)
    texts.pop(0)
    dict_response = json.loads(response.text)
    data["word"] = dict_response['translations'][0]['text']

    print(data)

    return data


@app.post("/api/totag")
def tagRequest(data=Body()):
    print(data)
    return data


if __name__ == '__main__':
    logger.info("Initiating token loop...")
    token_updater = multiprocessing.Process(target=initiate_token_loop, args=(config,))
    token_updater.start()
    logger.info("Token loop initiated.")

    logger.info("Launching server...")
    server = multiprocessing.Process(target=uvicorn.run, kwargs={"app": "server:app", "reload": True})
    server.start()
    logger.info("Server launched.")
