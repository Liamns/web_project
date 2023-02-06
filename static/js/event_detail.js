const event_part = document.getElementById("event_parti")
const user_id = document.getElementById("user_id").innerText
const event_id = document.getElementById("event_id").innerText

console.log("user_id : ", user_id, "event_id : ", event_id)

function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

const event_party = "{% url 'event_party' %}"

event_part.addEventListener("click", (e) => {
    fetch("http://127.0.0.1:8000/events/party/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            "user": user_id,
            "event": event_id
        })

    }).then(response => response.json()).then(data => {
        window.location.href
    })
})