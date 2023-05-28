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
        end,
        big_begin,
        big_end;
    if ((typeof data) === "string") {
        console.log(data);
        while (i > 0 && data[i] !== " ") {
            --i;
            //console.log(data[i])
        }
        begin = i;
        big_begin = begin+1;

        i = offset;
        while (i < data.length && data[i] !== " ") {
            ++i;
        }
        end = i;
        big_end = end-1;

        if(data[begin] === " ") {
            begin++;
        }
        var code = data.charCodeAt(big_begin);
        while (big_begin >= 0){
            if(((code >= 33 && code <= 47) || (code >= 58 && code <= 64) || (code <= 95 && code >= 91) || (code <= 126 && code >= 123)) && (code !== 39 || code !== 45)){
                big_begin++;
                break;
            }
            big_begin--;
            code = data.charCodeAt(big_begin);
        }
        code = data.charCodeAt(big_end);
        while (big_end < data.length){
            if(((code >= 33 && code <= 47) || (code >= 58 && code <= 64) || (code <= 95 && code >= 91) || (code <= 126 && code >= 123)) && (code !== 39 || code !== 45)){
                break
            }
            //console.log(code);
            big_end++;
            code = data.charCodeAt(big_end);
        }
        var context = data.substring(big_begin, big_end).toString();
        context = context.trim();
        console.log(context);
        var result = data.substring(begin, end).toString();
        var j = 0;
        begin = 0;
        i = result.length;
        end = result.length;
        while (j < i){
            var code_front = result.charCodeAt(j);
            var code_back = result.charCodeAt(i);
            if(((code_front <= 64 && code_front >= 33) || (code_front <= 95 && code_front >= 91) || (code_front <= 126 && code_front >= 123)) && (code_front !== 39 || code_front !== 45)){
                begin = ++j;
            }
            else{
                ++j;
            }
            if(((code_back <= 64 && code_back >= 33) || (code_back <= 95 && code_back >= 91) || (code_back <= 126 && code_back >= 123)) && (code_back !== 39 || code_back !== 45)){
                end = i--;
            }
            else{
                i--;
            }
        }
        result = result.substring(begin, end).trim();
        console.log(result);
        return [result, context];
    } else {
        console.log("Oops...");
        return ["Oops...", "Oops..."]
    }
}

async function postTranslation(line){
    const response = await fetch("http://localhost:8000/api/totrans", {
        method: "POST",
        headers: {"Accept": "application/json", "Content-Type": "application/json", "Access-Control-Allow-Origin": "*", 'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'},
        body: JSON.stringify({
            word: line[0],
            context: line[1]
        })
    });
    if(response.ok === true) {
        const new_word = await response.json();
        console.log(new_word["translation"].toString())
        return new_word["translation"];
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

        var word_and_sentence = await getWordUnderCursor(e);

        if (word_and_sentence[0] !== 'Oops...' && word_and_sentence[0].length > 0) {

            if (prevDom !== null && prevSpan !== null) {
                console.log(prevDom);
                console.log(prevDom.className)
                prevDom.classList.remove(MVC);
                prevDom.removeChild(prevSpan);
            }

            const span = await document.createElement('span');
            span.classList.add('tooltiptext');

            span.style.left = `${e.detail.clientX+10}px`;
            span.style.top = `${e.detail.clientY+10}px`;

            var result = await postTranslation(word_and_sentence);
            span.appendChild(document.createTextNode("Translated word: " + word_and_sentence[0] + " -> " + result));

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
                    pageX: e.pageX,
                    pageY: e.pageY,
                    offsetX: e.offsetX,
                    offsetY: e.offsetY,
                    screenX: e.screenX,
                    screenY: e.screenY,
                    target: e.target,
                    x: e.x,
                    y: e.y
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