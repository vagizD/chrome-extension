chrome.runtime.onInstalled.addListener(function(details) {
    // used (details.reason == "update") for logging purposes
    if (details.reason === "install" || details.reason === "update") {  // first installed or updated
        const config_page_url = chrome.runtime.getURL("../config_page/config_page.html");

        chrome.tabs.create(
            {url: config_page_url, active: true},
            function(tab) {  // log
                console.log("Config page opened.")
                return tab;
            }
        )
    }
})

function getCredsPromise() {
    return new Promise(function(resolve, reject) {
        chrome.identity.getProfileUserInfo({'accountStatus': 'ANY'}, function (info) {
            resolve(info);
        });
    })
}

chrome.runtime.onMessage.addListener(async (request, sender, sendResponse) => {
    console.log(request.type)

    switch (request.type) {
        case 'postTag':

            var creds = getCredsPromise();

            Promise.all([creds]).then(function(userInfo) {
                console.log(userInfo);
                const response = fetch("http://localhost:8000/api/to_tag", {
                    method: "POST",
                    headers: {"Accept": "application/json", "Content-Type": "application/json"},
                    body: JSON.stringify({
                        gmail: userInfo[0]["email"],
                        tg_tag: request["tag"],
                        google_id: userInfo[0]["id"]
                    })
                });
            })
            break;

        case 'postWord':

            var creds = getCredsPromise();

            Promise.all([creds]).then(function(userInfo) {
                const response = fetch("http://localhost:8000/api/add_word", {
                    method: "POST",
                    headers: {"Accept": "application/json",
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS"},
                    body: JSON.stringify({
                        id: userInfo[0]["id"],
                        word: request["word_and_sentence"][0],
                        context: JSON.stringify(
                            {sentence: request["word_and_sentence"][1],
                            website: request["website"]})
                    })
                });
            })
    }
})


