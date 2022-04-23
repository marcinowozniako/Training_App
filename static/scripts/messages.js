const messages = document.getElementsByClassName('alert')
console.log(messages)

setTimeout(function (){
    messages[0].classList.add('fade')
},2000)

setTimeout(function (){
    messages[0].classList.add('collapse')
},2850)