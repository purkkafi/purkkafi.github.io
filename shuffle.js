// -------------------------------------------
// shuffles children of div with id "shuffle"
// ------------------------------------------

const parent = document.querySelector('#shuffle');
const children = Array.from(parent.children);

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

shuffleArray(children);

for(index in children){
    var child = children[index];
    parent.appendChild(child);
}
