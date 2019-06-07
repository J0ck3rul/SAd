async function goHome(show_loading = true){
    if(show_loading){
        toggleLoading();
        await sleep(500);
    }

    location.href = "#home";

    var browse = document.getElementsByClassName("row-distro")[0];
    browse.style.display = "block";

    var browse = document.getElementsByClassName("row-team")[0];
    browse.style.display = "block";
    
    var browse = document.getElementsByClassName("browse")[0];
    browse.style.display = "none";

    var arrow = document.getElementsByClassName("right-arrow")[0];
    arrow.style.right = null;
    arrow.style.left = null;
    arrow.style.right = "0";
    arrow.style.transform = "rotate(0)";
    arrow.setAttribute("onclick", "goBrowse()");

    var logo = document.getElementsByClassName("logo")[0];
    logo.style.right = null;
    logo.style.left = null;
    logo.style.left = "0";

    if(show_loading){
        toggleLoading();
        await sleep(500);
    }
}

async function goBrowse(show_loading = true){
    if(show_loading){
        toggleLoading();
        await sleep(500);
    }

    location.href = "#browse";

    var browse = document.getElementsByClassName("row-distro")[0];
    browse.style.display = "none";

    var browse = document.getElementsByClassName("row-team")[0];
    browse.style.display = "none";

    var browse = document.getElementsByClassName("browse")[0];
    browse.style.display = "flex";

    var arrow = document.getElementsByClassName("right-arrow")[0];
    arrow.style.right = null;
    arrow.style.left = null;
    arrow.style.left = "0";
    arrow.style.transform = "rotate(180deg)";
    arrow.setAttribute("onclick", "goHome()");

    var logo = document.getElementsByClassName("logo")[0];
    logo.style.right = null;
    logo.style.left = null;
    logo.style.right = "0";

    if(show_loading){
        toggleLoading();
        await sleep(500);
    }
}

async function expandPackage(elem){
    if(elem.getElementsByClassName("expandable")[0].style.display === "block")
        elem.getElementsByClassName("expandable")[0].style.display = "nonee";
    else
        {
            elem.getElementsByClassName("expandable")[0].style.display = "block";
            getAllVersions(elem);
        }
}

async function selectOS(){
    document.getElementsByClassName("package-list")[0].style.display = "flex";
    document.getElementsByClassName("apply-changes-button")[0].style.display = "block";
}

async function selectPackage(elem, event){
    event.stopPropagation();
    if(elem.classList.contains("selected")){
        elem.classList.toggle("selected");
        elem.innerText = "Select";
    }
    else{
        elem.classList.toggle("selected");
        elem.innerText = "Deselect";
    }
}