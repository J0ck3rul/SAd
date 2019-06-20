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


window.onscroll = function() {
    scrollFunction();
}

function scrollFunction()
{
    if (document.body.scrollTop > 35 || document.documentElement.scrollTop > 35) {
        document.getElementById("goTop").style.display = "block";
      } else {
        document.getElementById("goTop").style.display = "none";
      }
}

function goTop()
{
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

