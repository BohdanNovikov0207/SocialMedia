const onlineSocket = new WebSocket(`ws://${window.location.host}/chat/online/`)
onlineSocket.onmessage = function(event) {
    const data = JSON.parse(event.data) 
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
                topChatUserStatus.textContent = data.status
            }
        }
    )
    // if (topChatUserStatus){
    //     const chatGroup = topChatUserStatus.getAttribute('data-is-group') === 'true'
    //     if (chatGroup){
    //         totalMembers = document.querySelectorAll('[data-chat-user]').length
    //         topChatUserStatus.textContent = `${totalMembers} учасники`
    //     }else{
    //         topChatUserStatus.textContent = data.status
    //     }
    // }
}