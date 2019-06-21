function setAjaxHeaders(ajaxHttp) {
    ajaxHttp.setRequestHeader("content-type", "application/json");
}

function createPackageDetails(package, versionList) {
    console.log(versionList);
    var expandable = document.createElement("div");
    expandable.classList.add("expandable");

    let id = document.createElement("p");
    id.innerHTML = package["_id"];
    id.style.display = "none";

    let description = document.createElement("p");
    description.innerHTML = package["description"];

    let versionContainer = document.createElement("p");

    let versionValue = document.createElement("span");
    let versionText = document.createElement("span");

    versionText.innerHTML = "version: ";
    versionValue.innerHTML = package["version"];

    versionContainer.appendChild(versionText);
    versionContainer.appendChild(versionValue);

    let architectureContainer = document.createElement("p");

    let architectureValue = document.createElement("span");
    let architectureText = document.createElement("span");

    architectureText.innerHTML = "architecture: ";
    architectureValue.innerHTML = package["architecture"];

    architectureContainer.appendChild(architectureText);
    architectureContainer.appendChild(architectureValue);

    let maintainer = document.createElement("p");
    maintainer.innerHTML = "maintainter: " + package["maintainer"];

    let selectButton = document.createElement("button");
    selectButton.setAttribute("onclick", "selectPackage(this, event)");
    let idValue = package["_id"];


    let isAlreadySelected = selectedPackages.indexOf(idValue);

    if (isAlreadySelected !== -1) {
        selectButton.classList.toggle("selected");
        selectButton.innerHTML = "Deselect";
    }
    else {
        selectButton.innerHTML = "Select";
    }

    let selectVersion = document.createElement("select");
    selectVersion.setAttribute("onclick", "selectClick(this,event)")
    selectVersion.setAttribute("id", "versionSelect");
    selectVersion.style.display = "block";

    let baseVersionOption = document.createElement("option");
    baseVersionOption.innerHTML = "select a different version";
    // baseVersionOption.disabled = true;
    baseVersionOption.selected = 'selected';

    selectVersion.appendChild(baseVersionOption);



    versionList.forEach(version=>{
        selectVersion.appendChild(createNewVersionOption(version));
    })

    expandable.appendChild(id)
    expandable.appendChild(description);
    expandable.appendChild(versionContainer);
    expandable.appendChild(architectureContainer);
    expandable.appendChild(maintainer);
    expandable.appendChild(selectButton);
    expandable.appendChild(selectVersion);

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