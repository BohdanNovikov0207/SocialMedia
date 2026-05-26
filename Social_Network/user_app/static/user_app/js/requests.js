function getCSRFToken(){
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content')
}

const csrfToken = getCSRFToken()
const homeFriendsList = document.querySelector('[data-home-section= "friends"]')

async function handlerFriendAction(actionButton){
    const response = await fetch(actionButton.dataset.url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        }
        
    })

    const data = await response.json()
    if (data.status === 'redirect') {
        window.location.href = data.redirect_url;
        return;
}
    if (data.friend_html){
        addFriendToHome(data.friend_html)
    }

    if (data.label){
        actionButton.textContent = data.label
    }

    if (data.remove){
        actionButton.closest('article').remove()
    }
}

function addFriendToHome(friendHtml){
    const friendsCount = homeFriendsList.querySelectorAll('article').length
    if (friendsCount >= 6){
        return
    }

    homeFriendsList.querySelector('p')?.remove()
    homeFriendsList.insertAdjacentHTML('beforeend', friendHtml)
    connectFriendActionButtons(homeFriendsList)
}

function connectFriendActionButtons(parent = document){
    const actionButtons = parent.querySelectorAll('[data-friend-action]')
    actionButtons.forEach((actionButton) => {
        if (actionButton.dataset.actionButton){
            return
        }
        actionButton.dataset.actionButton = 'true'
        actionButton.addEventListener(
            'click',
            async () => {
                await handlerFriendAction(actionButton)
            }
        )   
    })
}
window.connectFriendActionButtons = connectFriendActionButtons
connectFriendActionButtons()

let mainButton = document.getElementById("main-friends")
let requestsButton = document.getElementById("requests-friends")
let recommendedButton = document.getElementById("recommended-friends")
let friendsButton = document.getElementById("all-friends")

let requestsSection = document.getElementById("requests")
let recommendedSection = document.getElementById("recommendations")
let friendsSection = document.getElementById("friends")

mainButton.addEventListener('click',
    function (){
        requestsSection.style.display = "flex"
        recommendedSection.style.display = "flex"
        friendsSection.style.display = "flex"
    })


requestsButton.addEventListener('click',
    function (){
        allRequests.click()
    }
)

recommendedButton.addEventListener('click',
    function (){
        allRecommendations.click()
    }
)

friendsButton.addEventListener('click',
    function (){
        allFriends.click()
    }
)

let allRequests = document.getElementById("all_requests")
let allRecommendations = document.getElementById("all_recommendations")
let allFriends = document.getElementById("all_friends")

allRequests.addEventListener('click', () => {

    requestsSection.style.display = "none"
    recommendedSection.style.display = "none"
    friendsSection.style.display = "none"
})

allRecommendations.addEventListener('click', () => {

    requestsSection.style.display = "none"
    recommendedSection.style.display = "none"
    friendsSection.style.display = "none"
})

allFriends.addEventListener('click', () => {

    requestsSection.style.display = "none"
    recommendedSection.style.display = "none"
    friendsSection.style.display = "none"
})

