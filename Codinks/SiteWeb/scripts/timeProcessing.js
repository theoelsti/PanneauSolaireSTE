var today = new Date();
var time = today.getHours();
var mainHello = document.getElementsByClassName("subTitle")[0]
if(time>17 || time < 7){
    mainHello.innerHTML = "Bonsoir Mme/Mr Bonvent ! ";
    mainHello.style.color = "#FF6C11"
}
else{
    mainHello.innerHTML = "Bonjour Mme/Mr Bonvent ! "
    mainHello.style.color = "#FF6C11"
}