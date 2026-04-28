export function getCSRFToken(){
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content')
}
export function showRegisterForm(){
    document.querySelector(".form_register").style.display = 'flex'
    document.querySelector(".form_login").style.display = 'none'
    // document.querySelector('.form_register nav').firstElementChild.style.cssText = 'border-bottom: 2px solid #543C52'
}
showRegisterForm()
export function showLoginForm(){
    document.querySelector(".form_register").style.display = 'none'
    document.querySelector(".form_login").style.display = 'flex'
    // document.querySelector('.form_login nav').lastElementChild.style.cssText = 'border-bottom: 2px solid #543C52'
}
document.getElementById('register').addEventListener(
    'click',
    function(){
        showRegisterForm()
    }
)
document.getElementById('login').addEventListener(
    'click',
    function(){
        showLoginForm()
    }
)

export function renderErrors(containerId, errors) {
    const errorsContainer = document.getElementById(containerId)
    errorsContainer.innerHTML = ""
    for (let fieldName in errors ){
        errors[fieldName].forEach(errorObj => {
            let p = document.createElement('p')
            p.textContent = errorObj.message
            errorsContainer.appendChild(p)
        })
    }
}