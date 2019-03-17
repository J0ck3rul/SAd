function sleep(ms){
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function finishLoading(){
    await sleep(1000);
    document.getElementsByTagName('loading-screen')[0].classList.toggle('hidden');
    await sleep(1000);
    document.getElementsByTagName('loading-screen')[0].style.display = 'none';
}