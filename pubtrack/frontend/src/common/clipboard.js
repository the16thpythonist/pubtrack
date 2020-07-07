
function selectText(element) {
    var range;

    // This is the interface to selections for IE (Internet explorer)
    if (document.selection) {
        range = document.body.createTextRange();
        range.moveToElementText(element);
        range.select();
    }
    // For everything newer
    else if (window.getSelection) {
        range = document.createRange();
        range.selectNode(element);
        // Removing all selections, which are already present and might interfere
        window.getSelection().removeAllRanges();
        window.getSelection().addRange(range);
    }
}

function unselectText() {
    if (document.selection) {
        // Removing the selection after it is done
        document.selection.empty();
    } else if (window.getSelection) {
        window.getSelection().removeAllRanges();
    }
}

export function copyClipboard(element) {
    selectText(element);
    document.execCommand('copy');
    unselectText();
}