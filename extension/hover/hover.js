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

var makeHover = function(e) {
    var target = e.target;

    if (target.textContent) {

        if (prevDom != null) {
            prevDom.classList.remove(MVC);
            prevDom.removeChild(prevSpan);
        }

        const span = document.createElement('span');
        span.classList.add('tooltiptext');
        span.appendChild(document.createTextNode("Word was founded: " + getWords()));

        target.classList.add(MVC);
        target.appendChild(span)

        prevDom = target;
        prevSpan = span;
    }
}

var MVC = 'tooltip';

var prevDom = null;
var prevSpan = null;

setInterval(() => {
    document.addEventListener('click', makeHover, {once: true})
}, 0)


