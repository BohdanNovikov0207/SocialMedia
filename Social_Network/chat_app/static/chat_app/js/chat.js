let chatSocket = null
let observer = null
let activeChatId = null
let currentPage = 1
let isLoading = false
let hasNext = false

const chatTitle = document.querySelector('#chat-title')
const chatStatus = document.querySelector('#chat-status')
const chatButtons = document.querySelectorAll('[data-chat-user]')
// 
const chatWindow = document.getElementById('chat-window')
const messages = document.getElementById('messages')
const messageForm = document.getElementById('message-form')
const messageInput = document.getElementById('message-input')

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

const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute("content");
// 

function resetMessages(chatId){
    activeChatId = chatId
    currentPage = 1
    hasNext = true
    isLoading = false
    if(observer){observer.disconnect()}
    messages.innerHTML = ''
    const sentinel = document.createElement('div') 
    sentinel.id = 'message-load-sentinel'
    messages.prepend(sentinel)
}
// 
async function loadMessages(prepend = false){
    if( isLoading || !hasNext ){
        return
    }
    isLoading = true
    const oldHeight = messages.scrollHeight
    const response = await fetch(
        `/chats/chat_with/${activeChatId}/messages/?page=${currentPage}`,
        {
            headers: {
                'X-Requested-With': "XMLHttpRequest"
            }
        }
    )
    const data = await response.json()
    const fragment = document.createDocumentFragment()
    data.message.forEach(
        (message) => {
            fragment.appendChild(renderMessage(message))
        }
    )
    const sentinel = document.getElementById('message-load-sentinel')
    if(prepend){
        sentinel.after(fragment)
    }else{
        messages.appendChild(fragment)
    }
    hasNext = data.has_next
    currentPage++
    if(prepend){
        messages.scrollTop = messages.scrollHeight - oldHeight
    }else{
        messages.scrollTop = messages.scrollHeight
    }
    // якщо більше немає сторінок для завантаження
    if(!hasNext && observer){observer.disconnect()}
    isLoading= false
}

function connectWebSocket(chatId){
    // Якщо вже було виконано якесь вебсокет з'єднання  
    if (chatSocket){
        // закриваємо його
        chatSocket.close()
    }
    chatSocket = new WebSocket(`ws://${window.location.host}/chat_with/${chatId}/`)
    // обробляємо повідомлення від вебсокету
    chatSocket.onmessage = function (event){
        // 
        const data = JSON.parse(event.data)
    }
}
// Відкриває наявний чат або створюємо новий чат
async function openChatWithUser(userId, username) {
    const response = await fetch(
        `/chats/chat_with/${userId}/`, 
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            }
        }
    )
    const data = await response.json()
    if (!data.success){
        return
    }
    chatTitle.textContent = `Чат з ${data.username || username}`
    chatStatus.style = "display: none;"
    // Відкриваємо вебсокет з'єднання
    connectWebSocket(data.chat_id)
}

// 
chatButtons.forEach((button) => {
    button.addEventListener(
        'click',
        async () => {
            await openChatWithUser(button.dataset.chatUser, button.dataset.chatUsername)
        }
    )
})