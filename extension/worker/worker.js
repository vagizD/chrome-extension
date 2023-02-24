

function getCurrentUrl() {
    return window.location.href
}

function getSelectedWords() {
    const activeTextArea = document.activeElement;
    const selection = activeTextArea.value.substring(
        activeTextArea.selectionStart,
        activeTextArea.selectionEnd
    );
}

