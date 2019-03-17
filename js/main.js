async function goHome(){
    toggleLoading();
    await sleep(500);

    var browse = document.getElementsByClassName("row-image")[0];
    browse.style.display = "block";
    
    var browse = document.getElementsByClassName("browse")[0];
    browse.style.display = "none";

    toggleLoading();
}

async function goSearch(){
    toggleLoading();
    await sleep(500);

    var browse = document.getElementsByClassName("row-image")[0];
    browse.style.display = "none";

    var browse = document.getElementsByClassName("browse")[0];
    browse.style.display = "block";

    toggleLoading();
}