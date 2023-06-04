let tg_tag_submit_button = document.querySelector('.tg-tag-submit-button');
let tg_tag = document.querySelector('.tg-tag');

async function postTag() {
    chrome.runtime.sendMessage({type: 'postTag', tag: tg_tag.value});
}

// make action when button is clicked
if(tg_tag_submit_button !== null) {
    tg_tag_submit_button.addEventListener('click', postTag);
}