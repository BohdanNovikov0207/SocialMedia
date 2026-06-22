import { renderMessageImages, hasMessageImages, hasSelectedImages, clearSelectedImages, getSelectedImages } from "./loadImages.js";

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

const topChatName = document.getElementById('top-chat-user-id')

// let closeButtonGroup = document.getElementById("close-button-group")
// let closeButtonGroupSettings = document.getElementById("close-button-group-settings")
// let cancelGroupButton = document.getElementById("cancel-group-button")
// let chatBack = document.getElementById("chat-back")
// let createGroup = document.getElementById("create-group")
// let createButton = document.getElementById('create-button')
let chatButton = document.querySelectorAll('.chat-button')
let overlayNew = document.getElementById('overlay-new')
let overlaySet = document.getElementById('overlay-set')
let closeChatButton = document.getElementById('close-chat-button')

// closeButtonGroup.addEventListener('click', () => {
//     overlayNew.style.display = 'none';
// })

// closeButtonGroupSettings.addEventListener('click', () => {
//     overlaySet.style.display = 'none';
// })

// createGroup.addEventListener('click', () => {
//     overlayNew.style.display = 'flex';
// })

// createButton.addEventListener('click', () => {
//     overlaySet.style.display = 'flex';
// })

// cancelGroupButton.addEventListener('click', () => {
//     closeButtonGroup.click()
// })

// chatBack.addEventListener('click', () => {
//     closeButtonGroupSettings.click()
// })

const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute("content");
// 

const messageImagesInput = document.getElementById("message-images")

const messageImageButton = document.getElementById("message-image-button")

// 
// function hasMessageImages(data){
//     return Array.isArray(data.images) && data.images.length > 0
// }
// // 
// function renderMessageImages(images){
//     const imageList = document.createElement("div")
//     imageList.className = "message-images"
//     images.forEach((imageUrl) => {
//         const image = document.createElement("img")
//         image.src = imageUrl
//         image.alt = "Зображення в повідомленні"
//         imageList.appendChild(image)
//     }) 
//     return imageList
// }
// 
// function getSelectedImages(){
//     return Array.from(messageImagesInput.files) 
// }
// 
// function hasSelectedImages(){
//     return getSelectedImages().length > 0
// }
// 
// function clearSelectedImages(){
//     messageImagesInput.value = ""
// }
async function sendMessageWithImages(text){
    const formData = new FormData()
    formData.append("text", text)
    getSelectedImages().forEach((image) => {
        formData.append("images", image)
    })
    const response = await fetch(
        `/chats/${activeChatId}/messages/upload/`,
        {
            method: "POST",
            headers: { "X-CSRFToken": csrfToken },
            body: formData
        }
    )
    return response.json()
}
messageImageButton.addEventListener("click", () => {
    messageImagesInput.click()
    }
)

function renderMessage(data){
    const message = document.createElement('div')
    message.className = "message"
    if (data.sender === LOGGED_IN_USER){
        message.classList.add('my-message');
        message.innerHTML = `
        <div class="text-time">
                <span class=message-text>${data.text}</span>
                <span class=message-time>${data.created_at}</span>
        </div>`;
    } else {
        message.classList.add('other-message'); 
        message.innerHTML = 
            `
            <span class=message-sender>${data.sender}</span>
            <div class="text-time">
                <span class=message-text>${data.text}</span>
                <span class=message-time>${data.created_at}</span>
            </div>
            `;
    }
    if(hasMessageImages(data)){
        message.appendChild(renderMessageImages(data.images))
    }
    message.style.height = 'auto'
    message.style.minHeight = 'max-content'
    return message
}


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
    data.messages.forEach(
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

function startObserver(){
    const sentinel = document.getElementById("message-load-sentinel")
    observer = new IntersectionObserver(
        async (entries) => {
            if (entries[0].isIntersecting && isLoading === false) {
                await loadMessages(true)
            }
        },
        {
            root: messages,
            rootMargin: "20px"
        }
    )
    observer.observe(sentinel)
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
        messages.appendChild(renderMessage(data))
        // 
        messages.scrollTop = messages.scrollHeight
    }
}

