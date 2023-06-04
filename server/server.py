import json
import logging
import requests
import uvicorn
import multiprocessing

from update_token import initiate_token_loop
from logs.logs import logging_config
from config import config

from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

from queries import process_tag, process_word

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


@app.post("/api/to_trans")
def transRequest(data=Body()):
    logger.debug("New translation request.")

    texts.append(data["word"])
    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                             json=body,
                             headers=config.headers)
    texts.pop(0)
    dict_response = json.loads(response.text)

    if dict_response.get("translations", None) is not None:
        data.update({"translation": dict_response['translations'][0]['text']})
    else:
        data.update({"translation": "No translation found."})

    return data


@app.post("/api/to_tag")
def tagRequest(data=Body()):
    logger.debug(f"New tag request.")

    status = process_tag(data)

    return {"status": status}


@app.post("/api/add_word")
def addWord(data=Body()):
    data["context"] = json.loads(data["context"])

    status = process_word(data)

    print(data)
    return {"status": status}


if __name__ == '__main__':
    logger.info("Initiating token loop...")
    token_updater = multiprocessing.Process(target=initiate_token_loop, args=(config,))
    token_updater.start()
    logger.info("Token loop initiated.")

    logger.info("Launching server...")
    server = multiprocessing.Process(target=uvicorn.run, kwargs={"app": "server:app", "reload": True})
    server.start()
    logger.info("Server launched.")
