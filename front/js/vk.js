function vk_auth() {
    on_loader();
    var data = JSON.stringify({
        "url": window.location.href
    });

    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === 4) {
            if (this.status === 200){
                console.log(this.responseText);
                let data = JSON.parse(this.responseText);
                createButtons(data["jobs"]);
                off_loader();
            } else {
                console.log(this.responseText);
                alert("Ошибка на стороне сервера");
            }
        }
    });

    xhr.open("POST", "/api/vk");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Authorization", `Bearer ${getCookie('access_token')}`);

    xhr.send(data);
}

var data = getQueryParams();
console.log(data);
if (data.get_vk == "1"){
    console.log(data.get_vk);
    document.getElementById("vk_auth").style.visibility = 'visible';
    document.getElementById("vk_data").style.visibility = 'hidden';
} else {
    vk_auth();
    document.getElementById("vk_auth").style.visibility = 'hidden';
    document.getElementById("vk_data").style.visibility = 'visible';
}
