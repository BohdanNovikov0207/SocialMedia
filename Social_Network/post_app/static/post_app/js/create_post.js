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

document.addEventListener("DOMContentLoaded", function(){
    let closeButton = document.getElementById('close-button-tag')
    if (closeButton){
        closeButton.addEventListener(
            'click',
            function(){
                document.querySelector(".overlay2").style.display = "none"
            }
        )}

})

document.addEventListener("DOMContentLoaded", function() {
    const selectImage = document.getElementById('select-image');
    const idImages = document.getElementById('id_images');

    if (selectImage && idImages) {
        selectImage.appendChild(idImages);
        selectImage.addEventListener('click', function(si) {
            if (si.target !== idImages) {
                idImages.click();
            }
        });
    }
});

const saveTag = document.getElementById('save-tag');
const hashtagForm = document.getElementById('hashtag-form');

if (saveTag) {
    saveTag.addEventListener('click', function() {
        const formData = new FormData(hashtagForm);

        fetch(hashtagForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': hashtagForm.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => {
            if (response.ok) {
                let overlay2 = document.querySelector(".overlay2"); 
                if (overlay2) {
                    overlay2.style.display = "none"; 
                }
                let idHashtagName = document.getElementById('id_hashtag_name');
                if (idHashtagName) {
                    idHashtagName.value = ""; 
                }
            } else {
                alert("Помилка при збереженні хештега!");
            }
        });
    });
}

document.addEventListener("DOMContentLoaded", function() {
    const cancelTag = document.getElementById('cancel-tag');
    const idHashtagName = document.getElementById('id_hashtag_name'); 

    if (cancelTag && idHashtagName) {
        cancelTag.addEventListener('click', function() {
            idHashtagName.value = ""; 
            idHashtagName.focus(); 
        });
    }
});

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

function createLinkBlock() {

    let linksContainer = document.getElementById("link-inin")

    linksContainer.lastElementChild.querySelector(".only-button").remove()

    let container = document.createElement("div")
    container.className = "input-and-button"

    let inputContainer = document.createElement("div")
    inputContainer.className = "link-input-container"

    let input = document.createElement("input")
    input.type = "url"
    input.name = "links"
    input.placeholder = "https://example.com"

    let buttonContainer = document.createElement("div")
    buttonContainer.className = "only-button"

    let button = document.createElement("button")
    button.type = "button"
    button.className = "add-link-button"

    let img = document.createElement("img")
    img.src = "/static/post_app/images/plus.png"

    button.addEventListener("click", createLinkBlock)

    button.appendChild(img)
    buttonContainer.appendChild(button)
    inputContainer.appendChild(input)
    container.appendChild(inputContainer)
    container.appendChild(buttonContainer)
    linksContainer.appendChild(container)
}


// Первая кнопка
document.querySelector(".add-link-button").addEventListener(
    "click",
    createLinkBlock
);

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
    .catch(data => {
        // Якщо Django повернув помилки форми, показуємо їх над формою.
        if (data.errors) {
            renderErrors(data.errors);
        }
    });
});

const inputImages = document.getElementById('id_images'); // проверь ID своего инпута
const imageContainer = document.getElementById('image-container');

inputImages.addEventListener('change', function() {
    imageContainer.innerHTML = ''; 

    const files = Array.from(this.files).slice(0, 3);

    files.forEach((file) => {
        const reader = new FileReader();

        reader.onload = function(e) {
            const div = document.createElement('div');
            div.className = 'image-ind';
            div.innerHTML = `
                <img src="${e.target.result}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 12px;">
                <button type="button" class="delete-image" id="delete-image" style="background: transparent; width: 40px; height: 40px; border: none; position: absolute; top: 5px; right: 5px; cursor: pointer;">
                        <img src="/static/post_app/images/trashcan.png" style="width: 40px; height: 40px; display: block;" >
                </button>
            `;
            imageContainer.appendChild(div);
            div.querySelector(".delete-image").addEventListener('click', function(event) {
                event.preventDefault();
                event.stopPropagation();
                div.remove(); 
            });
        };
        reader.readAsDataURL(file);
    });
});

