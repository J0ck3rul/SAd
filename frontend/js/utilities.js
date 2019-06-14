function sleep(ms){
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function firstLoadingEnd(){
    if(window.location.hash != "") {
        var hash = window.location.hash.substring(1);
        if(hash === "browse"){
            goBrowse(false);
            await sleep(1000);
            document.getElementsByTagName('loading-screen')[0].classList.toggle('hidden');
            document.getElementsByTagName('loading-screen')[0].classList.toggle('shown');
        }
        else if(hash === "home"){
            goHome(false);
            await sleep(1000);
            document.getElementsByTagName('loading-screen')[0].classList.toggle('hidden');
            document.getElementsByTagName('loading-screen')[0].classList.toggle('shown');
        }
    }
    else{
        goHome(false);
        await sleep(500);
        document.getElementsByTagName('loading-screen')[0].classList.toggle('hidden');
        document.getElementsByTagName('loading-screen')[0].classList.toggle('shown');
    }
}

function toggleLoading(){
    document.getElementsByTagName('loading-screen')[0].classList.toggle('hidden');
    document.getElementsByTagName('loading-screen')[0].classList.toggle('shown');
}

