
function searchPackages() {
    let ajaxHttp = new XMLHttpRequest({ mozSystem: true });
    let url = baseURL + '/search';

    ajaxHttp.open("GET", url, true);

    setAjaxHeaders(ajaxHttp);

    let searchText = document.getElementsByClassName("search-field");
    let serachTextLength = searchText[0].textLength;
    let minimumTextLength = 4;
    if(serachTextLength < minimumTextLength)
        {
            alert("minimum "+ minimumTextLength + " characters");
            return ;
        }
    ajaxHttp.onreadystatechange = function () {
        var obj = JSON.parse(ajaxHttp.response)

        let packageList = obj["package_list"];
        let htmlPackageList = document.getElementsByClassName("package-list")[0];
        htmlPackageList.innerHTML = '';

        packageList.forEach(package => {
            packageNode = createItemForPackageList(package);
            htmlPackageList.appendChild(packageNode);
        });
    }
    ajaxHttp.send();
}

async function setVersions(packageContainer) {

    let id = packageContainer.childNodes[1].childNodes[0].textContent;
    let versionSelector = packageContainer.childNodes[1].childNodes[5];
    let url = baseURL + '/getVersions?id=' + id;

    if (versionDictionary[id] === undefined)
        await requestAndUpdateVersions(url, versionSelector, id);
    else
        UpdateVersions(versionSelector, id);
}

function versionSelect(elem, event) {
    event.stopPropagation();
    let version = elem.value;
    let id = elem.parentElement.parentElement.childNodes[0].textContent;
    let packageSection = elem.parentElement.parentElement.parentElement;

    let url = baseURL + '/getPackage?id=' + id + '&version=' + version;

    let ajaxHttp = new XMLHttpRequest({ mozSystem: true });
    ajaxHttp.open("GET", url, true);
    setAjaxHeaders(ajaxHttp);

    ajaxHttp.onreadystatechange = () => {
        var package = JSON.parse(ajaxHttp.response)

        packageSection.innerHTML = createItemForPackageList(package).innerHTML;
        packageSection.childNodes[1].style.display = "block";

        let versionSelector = getElementByIdFromParent("versionSelect", "select", packageSection)

        UpdateVersions(versionSelector, id);
    }
    ajaxHttp.send();
}



function Checkout() {
    let wantedPackeges = { "packages": selectedPackages };

    let url = baseURL + '/checkout';
    let ajaxHttp = new XMLHttpRequest({ mozSystem: true });
    ajaxHttp.open("POST", url, true);
    setAjaxHeaders(ajaxHttp);

    ajaxHttp.onreadystatechange = () => {
        console.log(ajaxHttp.response);
    }
    ajaxHttp.send(JSON.stringify(wantedPackeges));
}
