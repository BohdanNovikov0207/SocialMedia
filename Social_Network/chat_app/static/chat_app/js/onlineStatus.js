const globalOnlineUsers = new Set(); 
const onlineSocket = new WebSocket(`ws://${window.location.host}/chat/online/`) 
onlineSocket.onmessage = function(event) {
    const data = JSON.parse(event.data) 
    if (data.online_users_count && Array.isArray(data.online_users_count)){
        data.online_users_count.forEach(id => globalOnlineUsers.add(String(id)))
    }else if(data.user_id){
        if (data.status === 'online'){
            globalOnlineUsers.add(String(data.user_id))
        }else{
            globalOnlineUsers.delete(String(data.user_id))
        }
    }
    const buttons = document.querySelectorAll(`[data-chat-user="${data.user_id}"]`)
    buttons.forEach(
        (button) => {
            const statusBall = document.querySelectorAll(`.status-ball[data-chat-user="${data.user_id}"]`)
            const statusBallRequest = document.querySelectorAll(`.status-ball-request[data-chat-user="${data.user_id}"]`)
            let statusColor = ''
            if (data.status == 'online'){
                console.log('online')
                statusColor = '#22C55E'
            }else{
                console.log('offline')
                statusColor = '#CDCED2'
            }
            statusBall.forEach(ball => {
                ball.style.backgroundColor = statusColor
            })
            statusBallRequest.forEach(ball => {
                ball.style.backgroundColor = statusColor
            })
            const topChatUserStatus = document.querySelector('.top-chat-user-status')
            if (topChatUserStatus){
                if (data.is_group){
                    topChatUserStatus.setAttribute('data-chat-type', 'group')
                    topChatUserStatus.setAttribute('data-total-members', data.total_members)
                    topChatUserStatus.setAttribute('data-online-users', data.group_users_ids.join(','))
                    groupStatus()
                }else{
                    if (topChatUserStatus.getAttribute('data-chat-type') !== 'group'){
                        const currentUserId = topChatUserStatus.getAttribute('data-personal-user-id')
                        if(currentUserId && String(data.user_id) === String(currentUserId)){
                            topChatUserStatus.innerHTML = data.status
                        }
                    }
                }
            }
        }
    )
    groupStatus()
}
export function groupStatus(){
    const topChatUserStatus = document.querySelector('.top-chat-user-status')
    if (!topChatUserStatus || topChatUserStatus.getAttribute('data-chat-type') !== 'group') return;
        const totalMembers = topChatUserStatus.getAttribute('data-total-members') || 0
        const onlineUsers = topChatUserStatus.getAttribute('data-online-users')
        if (!onlineUsers) return;
            const groupUserIds = onlineUsers.split(',')
            let onlineUsersCount = 0
        groupUserIds.forEach(id => {
            if (typeof globalOnlineUsers !== 'undefined' && globalOnlineUsers.has(String(id).trim())){
                onlineUsersCount++;
            }
        })
    topChatUserStatus.innerHTML = `${totalMembers} учасники, ${onlineUsersCount} в мережі`
}
    // if (topChatUserStatus){
    //     const chatGroup = topChatUserStatus.getAttribute('data-is-group') === 'true'
    //     if (chatGroup){
    //         totalMembers = document.querySelectorAll('[data-chat-user]').length
    //         topChatUserStatus.textContent = `${totalMembers} учасники`
    //     }else{
    //         topChatUserStatus.textContent = data.status
    //     }
    // }