let currentUsername = null
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
    const topChatHeader = document.getElementById('top-chat-header');
    if (topChatHeader) {
        topChatHeader.style.setProperty('display', 'flex', 'important');
    }
    const topChatName = document.getElementById('top-chat-user-id');
    if (topChatName) {
        topChatName.textContent = data.username || username;
    }
    const chatTextBlock = document.getElementById("chat-text-block")
    if (chatTextBlock){
        chatTextBlock.classList.remove("is-placeholder")
    }
    
    if (chatTitle) chatTitle.style.display = 'none';
    if (chatStatus) chatStatus.style.display = 'none';
    
    
    chatWindow.classList.add('is-open')
    
    resetMessages(data.chat_id)
    connectWebSocket(data.chat_id)
    await loadMessages()
    startObserver()

}



closeChatButton.addEventListener('click', () => {
    if (chatSocket){
        chatSocket.close()
        chatSocket = null
    }
    if (chatWindow){
        chatWindow.classList.remove('is-open')
    }
    if (chatTitle){
        chatTitle.style.display = 'block'
        chatTitle.textContent = "Почніть нове спілкування"
    }
    if (chatStatus){
        chatStatus.style.display = 'block'
    }
    let topChatHeader = document.getElementById('top-chat-header')
    if (topChatHeader) {
        topChatHeader.style.setProperty('display', 'none', 'important');
    }
    document.getElementById("chat-text-block").classList.add("is-placeholder")
})

async function openChatById(chatId, title){
    const chatTextBlock = document.getElementById("chat-text-block")
    if (chatTextBlock){
        chatTextBlock.classList.remove("is-placeholder")
    }
    const topChatHeader = document.getElementById('top-chat-header')
    if (topChatHeader){
        topChatHeader.style.display = "flex"
    }
    const topChatUserId = document.getElementById("top-chat-user-id")
    if (topChatUserId){
        topChatUserId.textContent = title
    }
    chatTitle.textContent = title
    chatWindow.classList.add("is-open")
    chatTitle.hidden = true
    chatStatus.hidden = true
    resetMessages(chatId)
    connectWebSocket(chatId)
    await loadMessages()
    startObserver()
}

function bindGroupChatButtons(){
    const groupButtons = document.querySelectorAll("[data-chat-id]")
    groupButtons.forEach((button) => {
        if(button.dataset.groupBound === "true"){
            return
        }
        button.dataset.groupBound = "true"
        button.addEventListener(
            "click",
            async () => {
                await openChatById(button.dataset.chatId, button.dataset.chatTitle)
            }
        )
    })
}

// Робимо функцію відкриття чату доступною для group_chat.js після створення нової групи.

window.openChatById = openChatById

// Робимо повторне підключення кнопок груп доступним для group_chat.js.

window.bindGroupChatButtons = bindGroupChatButtons

// Підключаємо кнопки груп, які вже були відрендерені на сторінці.

bindGroupChatButtons()

// 
chatButtons.forEach((button) => {
    button.addEventListener(
        'click',
        async () => {
            await openChatWithUser(button.dataset.chatUser, button.dataset.chatUsername)
        }
    )
})

// document.querySelectorAll('.chat-button').forEach((button) => {
//    button.addEventListener(
//        'click',
//        async () => {
//            await openChatWithUser(button.dataset.chatUser, button.dataset.chatUsername)
//        }
//    )
// })

messageForm.addEventListener(
    'submit',
    async function (event){
        event.preventDefault()
        const text = messageInput.value.trim()
        if (!text && !hasSelectedImages()) return;
        if (hasSelectedImages()){
            const data = await sendMessageWithImages(text)
            if (!data.success) return;
            messageInput.value = ""
            clearSelectedImages()
            return
        }
        chatSocket.send(JSON.stringify({text: text}))
        messageInput.value = ''
    }
)



