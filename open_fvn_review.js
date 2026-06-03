// ----------------------------------------------
// opens the corresponding fvn review when linked
// ----------------------------------------------

var hash = location.hash

if(hash != "") {
    var review = document.querySelector(hash + ' ~ .review')
    review.open = true
}
