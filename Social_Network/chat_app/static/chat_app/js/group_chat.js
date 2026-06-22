// Знаходимо кнопку, яка відкриває модальне вікно створення групи.
const openGroupModalButton = document.querySelector("#open-group-modal");
// Знаходимо саме модальне вікно.
const groupModal = document.querySelector("#group-modal");
// Знаходимо перший крок модального вікна з вибором друзів.
const groupStepUsers = document.querySelector("#group-step-users");
// Знаходимо другий крок модального вікна з введенням назви.
const groupStepName = document.querySelector("#group-step-name");
// Знаходимо кнопку закриття на першому кроці.
const closeGroupModalButton = document.querySelector("#close-group-modal");
// Знаходимо кнопку закриття на другому кроці.
const closeGroupNameModalButton = document.querySelector("#close-group-name-modal");
// Знаходимо кнопку скасування створення групи.
const cancelGroupModalButton = document.querySelector("#cancel-group-modal");
// Знаходимо кнопку переходу до другого кроку.
const nextGroupStepButton = document.querySelector("#next-group-step");
// Знаходимо кнопку повернення до вибору друзів.
const backGroupStepButton = document.querySelector("#back-group-step");
// Знаходимо кнопку фінального створення групи.
const createGroupButton = document.querySelector("#submit-create-group");
// Знаходимо поле назви групового чату.
const groupNameInput = document.querySelector("#group-name");
// Знаходимо лічильник вибраних друзів.
const selectedCount = document.querySelector("#selected-count");
// Знаходимо блок, куди показуємо вибраних учасників на другому кроці.
const selectedUsersList = document.querySelector("#selected-users-list");
// Знаходимо всі чекбокси друзів у модальному вікні.
const groupUserCheckboxes = document.querySelectorAll(".group-user-checkbox");
// Знаходимо список груп у правому блоці сторінки.
const groupList = document.querySelector("#group-list");

// Відкриваємо модальне вікно на першому кроці.
function openGroupModal(){
    groupModal.hidden = false
    groupStepUsers.hidden = false
    groupStepName.hidden = true
}
// Закриваємо модальне вікно й очищаємо введені дані.
function closeGroupModal(){
    groupModal.hidden = true
    groupNameInput.value = ""
    selectedUsersList.innerHTML = ""
    groupUserCheckboxes.forEach((checkbox) => {
        checkbox.checked = false
    })
    updateSelectedCount()
}
// Оновлюємо кількість вибраних друзів у модальному вікні.
function updateSelectedCount(){
    const count = document.querySelectorAll(".group-user-checkbox:checked").length
    selectedCount.textContent = count
}

// Показуємо вибраних друзів на другому кроці перед створенням групи.

function renderSelectedUsers(){
    if (!selectedUsersList) return;
    selectedUsersList.innerHTML = ""; 

    groupUserCheckboxes.forEach((checkbox) => {
        if(checkbox.checked){
            const userName = checkbox.dataset.userName || "Користувач";
            const initial = userName.charAt(0).toUpperCase();

            const userRow = document.createElement("div");
            userRow.className = "friend-choice";

            userRow.innerHTML = `
                    <img src="/static/home_app/images/avatar4.png" class="friend-avatar" alt="Avatar">
                    <p class="user-name-text">${userName}</p>
                    <button type="button" class="delete-friend">
                        <img src="/static/chat_app/images/trashcan.png" class="delete-friend" alt="Видалити">
                    </button> `;
            const removeBtn = userRow.querySelector(".delete-friend");
            removeBtn.addEventListener("click", () => {
                checkbox.checked = false;
                userRow.remove();        
                updateSelectedCount();   
            });
            selectedUsersList.appendChild(userRow);
        }
    });
}

// Переходимо з вибору друзів до введення назви групи.

function showNameStep(){
    renderSelectedUsers()
    groupStepUsers.hidden = true
    groupStepName.hidden = false
}

// Повертаємося з другого кроку до вибору друзів.

function showUsersStep(){
    groupStepUsers.hidden = false
    groupStepName.hidden = true
}

// Додаємо створену групу в правий блок без перезавантаження сторінки.

