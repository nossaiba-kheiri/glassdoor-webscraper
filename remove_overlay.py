def get_overlay_removal_script():
    """
    Returns the JavaScript code to remove the Glassdoor overlay.
    """
    return """
    function addGlobalStyle(css) {
        var head, style;
        head = document.getElementsByTagName('head')[0];
        if (!head) { return; }
        style = document.createElement('style');
        style.type = 'text/css';
        style.innerHTML = css;
        head.appendChild(style);
    }

    addGlobalStyle("#HardsellOverlay {display:none !important;}");
    addGlobalStyle("body {overflow:auto !important; position: initial !important}");

    window.addEventListener("scroll", event => event.stopPropagation(), true);
    window.addEventListener("mousemove", event => event.stopPropagation(), true);
    """