async function selectPackage(elem, event) {
    event.stopPropagation();

    let id = elem.parentElement.childNodes[0].textContent;

    if (elem.classList.contains("selected")) {
        elem.classList.toggle("selected");
        elem.innerText = "Select";
        removePackage(id);
    }
    else {
        elem.classList.toggle("selected");
        elem.innerText = "Deselect";
        addPackage(id);
    }
}

function addPackage(id) {
    selectedPackages.push(id);
}
function removePackage(pkg) {
    selectedPackages = selectedPackages.filter(function (package) {
        return package != pkg;
    })
}
function Reset() {
    selectedPackages = [];
    selectButtons = document.getElementsByClassName("selected");
    while(selectButtons.length > 0) {
        button = selectButtons[selectButtons.length-1];
        button.classList.toggle("selected");
        button.innerHTML = "Select";
    }
}