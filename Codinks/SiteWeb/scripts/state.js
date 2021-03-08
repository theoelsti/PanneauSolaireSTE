const dot = ['.','..','...','....']
let i = 0


setInterval(function(){
    if(typeof mode == undefined){
    if(i==4) i=0
    document.getElementsByClassName("actualMode")[0].innerHTML = ` Recherche en cours ${dot[i]}`
    i++
    }
    else if(mode == true){
        document.getElementsByClassName("actualMode")[0].innerHTML = `&nbsp Manuel`
    }
    else if(mode == false){
        document.getElementsByClassName("actualMode")[0].innerHTML = ` &nbsp Automatique`
    }

    if(typeof current == undefined){
    if(i==4) i=0
        document.getElementsByClassName("actualState")[0].innerHTML = ` Recherche en cours ${dot[i]}`
        i++
    }
    else if(current == false){
        document.getElementsByClassName("actualState")[0].innerHTML = `&nbsp Sécurisé` 
    }
    else if(current == true){
        document.getElementsByClassName("actualState")[0].innerHTML = `&nbsp Levé`
    }
    
},1000)


