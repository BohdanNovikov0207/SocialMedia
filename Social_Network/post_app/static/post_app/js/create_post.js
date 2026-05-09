// Дістаємо CSRF-токен з meta-тега, щоб Django прийняв POST-запит через fetch.
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute("content");
}

document.getElementById('design-proceed').addEventListener(
    'click',
    function(){
        document.querySelector(".overlay1").style.display = "flex"
    }
)

let input1 = document.getElementById("post-text-input")
let input2 = document.getElementById("id_content")

document.getElementById("post-text-input").addEventListener(
    'change',
    function(){
        input2.value = input1.value
    }
)
document.getElementById("id_content").addEventListener(
    'change',
    function(){
        input1.value = input2.value
    }
)

document.getElementById('close-button').addEventListener(
    'click',
    function(){
        document.querySelector(".overlay1").style.display = "none"
    }
)

document.getElementById('close-button-tag').addEventListener(
    'click',
    function(){
        document.querySelector(".overlay2").style.display = "none"
    }
)



// Показуємо помилки, які backend повертає у JSON-форматі.
function renderErrors(errors) {
    const errorsContainer = document.getElementById("post-errors");
    errorsContainer.innerHTML = "";

    for (const fieldName in errors) {
        errors[fieldName].forEach((errorObj) => {
            const p = document.createElement("p");
            p.textContent = errorObj.message;
            errorsContainer.appendChild(p);
        });
    }
}

document.addEventListener("DOMContentLoaded", function () {
    let list_tags = document.getElementById("id_tags");
    let plus_tag = document.getElementById("plus-tag");

    // console.log(list_tags);
    // console.log(plus_tag);

    if (list_tags && plus_tag){
        let li = document.createElement("li");
        li.appendChild(plus_tag);
        list_tags.appendChild(li);
        // console.log("knopka v spiske");
    }
});

document.getElementById('plus-tag').addEventListener(
    'click',
    function(){
        document.querySelector('.overlay2').style.display = "flex"
    }
)

const linkInin = document.getElementById("link-inin");

const plusButton = document.getElementById("add-link");

plusButton.addEventListener("click", function () {

    
    const oldBtn = document.querySelector(".only-button");
    if (oldBtn) oldBtn.remove();

  
    const container = document.createElement("div");
    container.className = "input-and-button";

    const inputContainer = document.createElement("div");
    inputContainer.className = "link-input-container";

    const input = document.createElement("input");
    input.type = "url";
    input.name = "links";
    input.placeholder = "https://example.com";

    inputContainer.appendChild(input);

  
    const btnWrapper = document.createElement("div");
    btnWrapper.className = "only-button";

    const button = document.createElement("button");
    button.type = "button";
    button.className = "add-link-button";

    const img = document.createElement("img");
    img.src = "/static/post_app/images/plus.png";

    button.appendChild(img);
    btnWrapper.appendChild(button);

    
    container.appendChild(inputContainer);
    container.appendChild(btnWrapper);

    linkInin.appendChild(container);
});

// Відправляємо форму у фоновому режимі без перезавантаження сторінки.
document.getElementById("post-create-form").addEventListener("submit", function (e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);

    fetch(form.action, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "X-Requested-With": "XMLHttpRequest",
        },
        body: formData,
    })
    .then(async (response) => {
        // Спочатку читаємо JSON, а потім перевіряємо HTTP-статус.
        const data = await response.json();

        if (!response.ok) {
            throw data;
        }

        return data;
    })
    .then((data) => {
        // Після успішного створення переходимо на сторінку всіх постів.
        if (data.redirect_url) {
            window.location.href = data.redirect_url;
        }
    })
    .catch((data) => {
        // Якщо Django повернув помилки форми, показуємо їх над формою.
        if (data.errors) {
            renderErrors(data.errors);
        }
    });
});

