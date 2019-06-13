
function searchPackages() {
    let url = baseURL + '/search';
    let minimumTextLength = 4;
    
    
    let ajaxHttp = new XMLHttpRequest({ mozSystem: true });
    
    ajaxHttp.open("GET", url, true);
    setAjaxHeaders(ajaxHttp);
    
    let searchText = document.getElementsByClassName("search-field");
    let serachTextLength = searchText[0].textLength;
    if(serachTextLength < minimumTextLength)
        {
            alert("minimum "+ minimumTextLength + " characters");
            return ;
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

    // if (versionDictionary[id] === undefined)
        // await requestAndUpdateVersions(url, versionSelector, id);
    // else
        // UpdateVersions(versionSelector, id);

    let name = packageContainer.childNodes[0].textContent;

    let url = baseURL + '/getPackage?name='+name;
    
    let ajaxHttp = new XMLHttpRequest({ mozSystem: true });
    
    ajaxHttp.open("GET", url, true);
    setAjaxHeaders(ajaxHttp);

    ajaxHttp.onreadystatechange = function () {
        var obj = JSON.parse(ajaxHttp.response)

        // console.log(obj);

        console.log(packageContainer);
        let packageDetails = createPackeDetails(obj);
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
    }
    ajaxHttp.send(JSON.stringify(wantedPackeges));
}
