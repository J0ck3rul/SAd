async function goHome(show_loading = true){
    if(show_loading){
        toggleLoading();
        await sleep(500);
    }

    var browse = document.getElementsByClassName("row-distro")[0];
    browse.style.display = "block";

    var browse = document.getElementsByClassName("row-team")[0];
    browse.style.display = "block";
    
    var browse = document.getElementsByClassName("browse")[0];
    browse.style.display = "none";

    var arrow = document.getElementsByClassName("right-arrow")[0];
    arrow.style.right = "0";
    arrow.style.transform = "rotate(0)";
    arrow.setAttribute("onclick", "goBrowse()");

    var logo = document.getElementsByClassName("logo")[0];
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

    var browse = document.getElementsByClassName("row-distro")[0];
    browse.style.display = "none";

    var browse = document.getElementsByClassName("row-team")[0];
    browse.style.display = "none";

    var browse = document.getElementsByClassName("browse")[0];
    browse.style.display = "block";

    var arrow = document.getElementsByClassName("right-arrow")[0];
    arrow.style.right = "95.5%";
    arrow.style.transform = "rotate(180deg)";
    arrow.setAttribute("onclick", "goHome()");

    var logo = document.getElementsByClassName("logo")[0];
    logo.style.left = "95.5%";

    if(show_loading){
        toggleLoading();
        await sleep(500);
    }
}

async function expandPackage(elem){
    console.log(elem.getElementsByClassName("expandable")[0].style.display);
    if(elem.getElementsByClassName("expandable")[0].style.display === "block")
        elem.getElementsByClassName("expandable")[0].style.display = "none";
    else
        elem.getElementsByClassName("expandable")[0].style.display = "block";
}

async function selectOS(){
    document.getElementsByClassName("package-list")[0].style.display = "flex";
}