document.addEventListener('click', function(event) {
    const modalOverlay = document.getElementById('overlay');
    const ThreeDots = event.target.closest('#edit-menu-dots');
    
    if (ThreeDots) {
        event.preventDefault();
        event.stopPropagation();
        if (modalOverlay) {
            if (modalOverlay.style.display === 'block') {
                modalOverlay.style.display = 'none';
            } else {
                modalOverlay.style.display = 'block';
            }
        }
        return;
    }
    if (modalOverlay && modalOverlay.style.display === 'block') {
        const isClickInsideModal = event.target.closest('#overlay') || event.target.closest('.overlay-edit-chat');
        
        if (!isClickInsideModal) {
            modalOverlay.style.display = 'none';
        }
    }
});

document.addEventListener('click', function(event) {
    const editModal = document.getElementById('overlay-edit');
    const openEditModal = event.target.closest('#edit-modal');
    const closeX = event.target.closest('#edit-close-cross');
    const closeBack = event.target.closest('#close-edit-modal');

    const deleteEditFriend = event.target.closest('.delete-friend');
    if (deleteEditFriend) {
        event.preventDefault();
        const memberRow = deleteEditFriend.closest('.friend-choice');
        if (memberRow) {
            memberRow.remove();
        }
        return;
    }

    if (openEditModal) {
        event.preventDefault();
        event.stopPropagation();
        
        if (editModal) {
            const activeChat = document.querySelector('.groups-chats-container.active') || 
                               document.querySelector('.groups-chats-container.selected') ||
                               document.querySelector('.groups-chats-container');
                               
            const listContainer = document.getElementById('modal-members-list');

            if (activeChat && listContainer) {
                listContainer.innerHTML = '';

                const membersData = activeChat.getAttribute('data-members');

                if (membersData) {
                    try {
                        const members = JSON.parse(membersData);

                        members.forEach(member => {
                            const item = document.createElement('div');
                            item.className = 'friend-choice';
                            item.setAttribute('data-user-id', member.id);
                            item.innerHTML = `
                                <img src="/static/home_app/images/avatar6.png" class="friend-avatar">
                                <div class="delete-friend-container">
                                    <span class="user-name-text">${member.username}</span>
                                    <img src="/static/chat_app/images/trashcan.png" class="delete-friend">
                                </div>
                            `;
                            listContainer.appendChild(item);
                        });
                    } catch (e) {
                        console.error(e);
                    }
                }
            }
            editModal.style.display = 'flex';
        }
        return;
    }

    if (closeX || closeBack) {
        event.preventDefault();
        if (editModal) {
            editModal.style.display = 'none';
        }
        return;
    }

    if (editModal && editModal.style.display === 'flex') {
        if (event.target === editModal) {
            editModal.style.display = 'none';
        }
    }
});


document.addEventListener('click', function(event) {
    const editModal = document.getElementById('overlay-edit');
    const newModal = document.getElementById('overlay-new');

    const openNewMemberModal = event.target.closest('#add-member');
    const cancelNewModal = event.target.closest('#cancel-group-button');

    if (openNewMemberModal) {
        event.preventDefault();
        if (editModal) {
            editModal.style.display = 'none'; 
        }
        if (newModal) {
            newModal.style.display = 'flex';  
        }
        return;
    }

    if (cancelNewModal) {
        event.preventDefault();
        if (newModal) {
            newModal.style.display = 'none'; 
        }
        if (editModal) {
            editModal.style.display = 'flex'; 
        }
        return;
    }

    if (event.target === newModal) {
        newModal.style.display = 'none';
    }
});

document.addEventListener('click', function(event) {
    const editModal = document.getElementById('overlay-edit');
    const newModal = document.getElementById('overlay-new');

    const closeXGroup = event.target.closest('#close-button-group');
    const cancelNewModal = event.target.closest('#cancel-group-button');
    if (closeXGroup || cancelNewModal) {
        event.preventDefault();
        if (newModal) {
            newModal.style.display = 'none';  
        }
        if (editModal) {
            editModal.style.display = 'flex'; 
        }
        return;
    }
});