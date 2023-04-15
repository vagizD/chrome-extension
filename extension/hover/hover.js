function getWordUnderCursor(e) {
    var range, textNode, offset;

    if (document.caretRangeFromPoint) {     // Chrome
        range = document.caretRangeFromPoint(e.clientX, e.clientY);
        textNode = range.startContainer;
        offset = range.startOffset;
    }
    var data = textNode.data,
        i = offset,
        begin,
        end;
    if(data !== undefined) {
        while (i > 0 && data[i] !== " ") {
            --i;
        }
        begin = i;
        i = offset;
        while (i < data.length && data[i] !== " ") {
            ++i;
        }
        end = i;

        return data.substring(begin, end);
    }
    else {
        return "Oops..."
    }
}
function getWords() {
    var selected = window.getSelection()
    if(selected.rangeCount > 0) {
        var range = selected.getRangeAt(0).cloneRange()

        if (range.startOffset === range.endOffset) {
            let startWord;
            let endWord;
            startWord = (r) => r.toString().match(/^\s/)
            endWord = (r) => r.toString().match(/\s$/)

            while (!startWord(range) && range.startOffset > 0) {
                range.setStart(range.startContainer, range.startOffset - 1)
            }
            if (startWord(range)) range.setStart(range.startContainer, range.startOffset + 1)

            var length = range.endContainer.length || range.endContainer.childNodes.length
            while (!endWord(range) && range.endOffset < length) {
                range.setEnd(range.endContainer, range.endOffset + 1)
            }
            if (endWord(range) && range.endOffset > 0) range.setEnd(range.endContainer, range.endOffset - 1)

        }
        return range.toString()
    }
    else {
        return "Oops..."
    }
}

async function postTranslation(line){
    const response = await fetch("http://localhost:8000/api/totrans", {
        method: "POST",
        headers: {"Accept": "application/json", "Content-Type": "application/json"},
        body: JSON.stringify({
            word: line
        })
    });
    if(response.ok === true) {
        const new_word = await response.json();
        console.log(new_word["word"].toString())
        return new_word["word"];
    }
    else {
        const error = await response.json();
        console.log(error.message)
    }
}

function getText(el) {
    let ret = "";
    var length = el.childNodes.length;
    for(var i = 0; i < length; i++) {
        var node = el.childNodes[i];
        if(node.nodeType !== 8) {
            ret += node.nodeType !== 1 ? node.nodeValue : getText(node);
        }
    }
    return ret;
}

function getCount(el) {
    var words = getText(el);
    return words.split(' ').length;
}

var makeHover = async function(e) {

    var target = e.target;

    if (target.textContent) {

        if (prevDom !== null) {
            console.log(prevDom);
            console.log(prevDom.className)
            prevDom.classList.remove(MVC);
            prevDom.removeChild(prevSpan);
        }

        const span = await document.createElement('span');
        span.classList.add('tooltiptext');
        var word = await getWordUnderCursor(e);
        var result = await postTranslation(word);
        if (result !== 'Oops...') {

            span.appendChild(document.createTextNode("Word was founded: " + result));

            target.classList.add(MVC);
            target.appendChild(span);

            prevDom = target;
            prevSpan = span;

        }
    }
}



var MVC = 'tooltip';

var prevDom = null;
var prevSpan = null;

setInterval(() => {
    document.addEventListener('click', makeHover, {once: true})
}, 0)


