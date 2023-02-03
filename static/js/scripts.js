/*!
 * Start Bootstrap - Shop Homepage v5.0.5 (https://startbootstrap.com/template/shop-homepage)
 * Copyright 2013-2022 Start Bootstrap
 * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
 */
// This file is intentionally blank
// Use this file to add JavaScript to your project

let data = 5;

fetch("/events/", {
  method: "GET",
})
  .then((response) => response.json())
  .then((data) => console.log(data));

window.addEventListener("scroll", infiniteScroll);

let timer = null;

function infiniteScroll() {
  const currentScroll = window.scrollY;
  const windowHeight = window.innerHeight;
  const bodyHeight = document.querySelector("section").clientHeight;
  const paddingBottom = 200;

  if (currentScroll + windowHeight + paddingBottom >= bodyHeight) {
    if (!timer) {
      timer = setTimeout(() => {
        timer = null;

        // -- fetch API --
      }, 200);
    }
  }
}

// window.addEventListener("scroll", callback, { passive: true });
