import json
import logging
import os

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

data_for_dict = {
    "key": os.getenv("DICT_API"),
    "lang": "en-ru",
    "text": "",
}

header_for_dict = {
    "Content-Type": "application/json",
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

    dict_response = json.loads(response.text)
    data_for_dict["text"] = data["word"]
    extra_info = requests.post(f'https://dictionary.yandex.net/api/v1/dicservice.json/lookup',
                               data=data_for_dict)

    extra_info_response = json.loads(extra_info.text)

    texts.pop(0)
    other_trans = dict()

    for j in range(len(extra_info_response["def"])):
        for i in range(min(2, len(extra_info_response["def"][j]["tr"]))):
            if extra_info_response["def"][j]["tr"][i]["pos"] in other_trans.keys():
                other_trans[extra_info_response["def"][j]["tr"][i]["pos"]].append(extra_info_response["def"][j]["tr"][i]["text"])
            else:
                other_trans[extra_info_response["def"][j]["tr"][i]["pos"]] = [extra_info_response["def"][j]["tr"][i]["text"]]
    print(other_trans)

    if dict_response.get("translations", None) is not None:
        data.update({"translation": dict_response['translations'][0]['text']})
        data.update({"extras": other_trans})
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
