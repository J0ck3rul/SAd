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

function createNewVersionOption(version) {
    let option = document.createElement("option");
    option.setAttribute('onclick', 'versionSelect(this, event)');
    option.innerHTML = version;
    return option;
}