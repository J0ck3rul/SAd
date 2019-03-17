async function goHome(){
    toggleLoading();
    await sleep(500);

    var browse = document.getElementsByClassName("row-image")[0];
    browse.style.display = "block";

    var browse = document.getElementsByClassName("row-distro")[0];
    browse.style.display = "block";

    var browse = document.getElementsByClassName("row-team")[0];
    browse.style.display = "block";
    
    var browse = document.getElementsByClassName("browse")[0];
    browse.style.display = "none";

    toggleLoading();
}

async function goBrowse(){
    toggleLoading();
    await sleep(500);

    var browse = document.getElementsByClassName("row-image")[0];
    browse.style.display = "none";

    var browse = document.getElementsByClassName("row-distro")[0];
    browse.style.display = "none";

    var browse = document.getElementsByClassName("row-team")[0];
    browse.style.display = "none";

    var browse = document.getElementsByClassName("browse")[0];
    browse.style.display = "block";

    toggleLoading();
}