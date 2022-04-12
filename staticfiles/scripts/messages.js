// document.ready(function (){
//     setTimeout(function (){
//         '.alert'.fadeOut('slow')
//
//     }, 100)
// })
const messages = document.getElementsByClassName('alert')
console.log(messages)

setTimeout(function (){
    messages[0].classList.add('fade')
    // messages[0].classList.add('collapse')
},2000)

setTimeout(function (){
    messages[0].classList.add('collapse')
    // messages[0].classList.add('collapse')
},2850)