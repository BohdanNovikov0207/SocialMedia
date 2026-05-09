function getCSRFToken(){
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content')
}

const form = document.getElementById("firstlogin-form")

if (form) {

    form.addEventListener(
        'submit', 
        function(event){
        event.preventDefault()

        const formData = new FormData(form)

        fetch(form.action, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "X-Requested-With": "XMLHttpRequest",
            },
            body: formData
        })
        .then(async response => {
            const data = await response.json()

            if (!response.ok) {
                throw data
            }

            return data
        })
        .then(data => {
            form.reset()
            window.location.reload()
        })
    })
}