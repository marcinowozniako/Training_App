const messages = document.getElementsByClassName('alert')

setTimeout(function (){
    messages[0].classList.add('fade')
},2000)

setTimeout(function (){
    messages[0].classList.add('collapse')
},2850)