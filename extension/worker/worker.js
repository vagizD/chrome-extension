chrome.runtime.onInstalled.addListener(function(details) {
    // used (details.reason == "update") for logging purposes
    if (details.reason === "install" || details.reason === "update") {  // first installed or updated
        const config_page_url = chrome.runtime.getURL("../config_page/config_page.html");

        chrome.tabs.create(
            {url: config_page_url, active: true},
            function(tab) {  // log
                console.log("Config page opened.")
            }
        )
    }
})