/*!
 * Start Bootstrap - Shop Homepage v5.0.5 (https://startbootstrap.com/template/shop-homepage)
 * Copyright 2013-2022 Start Bootstrap
 * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
 */
// This file is intentionally blank
// Use this file to add JavaScript to your project

var infinite = new Waypoint.Infinite({
  element: $('.infinite-container')[0],

  offset: 'bottom-in-view',
  onBeforePageLoad: function () {
    $('.loading').show();
  },
  onAfterPageLoad: function ($items) {
    $('.loading').hide();
  }
});

const firstSelect = document.getElementById("address");
const secondSelect = document.getElementById("address_detail");
const thirdSelect = document.getElementById("gathering");
const btns = document.getElementById("btns");
const searchForm = document.getElementById("searchForm");
const searchBtn = document.querySelector(".search")

firstSelect.addEventListener("change", function (e) {

  e.preventDefault();

  const selectedValue = firstSelect.value;
  let options =
    '<option class="dropdown-item address2" value="">세부지역</option>' + '<option class="dropdown-item address2" value="">전체</option>';

  if (selectedValue in address_total) {
    address_total[selectedValue].forEach(function (option) {
      options += "<option  class='dropdown-item address2' value='" + option + "' {% if '" + option + "' in address %} selected='selected' {% endif %}" + "'>" + option + "</option>";
    });
  };

  secondSelect.innerHTML = options;

  let addressForm = document.querySelector("#addressForm");

  addressForm.value = e.target.value;

  if (addressForm.value == "전체") {
    searchForm.submit()
  }
});


secondSelect.addEventListener("change", function (e) {

  e.preventDefault();

  addressForm.value += " ";
  addressForm.value += e.target.value;


  searchForm.submit();

});


let gatheringForm = document.querySelector("#gatheringForm")

thirdSelect.addEventListener("change", function (e) {

  e.preventDefault();
  gatheringForm.value = e.target.value;

  searchForm.submit();

})

let keywordForm = document.querySelector("#keywordForm");
let keyword = document.querySelector("#keyword");

searchBtn.addEventListener("click", function () {

  keywordForm.value = keyword.value

  searchForm.submit()

})

let so = document.querySelector("#so")
let sortForm = document.querySelector("#sortForm")

so.addEventListener("change", function () {

  sortForm.value = so.value;

  searchForm.submit();

});

btns.scrollIntoView();