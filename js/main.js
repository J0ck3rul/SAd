function goHome(){
    triggerLoading(750);
    var browse = document.getElementsByClassName("row-image")[0];
    browse.style.display = "block";
    
    var browse = document.getElementsByClassName("browse")[0];
    browse.style.display = "none";
}

function goSearch(){
    triggerLoading(750);
    var browse = document.getElementsByClassName("home")[0];
    browse.style.display = "none";

    var browse = document.getElementsByClassName("browse")[0];
    browse.style.display = "block";
}