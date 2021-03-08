if(current) document.getElementById('userSelect').innerHTML= "Sécuriser mon panneau"
if(!current) document.getElementById('userSelect').innerHTML= "Lever mon panneau"
if(mode == 0){
    document.getElementById("secure-container").style.opacity = 0.5
    document.getElementById("secure-container").style.cursor = 'not-allowed'
    document.getElementById("userSelect").style.cursor = 'not-allowed'
    document.getElementById("userSelect").removeAttribute("href")
    document.getElementById("userMode").innerHTML = "Mode Manuel"
}
if(mode){
    document.getElementById("userMode").innerHTML = "Mode Automatique"
}


document.getElementById("dirValue").innerHTML = `${dir%360}°` 
