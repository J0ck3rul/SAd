function sleep(ms){
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function firstLoadingEnd(){
    await sleep(500);
    document.getElementsByTagName('loading-screen')[0].classList.toggle('hidden');
    document.getElementsByTagName('loading-screen')[0].classList.toggle('shown');
}

function toggleLoading(){
    document.getElementsByTagName('loading-screen')[0].classList.toggle('hidden');
    document.getElementsByTagName('loading-screen')[0].classList.toggle('shown');
}