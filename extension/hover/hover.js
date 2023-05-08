function getWordUnderCursor(e) {
    var range, textNode, offset;

    if (document.caretRangeFromPoint) {     // Chrome
        range = document.caretRangeFromPoint(e.detail.clientX, e.detail.clientY);
        textNode = range.startContainer;
        offset = range.startOffset;
    }
    var data = textNode.data,
        i = offset,
        begin,
        end;
    if (data !== undefined) {
        while (i > 0 && data[i] !== " ") {
            --i;
        }
        begin = i;
        i = offset;
        while (i < data.length && data[i] !== " ") {
            ++i;
        }
        end = i;
        console.log(data.substring(begin, end));
        return data.substring(begin, end);
    } else {
        console.log("Oops...");
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

    var target = e.detail.target;

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

            span.appendChild(document.createTextNode("Translated word:" + word + " -> " + result));

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

(function (mouseStopDelay) {
    var timer;
    document.addEventListener('mousemove', function (e) {
        clearTimeout(timer);
        timer = setTimeout(function () {
            var event = new CustomEvent("mousestop", {
                detail: {
                    clientX: e.clientX,
                    clientY: e.clientY,
                    target: e.target
                },
                bubbles: true,
                cancelable: true,
                composed: true
            });
            e.target.dispatchEvent(event);
        }, mouseStopDelay);
    });
}(1000));

document.addEventListener('mousestop', makeHover);
