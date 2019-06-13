function setAjaxHeaders(ajaxHttp) {
    ajaxHttp.setRequestHeader("content-type", "application/json");
    ajaxHttp.setRequestHeader("Access-Control-Allow-Methods", "*");
    ajaxHttp.setRequestHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    ajaxHttp.setRequestHeader('Access-Control-Allow-Credentials', 'true');
    ajaxHttp.setRequestHeader('Access-Control-Allow-Origin', '*');
}

function createPackeDetails(package) {

    var expandable = document.createElement("div");
    expandable.classList.add("expandable");

    let id = document.createElement("p");
    id.innerHTML = package["_id"];
    id.style.display = "none";

    let description = document.createElement("p");
    description.innerHTML = package["_description"];

    let versionContainer = document.createElement("p");

    let versionValue = document.createElement("span");
    let versionText = document.createElement("span");

    versionText.innerHTML = "version: ";
    versionValue.innerHTML = package["_version"];

    versionContainer.appendChild(versionText);
    versionContainer.appendChild(versionValue);

    let maintainer = document.createElement("p");
    maintainer.innerHTML = "maintainter: " + package["_maintainer"];

    let selectButton = document.createElement("button");
    selectButton.setAttribute("onclick", "selectPackage(this, event)");
    let idValue = package["_id"];


    let isAlreadySelected = selectedPackages.indexOf(idValue);

    if (isAlreadySelected !== -1) {
        selectButton.classList.toggle("selected");
        selectButton.innerHTML = "Deselect";
    }
    else {
        // selectButton.classList.toggle("selected");
        selectButton.innerHTML = "Select";
    }

    let selectVersion = document.createElement("select");
    selectVersion.setAttribute("onclick", "stopPropagation(event)")
    selectVersion.setAttribute("id", "versionSelect");
    selectVersion.style.display = "block";

    let baseVersionOption = document.createElement("option");
    baseVersionOption.innerHTML = "select a different version";
    // baseVersionOption.disabled = true;
    baseVersionOption.selected = 'selected';


    let selectArhitecture = document.createElement("select");
    selectArhitecture.setAttribute("onclick", "stopPropagation(event)");
    selectArhitecture.setAttribute("id", "arhitectureSelect");
    selectArhitecture.style.display = "block";

    let baseArhitectureOption = document.createElement("option");
    let architectureVersion = package["_architecture"];
    baseArhitectureOption.innerHTML = architectureVersion;
    baseArhitectureOption.selected = "selected";

  
    selectVersion.appendChild(baseVersionOption);
    selectArhitecture.appendChild(baseArhitectureOption);
    expandable.appendChild(id)
    expandable.appendChild(description);
    expandable.appendChild(versionContainer);
    expandable.appendChild(maintainer);
    expandable.appendChild(selectButton);
    expandable.appendChild(selectVersion);
    expandable.appendChild(selectArhitecture);

    return expandable;
}

function createItemForPackageList(name) {
    let section = document.createElement("section");
    section.classList.add("package");
    section.setAttribute("onclick", "expandPackage(this);");

    let nameField = document.createElement("h2");
    nameField.innerHTML = name;

    var expandable = document.createElement("div");
    expandable.classList.add("expandable");



    section.appendChild(nameField);
    section.appendChild(expandable);

    return section;
}

function getElementByIdFromParent(elementId, elementName, parent) {
    list = parent.getElementsByTagName(elementName);
    let searchedElement;
    for (let i = 0; i < list.length; i++) {
        if (list[i].id === elementId)
            searchedElement = list[i];
    }
    return searchedElement;
}

function serachInPackageList(object) {
    let isFound = false;
    selectedPackages.forEach(package => {
        if (package.id === object.id)
            if (package.version === object.version)
                isFound = true;
    })

    return isFound;
}
function getIndexOfSelectedPackage(object) {
    for (let i = 0; i < selectedPackages.length; i++) {
        if ((object.id === selectedPackages[i].id))
            if (object.version === selectedPackages[i].version)
                return i;
    }
    return 0;
}
function stopPropagation(event) {
    event.stopPropagation();
}