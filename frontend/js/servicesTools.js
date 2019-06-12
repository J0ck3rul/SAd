function setAjaxHeaders(ajaxHttp) {
    ajaxHttp.setRequestHeader("content-type", "application/json");
    ajaxHttp.setRequestHeader("Access-Control-Allow-Methods", "*");
    ajaxHttp.setRequestHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    ajaxHttp.setRequestHeader('Access-Control-Allow-Credentials', 'true');
    ajaxHttp.setRequestHeader('Access-Control-Allow-Origin', '*');
}

function createItemForPackageList(package) {
    let section = document.createElement("section");
    section.classList.add("package");
    section.setAttribute("onclick", "expandPackage(this);");

    let name = document.createElement("h2");
    name.innerHTML = package["_name"];

    var expandable = document.createElement("div");
    expandable.classList.add("expandable");

    let id = document.createElement("p");
    id.innerHTML = package["_id"];
    id.style.display = "none";

    let description = document.createElement("p");
    description.innerHTML = package["_description"];

    let version = document.createElement("p");
    version.innerHTML = "version: " + package["_version"];

    let maintainer = document.createElement("p");
    maintainer.innerHTML = "maintainter: " + package["_maintainer"];

    let selectButton = document.createElement("button");
    selectButton.setAttribute("onclick", "selectPackage(this, event");


    let selectVersion = document.createElement("select");

    let baseOption = document.createElement("option");
    baseOption.innerHTML = "select a different version";
    baseOption.disabled = true;

    selectVersion.appendChild(baseOption);
    expandable.appendChild(id)
    expandable.appendChild(description);
    expandable.appendChild(version);
    expandable.appendChild(maintainer);
    expandable.appendChild(selectButton);
    expandable.appendChild(selectVersion);

    section.appendChild(name);
    section.appendChild(expandable);

    return section;
}