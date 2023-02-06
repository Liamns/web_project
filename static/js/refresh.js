const current_url = window.location.href

function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

fetch(current_url, {
    method: "GET"
}).then((response) => {
    if (!response.ok) {
        fetch("refresh/token/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": "application/json"
            },

        }).then((response) => response.json()).then(data => console.log(data))
    } else {
        response.json()
    }
}).then(data => console.log(data))