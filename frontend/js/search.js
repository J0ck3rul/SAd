function searchButton()
{
    var ajaxHttp = new XMLHttpRequest();
    var url = 'http://localhost:5123/search';

    ajaxHttp.open("GET", url, true);
    ajaxHttp.setRequestHeader("content-type","application/json");

    var searchText = document.getElementsByClassName("search-field");

    ajaxHttp.onreadystatechange = function () {
        var obj = JSON.parse(ajaxHttp.response)

        let packageList = obj["package_list"];

        let htmlPackageList = document.getElementsByClassName("package-list")[0];
        htmlPackageList.innerHTML = '';

        packageList.forEach(package => {
            packageNode = createPackageListItem(package);
            htmlPackageList.appendChild(packageNode);
        });
    }

    ajaxHttp.send();
}

function createPackageListItem(package)
{
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
    console.log(package["_version"]);
    version.innerHTML = "version: "+ package["_version"][package["_version"].length -1];

    let maintainer = document.createElement("p");
    maintainer.innerHTML = "maintainter: " + package["_maintainer"];

    let selectButton = document.createElement("button");
    selectButton.setAttribute("onclick","selectPackage(this, event");


    let selectVersion = document.createElement("select");
    selectVersion.setAttribute("onclick", "getAllVersions(this)");

    let baseOption = document.createElement("option");
    baseOption.innerHTML = "select a different version";
    
    selectVersion.appendChild(baseOption);
    // package["_version"].forEach(version=>{
    //     let newOption = document.createElement("option");
    //     newOption.innerHTML = version;
    //     selectVersion.appendChild(newOption);
    // })
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
function getAllVersions(x)
{
    x = x.parentElement;
    x = x.parentElement;
    x = x.childNodes[1].childNodes[0];
    x = x.textContent;
    console.log(x);
    
}



