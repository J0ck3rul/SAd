async function requestAndUpdateVersions(requestURL, versionSelector, id) {
    let ajaxHttp = new XMLHttpRequest({ mozSystem: true });
    ajaxHttp.open("GET", requestURL, true);
    
        

    ajaxHttp.onreadystatechange = function () {
        let versionsList = JSON.parse(ajaxHttp.response)

        versionDictionary[id] = versionsList;

        AddOptionsToHTMLVersionsSelector(versionSelector, versionsList)
    }
    ajaxHttp.send();
}
function AddOptionsToHTMLVersionsSelector(selector, optionsList) {
    selector.innerHTML = '';
    let baseOption = document.createElement("option");
    baseOption.innerHTML = "select a different version";
    baseOption.disabled = true;
    baseOption.selected = 'selected';

    selector.appendChild(baseOption);

    optionsList.forEach(version => {
        let option = createNewVersionOption(version);
        selector.appendChild(option);
    });
}

function UpdateVersions(versionSelector, id) {
    let versionsList = versionDictionary[id];
    AddOptionsToHTMLVersionsSelector(versionSelector, versionsList)
}

function createNewVersionOption(versionObject) {
    let option = document.createElement("option");
    option.setAttribute('onclick', 'versionSelect(this, event)');
    
    let version = document.createElement("span");
    let separator = document.createElement("span");
    let architecture = document.createElement("span");
    version.innerHTML = versionObject["version"];
    architecture.innerHTML = versionObject["architecture"];
    separator.innerHTML = " - "
    // option.innerHTML = version;
    option.appendChild(version);
    option.appendChild(separator);
    option.appendChild(architecture);
    return option;
}