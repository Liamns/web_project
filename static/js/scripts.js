/*!
 * Start Bootstrap - Shop Homepage v5.0.5 (https://startbootstrap.com/template/shop-homepage)
 * Copyright 2013-2022 Start Bootstrap
 * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
 */
// This file is intentionally blank
// Use this file to add JavaScript to your project

let pager = 1;

window.addEventListener("scroll", infiniteScroll, { passive: true });

let timer = null;

function getCookie(key) {
  var result = null;
  var cookie = document.cookie.split(";");
  cookie.some(function (item) {
    // 공백을 제거
    item = item.replace(" ", "");

    var dic = item.split("=");

    if (key === dic[0]) {
      result = dic[1];
      return true; // break;
    }
  });
  return result;
}

function infiniteScroll() {
  const currentScroll = window.scrollY;
  const windowHeight = window.innerHeight;
  const bodyHeight = document.querySelector("section").clientHeight;
  const paddingBottom = 200;

  if (currentScroll + windowHeight + paddingBottom >= bodyHeight) {
    if (!timer) {
      timer = setTimeout(() => {
        timer = null;
        pager++;
        // -- fetch API --
        fetch("http://127.0.0.1:8000/events/", {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
          },
          body: JSON.stringify({
            page: pager,
          }),
        })
          .then((response) => response.json())
          .then((data) => console.log(data));
      }, 200);
    }
  }
}

// window.addEventListener("scroll", callback, { passive: true });
