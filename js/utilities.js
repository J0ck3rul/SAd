function sleep(ms){
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function firstLoadingEnd(){
    await sleep(750);
    document.getElementsByTagName('loading-screen')[0].classList.toggle('hidden');
    document.getElementsByTagName('loading-screen')[0].classList.toggle('shown');
}

async function triggerLoading(ms){
    document.getElementsByTagName('loading-screen')[0].classList.toggle('hidden');
    document.getElementsByTagName('loading-screen')[0].classList.toggle('shown');
    await sleep(ms);
    document.getElementsByTagName('loading-screen')[0].classList.toggle('hidden');
    document.getElementsByTagName('loading-screen')[0].classList.toggle('shown');
}