// ---------------------------------------------
// adds clickble expand button to new links feed
// ---------------------------------------------

var links = document.getElementById("newLinks");

if(links.childElementCount > 5) {
    for(var i = 5; i < links.childElementCount; i++) {
        var link = links.childNodes[i];
        link.classList.add("hiddenLink");
    }
    
    function expandLinks(event) {
        for(var i = 5; i < links.childElementCount; i++) {
            var link = links.childNodes[i];
            link.classList.remove("hiddenLink");
        }
        
        document.getElementById("expandLinksButton").remove();
        
        event.preventDefault();
    }
    
    links.insertAdjacentHTML('afterend', '<a id="expandLinksButton" href="#" role="button" tabindex="0" onclick="expandLinks(event)">...</a>');
}
