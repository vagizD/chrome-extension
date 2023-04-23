let form = document.querySelector('.subscription');
let tag = document.querySelector('.subscription-tag');
async function postTag(tag, email){
    const response = await fetch("http://localhost:8000/api/totag", {
        method: "POST",
        headers: {"Accept": "application/json", "Content-Type": "application/json"},
        body: JSON.stringify({
            tag_word: tag,
            email_word: email
        })
    });
    if(response.ok === true) {
        const new_word = await response.json();
        return new_word["word"];
    }
    else {
        const error = await response.json();
        console.log(error.message)
    }
}

let email = null;
chrome.identity.getProfileUserInfo({'accountStatus': 'ANY'}, function (info){
    console.log(info);
    document.querySelector('textarea').value = JSON.stringify(info);
    email = info['email'];
})

console.log(tag);
if(form !== null) {
    form.onsubmit = function () {
        postTag(tag.value, email);
    }
}