let tg_tag_submit_button = document.querySelector('.tg-tag-submit-button');
let tg_tag = document.querySelector('.tg-tag');

// get user's credentials
let email = null;
let id = null;
chrome.identity.getProfileUserInfo({'accountStatus': 'ANY'}, function (info) {
    console.log(info);  // log
    email = info['email'];
    id = info['id'];
})

// request to update info about user
async function postTag() {
    const response = await fetch("http://localhost:8000/api/totag", {
        method: "POST",
        headers: {"Accept": "application/json", "Content-Type": "application/json"},
        body: JSON.stringify({
            tg_tag: tg_tag.value,
            email: email,
            id: id
        })
    });
    // logs
    if(response.ok === true) {
        const new_word = await response.json();
        return new_word["word"];
    }
    else {
        const error = await response.json();
        console.log(error.message)
    }
    // logs
}

// make action when button is clicked
if(tg_tag_submit_button !== null) {
    tg_tag_submit_button.addEventListener('click', postTag);
}