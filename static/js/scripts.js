/*!
 * Start Bootstrap - Shop Homepage v5.0.5 (https://startbootstrap.com/template/shop-homepage)
 * Copyright 2013-2022 Start Bootstrap
 * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
 */
// This file is intentionally blank
// Use this file to add JavaScript to your project

fetch("http://127.0.0.1:8000", {
  method: "GET",
  headers: {
    Authentication:
      "JWT " + String(window.localStorage.getItem("aceess-token")),
  },
})
  .then((response) => response.json())
  .then((data) => {
    window.localStorage.clear();
  });

if (window.localStorage.getItem("aceess-token") != NaN) {
  const login_btn = document.querySelector(
    "#navbarSupportedContent > ul > li:nth-child(6) > a"
  );
  login_btn.innerHTML = "프로필";
  login_btn.classList.remove("btn-sm");
} else {
  const login_btn = document.querySelector(
    "#navbarSupportedContent > ul > li:nth-child(6) > a"
  );
  login_btn.innerHTML = "프로필";
}
