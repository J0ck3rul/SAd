function searchPackages() {
    let searchText = document.getElementsByClassName("search-field")[0].value;
    let htmlPackageList = document.getElementsByClassName("package-list")[0];
    htmlPackageList.innerHTML = '';

    let container = document.createElement("div");
    container.classList.add("container");

    loadingContainer = document.createElement("div");
    loadingContainer.classList.add("loading");
    loadingText = document.createElement("span");
    loadingText.innerHTML = "Loading";

    loadingContainer.appendChild(loadingText);
    container.appendChild(loadingContainer);
    htmlPackageList.appendChild(container);

    let url = baseURL + '/search/' + searchText;



    let ajaxHttp = new XMLHttpRequest({ mozSystem: true });

    ajaxHttp.open("GET", url, true);
    setAjaxHeaders(ajaxHttp);

    let serachTextLength = searchText[0].textLength;
    if (serachTextLength < minimumTextLength) {
        alert("minimum " + minimumTextLength + " characters");
        return;
    }

    ajaxHttp.onreadystatechange = function () {
        var obj = JSON.parse(ajaxHttp.response)
        let packageList = obj;

        htmlPackageList.innerHTML = '';

        packageList.forEach(package => {
            packageNode = createItemForPackageList(package);
            htmlPackageList.appendChild(packageNode);
        });
    }
    ajaxHttp.send();
}


async function getPackageProperties(packageContainer) {

    let name = packageContainer.childNodes[0].textContent;

    let url = baseURL + '/package/' + name;

    let ajaxHttp = new XMLHttpRequest({ mozSystem: true });

    ajaxHttp.open("GET", url, true);
    setAjaxHeaders(ajaxHttp);

    ajaxHttp.onreadystatechange = function () {
        var obj = JSON.parse(ajaxHttp.response)

        let versionList = [];

        obj.forEach(function (package, index) {
            versionList.push({ "version": package["version"], "architecture": package["architecture"] });
        });


        versionDictionary[obj[0]["name"]] = versionList;

        let packageDetails = createPackageDetails(obj[0], versionList);

        packageContainer.childNodes[1].innerHTML = packageDetails.innerHTML;


        // let packageList = obj;
        // let htmlPackageList = document.getElementsByClassName("package-list")[0];
        // htmlPackageList.innerHTML = '';

        // packageList.forEach(package => {
        //     packageNode = createItemForPackageList(package);
        //     htmlPackageList.appendChild(packageNode);
        // });
    }
    ajaxHttp.send();
}


function versionSelect(elem, event) {
    event.stopPropagation();


    let packageSection = elem.parentNode.parentNode.parentNode;

    let sepIndex = elem.value.indexOf(" - ");
    let version = elem.value.substr(0, sepIndex);
    let architecture = elem.value.substr(sepIndex + 3, 15);
    let name = elem.parentNode.parentNode.parentNode.childNodes[0].textContent;



    let url = baseURL + '/getPackage/' + name + '/' + version + '/' + architecture;
    let ajaxHttp = new XMLHttpRequest({ mozSystem: true });
    ajaxHttp.open("GET", url, true);
    setAjaxHeaders(ajaxHttp);

    ajaxHttp.onreadystatechange = () => {
        let versionList = [];
        var package = JSON.parse(ajaxHttp.response)
        versionList = versionDictionary[package["_name"]];
        packageSection.childNodes[1].innerHTML = createPackageDetails(package, versionList).innerHTML;
    }
    ajaxHttp.send();
}


function Checkout() {
    let wantedPackages = { "packages": selectedPackages };
    let url = baseURL + '/install/' + selectedPackages.join(",");
    window.location.href = baseURL + '/install/' + selectedPackages.join(",")
}


function selectClick(elem, event) {
    elem.childNodes[0].disabled = true;
    event.stopPropagation();
}