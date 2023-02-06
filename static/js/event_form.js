var mapContainer = document.getElementById("map"), // 지도를 표시할 div
  mapOption = {
    center: new daum.maps.LatLng(37.537187, 127.005476), // 지도의 중심좌표
    level: 5, // 지도의 확대 레벨
  };

//지도를 미리 생성
var map = new daum.maps.Map(mapContainer, mapOption);
//주소-좌표 변환 객체를 생성
var geocoder = new daum.maps.services.Geocoder();
//마커를 미리 생성
var marker = new daum.maps.Marker({
  position: new daum.maps.LatLng(37.537187, 127.005476),
  map: map,
});



function sample5_execDaumPostcode() {
  new daum.Postcode({
    oncomplete: function (data) {
      var addr = data.address; // 최종 주소 변수

      // 주소 정보를 해당 필드에 넣는다.
      document.getElementById("sample5_address").value = addr;
      // 주소로 상세 정보를 검색
      geocoder.addressSearch(data.address, function (results, status) {
        // 정상적으로 검색이 완료됐으면
        if (status === daum.maps.services.Status.OK) {
          var result = results[0]; //첫번째 결과의 값을 활용

          // 해당 주소에 대한 좌표를 받아서
          var coords = new daum.maps.LatLng(result.y, result.x);
          // 지도를 보여준다.
          mapContainer.style.display = "block";
          map.relayout();
          // 지도 중심을 변경한다.
          map.setCenter(coords);
          // 마커를 결과값으로 받은 위치로 옮긴다.
          marker.setPosition(coords);
        }
      });
    },
  }).open();
}

// function getCookie(key) {
//   var result = null;
//   var cookie = document.cookie.split(";");
//   cookie.some(function (item) {
//     // 공백을 제거
//     item = item.replace(" ", "");

//     var dic = item.split("=");

//     if (key === dic[0]) {
//       result = dic[1];
//       return true; // break;
//     }
//   });
//   return result;
// }

function getCookie(name) {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

function praseJWT() {
  var token = getCookie("access_token")
  var base64Url = token.split('.')[1];
  var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');

  var jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  }).join(''));

  return JSON.parse(jsonPayload);
}

var user_id = praseJWT()['nkn']




const title = document.getElementById("title")
const content = document.getElementById("contents")
const image = document.getElementById("image")
const tags = document.getElementById("tags")
const deadline_time = document.getElementById("deadline-time")
const start_time = document.getElementById("start-time")
const end_time = document.getElementById("end-time")
const participants = document.getElementById("participants")
const address = document.getElementById("sample5_address")
const category = document.querySelector(".category_metting")
const form_data = document.querySelector("#event-form")

document.getElementById("submit-btn-class").addEventListener("click", (e) => {

  const data_obj = {
    "user": user_id,
    "category": category.value,
    "title": title.value,
    "content": content.value,
    "event_image": image.value,
    "tags": tags.value,
    "deadline": deadline_time.value,
    "participants_limit": participants.value,
    "start_event": start_time.value,
    "end_event": end_time.value,
    "location_tags": address.value
  }

  console.log(data_obj)

  fetch("http://127.0.0.1:8000/events/forms/", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data_obj)
  }).then((response) => response.json()).then((data) => console.log(data))


})