function addGroupButton(chatId, name){
    const groupEmpty = document.getElementById("group-empty")
    if (groupEmpty){
        groupEmpty.remove()
    }
    const divAvat = document.createElement("div")
    const avat = document.createElement("img")
    divAvat.className = "chat-group-avatar"
    avat.src = "/static/home_app/images/avatar4.png"
    avat.style.display = "flex"
    avat.style.width = "46px"
    avat.style.height = "46px"
    divAvat.appendChild(avat)
    const textSpan = document.createElement("span")
    textSpan.textContent = name
    textSpan.className = "bold-text message-name"
    textSpan.style.fontFamily = "GT Walsheim Pro, sans-serif;"
    textSpan.style.fontWeight = "700"
    const button = document.createElement("div")
    // button.type = "button"
    button.className = "in-per chat-group-button"
    button.dataset.chatId = chatId
    button.dataset.chatTitle = name
    button.style.width = "348px"
    button.style.height = "62px"
    button.style.minWidth = "348px"
    button.style.minHeight = "62px"
    button.style.gap = "16px"
    button.style.display = "flex"  
    button.style.flexDirection = "row"
    button.style.justifyContent = "column"
    button.style.cursor = "pointer"
    button.appendChild(divAvat)         
    button.appendChild(textSpan)      
    groupList.appendChild(button)

    window.bindGroupChatButtons()
}

// Створюємо груповий чат на backend.

async function createGroup(){
    const groupNameInput = document.querySelector("#group-name")
    const formData = new FormData()
    formData.append("name", groupNameInput.value)
    groupUserCheckboxes.forEach((checkbox) => {
        if(checkbox.checked){
            formData.append("users", checkbox.value)
        }
    })
    const response = await fetch(
        `/chats/create_group/`,
        {
            method: "POST",
            headers: {
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
            },
            body: formData
        }
    )
    const data = await response.json()
    if(!data.success){
        return
    }

    let groupsCount = document.querySelectorAll(".groups-chats-container").length
    if (groupsCount < 6) {
        addGroupButton(data.chat_id, data.name)
    } else {
        window.location.reload()
    }

    closeGroupModal()
}

// Вішаємо відкриття модального вікна на кнопку створення групи.
openGroupModalButton.addEventListener("click", openGroupModal);
// Вішаємо закриття першого кроку.
closeGroupModalButton.addEventListener("click", closeGroupModal);
// Вішаємо закриття другого кроку.
closeGroupNameModalButton.addEventListener("click", closeGroupModal);
// Вішаємо скасування створення групи.
cancelGroupModalButton.addEventListener("click", closeGroupModal);
// Вішаємо перехід до кроку з назвою.
nextGroupStepButton.addEventListener("click", showNameStep);
// Вішаємо повернення до вибору друзів.
backGroupStepButton.addEventListener("click", showUsersStep);
// Вішаємо створення групи.
createGroupButton.addEventListener("click", createGroup);
// Оновлюємо лічильник при кожній зміні чекбокса друга.
groupUserCheckboxes.forEach((checkbox) => {
    // Реагуємо на вибір або зняття вибору друга.
    checkbox.addEventListener("change", updateSelectedCount);
});

document.getElementById('group-list').addEventListener('click', function(event) {
    const chatContainer = event.target.closest('.groups-chats-container');
    
    if (chatContainer) {
        const titleElement = chatContainer.querySelector('.chat-button-title');
        if (titleElement) {
            const chatName = titleElement.textContent.trim();
            const headerTitle = document.getElementById('top-chat-user-id');
            
            if (headerTitle) {
                headerTitle.textContent = chatName;
            }
        }
    }
});
document.addEventListener('change', function(event) {
    if (event.target.classList.contains('group-user-checkbox')) {
        const currentModal = event.target.closest('#overlay-new') || event.target.closest('#group-modal');
        
        if (currentModal) {
            const checkedCount = currentModal.querySelectorAll('.group-user-checkbox:checked').length;
            const countSpan = currentModal.querySelector('#selected-count');
            
            if (countSpan) {
                countSpan.textContent = checkedCount;
            }
        }
    }
});