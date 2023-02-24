
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

makeHover = function(e) {
    var target = e.target;

    if (prevDom !== target && target.textContent) {

        if (prevDom != null) {
            prevDom.classList.remove(MVC);
            prevDom.removeChild(prevSpan);
        }

        const span = document.createElement('span');
        span.classList.add('tooltiptext');
        span.appendChild(document.createTextNode("Contains text! Word count: " + getCount(target)));

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
    document.addEventListener('mousemove', makeHover, {once: true})
}, 350)


