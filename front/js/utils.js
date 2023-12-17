function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function deleteCookie(name) {
    document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT; path=/';
}

function getQueryParams() {
    const queryParams = new URLSearchParams(window.location.search);
    const params = {};

    for (const [key, value] of queryParams.entries()) {
        params[key] = value;
    }

    return params;
}

function off_loader() {
    document.getElementById("loader").style.visibility = 'hidden';
}

function on_loader() {
    document.getElementById("loader").style.visibility = 'visible';
}

var data_profession = {};

function get_profession(profession) {
    document.getElementById("profi_desc").innerHTML = "";
    remove_target_profi();
    set_target_profi(profession);
    if (profession in data_profession) {
        document.getElementById("profi_desc").innerHTML = `<p>${data_profession[profession]}</p>`;
        return 0
    }
    on_loader();
    var data = JSON.stringify({
        "job": profession
    });

    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === 4) {
            if (this.status === 200) {
                console.log(this.responseText);
                let data = JSON.parse(this.responseText);
                data_profession[profession] = data.gigachat;
                document.getElementById("profi_desc").innerHTML = `<p>${data.gigachat}</p>`;
                off_loader();
            } else {
                console.log(this.responseText);
                alert("Ошибка на стороне сервера");
            }
        }
    });

    xhr.open("POST", "/api/job");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Authorization", `Bearer ${getCookie('access_token')}`);

    xhr.send(data);
}



function createButtons(professions) {
    const container = document.getElementById('profi');
    container.innerHTML = ''; // Очищаем контейнер перед добавлением новых кнопок

    professions.forEach((profession, index) => {
        const button = document.createElement('div');
        button.className = `button color-${(index % 10) + 1}`; // Назначаем классы для стилизации и цвета
        button.addEventListener('click', function () {
            get_profession(profession);
        });
        button.textContent = profession;
        container.appendChild(button);
    });
}


function set_target_profi(text) {
    var divs = document.getElementsByTagName('div');

    for (var i = 0; i < divs.length; i++) {
        if (divs[i].textContent.trim() === text) {
            divs[i].name = 'target_profi';
            divs[i].style.border = '10px solid transparent';
            divs[i].style.borderImage = 'linear-gradient(45deg, rgba(52, 152, 219, 1), rgba(231, 76, 60, 1)) 1';
            break;
        }
    }
}

function remove_target_profi() {
    var divs = document.getElementsByTagName('div');

    for (var i = 0; i < divs.length; i++) {
        if (divs[i].name === 'target_profi') {
            divs[i].name = '';
            divs[i].style.border = '';
            divs[i].style.borderImage = '';
        }
    }
}

function send_vk_id() {
    var data = JSON.stringify({
        "vk_id": document.getElementById("vk_data").value
    });

    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === 4) {
            console.log(this.responseText);
        }
    });

    xhr.open("PUT", "/api/update_vk_id");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Authorization", `Bearer ${getCookie('access_token')}`);

    xhr.send(data);
}


function send_question() {
    var obj = {
        "question_1": "Какие предметы в школе нравятся больше всего?",
        "question_2": "Какие академические достижения есть? (олимпиады, победы в конкурсах)",
        "question_3": "Предпочтение работы в команде или одному?",
        "question_4": "Баланса между работой и личной жизнью?",
        "question_5": "Есть ли предпочтения относительно рабочей среды, например, офисная работа, удалённая работа, работа на открытом воздухе и т.д.?"
    }

    for (var key in obj) {
        if (obj.hasOwnProperty(key)) {
            var question = obj[key];
            var respons = document.getElementById(key).value;
            var data = JSON.stringify({
                "message": `${question} - ответ - ${respons}`,
            });
            if (respons && respons.length > 1) {
                var xhr = new XMLHttpRequest();
                xhr.withCredentials = true;
                xhr.addEventListener("readystatechange", function () {
                    if (this.readyState === 4) {
                        console.log(this.responseText);
                    }
                });
                xhr.open("PUT", "/api/message");
                xhr.setRequestHeader("Content-Type", "application/json");
                xhr.setRequestHeader("Authorization", `Bearer ${getCookie('access_token')}`);
                xhr.send(data);
            }
        }
    }
}


function send_gigachat() {
    var data = null;

    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === 4) {
            let data = JSON.parse(this.responseText);
            createButtons(data["jobs"]);
            off_loader();
            console.log(data["jobs"]);
            off_loader();
        }
    });

    xhr.open("GET", "/api/gigachat");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Authorization", `Bearer ${getCookie('access_token')}`);

    xhr.send(data);
}

function whoami() {
    var data = null;

    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === 4) {
            if (this.status === 200){
                console.log(this.responseText);
            } else {
                deleteCookie("access_token");
                window.location.href = "/index.html";
            }
        }
    });

    xhr.open("GET", "/api/whoami");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Authorization", `Bearer ${getCookie('access_token')}`);

    xhr.send(data);
}

// setCookie("exampleKey", "exampleValue", 7); // Сохраняет куки на 7 дней