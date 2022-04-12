// document.ready(function (){
//     setTimeout(function (){
//         '.alert'.fadeOut('slow')
//
//     }, 100)
// })
const messages = document.getElementsByClassName('alert')

setTimeout(function (){
    messages[0].classList.add('d-none')
},2000)