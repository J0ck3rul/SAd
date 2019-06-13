
function searchPackages() {
    let url = baseURL + '/search';
    let minimumTextLength = 4;


    let ajaxHttp = new XMLHttpRequest({ mozSystem: true });

    ajaxHttp.open("GET", url, true);
    setAjaxHeaders(ajaxHttp);

    let searchText = document.getElementsByClassName("search-field");
    let serachTextLength = searchText[0].textLength;
    if (serachTextLength < minimumTextLength) {
        alert("minimum " + minimumTextLength + " characters");
        return;
    }

    ajaxHttp.onreadystatechange = function () {
        var obj = JSON.parse(ajaxHttp.response)

        let packageList = obj;
        let htmlPackageList = document.getElementsByClassName("package-list")[0];
        htmlPackageList.innerHTML = '';

        packageList.forEach(package => {
            packageNode = createItemForPackageList(package);
            htmlPackageList.appendChild(packageNode);
        });
    }
    ajaxHttp.send();
}




async function getPackageProperties(packageContainer) {
    // let id = packageContainer.childNodes[1].childNodes[0].textContent;
    // let versionSelector = packageContainer.childNodes[1].childNodes[5];
    // let url = baseURL + '/getVersions?id=' + id+'architecture=';

    let name = packageContainer.childNodes[0].textContent;

    let url = baseURL + '/package?name=' + name;

    let ajaxHttp = new XMLHttpRequest({ mozSystem: true });

    ajaxHttp.open("GET", url, true);
    setAjaxHeaders(ajaxHttp);

    ajaxHttp.onreadystatechange = function () {
        var obj = JSON.parse(ajaxHttp.response)

        let versionList = [];

        obj.forEach(function (package, index) {
            versionList.push({"version":package["_version"], "architecture":package["_architecture"]});
        });


        versionDictionary[obj[0]["_name"]] = versionList; 

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
    let architecture = elem.value.substr(sepIndex+3, 15);
    let name = elem.parentNode.parentNode.parentNode.childNodes[0].textContent;



    let url = baseURL + '/getPackage?name=' + name + '&version=' + version +'&architecture='+architecture;
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
    console.log(wantedPackages);
    let url = baseURL + '/checkout';
    let ajaxHttp = new XMLHttpRequest({ mozSystem: true });
    ajaxHttp.open("POST", url, true);
    setAjaxHeaders(ajaxHttp);

    ajaxHttp.onreadystatechange = () => {
    }
    ajaxHttp.send(JSON.stringify(wantedPackages));
}
function selectClick(elem, event)
{
    elem.childNodes[0].disabled = true;
    event.stopPropagation();
}