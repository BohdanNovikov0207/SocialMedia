function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute("content");
}

let closeButtonGroup = document.getElementById("close-button-group")
let closeButtonGroupSettings = document.getElementById("close-button-group-settings")
let cancelGroupButton = document.getElementById("cancel-group-button")
let chatBack = document.getElementById("chat-back")
let createGroup = document.getElementById("create-group")
let createButton = document.getElementById('create-button')
let overlayNew = document.getElementById('overlay-new')
let overlaySet = document.getElementById('overlay-set')

closeButtonGroup.addEventListener('click', () => {
    overlayNew.style.display = 'none';
})

closeButtonGroupSettings.addEventListener('click', () => {
    overlaySet.style.display = 'none';
})

createGroup.addEventListener('click', () => {
    overlayNew.style.display = 'flex';
})

createButton.addEventListener('click', () => {
    overlaySet.style.display = 'flex';
})

cancelGroupButton.addEventListener('click', () => {
    closeButtonGroup.click()
})

chatBack.addEventListener('click', () => {
    closeButtonGroupSettings.click()
})