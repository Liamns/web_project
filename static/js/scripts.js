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

// let pager = 1;
// let timer = null;

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

// function addNewContent() {
//   $.ajax({
//     type: "GET", // request 전달 방식 (POST, GET 등)
//     url: "http://127.0.0.1:8000/events/",
//     headers: {
//       //헤더에 csrf 토큰 추가
//       "X-CSRFToken": getCookie("csrftoken"),
//     },
//     data: JSON.stringify({
//       // json 형식으로 서버에 데이터 전달
//       "page": pager,
//     }),
//     dataType: "json", // json 형식으로 데이터 주고 받기
//     success: function (result) {
//       const data = JSON.parse(result);
//       // data 반복문으로 태그 넣기
//       for (let i = 0; i < data.length; i++) {
//         let rowData = data[i];
//         const appendNode = `        <div class="col mb-5">
//             <div class="card h-100">
//               <div class="badge bg-dark text-white position-absolute" style="top: 0.5rem; right: 0.5rem">모집중</div>
//               <!-- 모임 이미지 -->
//               {% if event.event_imgage %}
//               <img class="card-img-top" src="${rowData.fields.event_imgage.url}" alt="..." style="height: 200px" />
//               {% else %}
//               <img class="card-img-top" src="" alt="..." />
//               {% endif %}
//               <!-- 모임 내용 디테일-->
//               <div class="card-body p-4">
//                 <div class="text-center">
//                   <!-- 모임 제목 -->
//                   <h5 class="fw-bolder"
//                     style="display: inline-block; width: 180px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
//                     ${rowData.fields.title}</h5><br>
//                   <!-- category-->
//                   ${rowData.fields.category}
//                 </div>
//               </div>
//               <!-- Product actions-->
//               <div class="card-footer p-4 pt-0 border-top-0 bg-transparent">
//                 <div class="text-center">
//                   <a class="btn btn-outline-dark mt-auto" href="{% url 'event_detail' %}">자세히 보기</a>
//                 </div>
//               </div>
//             </div>
//           </div>`;
//         $("#events-list").append(appendNode);
//       }
//       // 가져온 데이터가 18개 이면 더 가져올 데이터가 있다고 판단 다시 관찰 시작
//       // 18개가 아닐경우 더이상 가져올 데이터가 없다고 판단 관찰 중지상태로 끝내기
//       if (data.length === 8) {
//         observer.observe(sentinel);
//       }
//     },
//     error: function (request, status, error) {
//       console.log(
//         `code: ${request.status} \nmessage: ${request.responseText}\nerror: ${error}`
//       );
//       console.dir(request);
//       console.dir(status);
//       console.dir(error);
//       console.log(`request: ${request}`);
//       console.log(`status: ${status}`);
//       console.log(`error: ${error}`);
//     },
//     beforeSend: function () {
//       // ajax 보내기 전
//       console.log("페이지 스크롤 시작");
//       // 통신 시작할 때 관찰 끄기
//       observer.unobserve(sentinel);
//     },
//     complete: function () {
//       // ajax 완료
//       console.log("페이지 스크롤 끝");
//     },
//   });
// }

// // target 선언
// const sentinel = document.querySelector("#sentinel");

// // option 설정
// const option = {
//   root: null, //viewport
//   rootMargin: "0px",
//   threshold: 0.3, // 전체(100%)가 viewport에 들어와야 callback함수 실행
// };

// // callback 함수 정의
// const callback = (entries, observer) => {
//   entries.forEach((entry) => {
//     if (entry.isIntersecting) {
//       pager++; // 2부터 시
//       //console.log(page);
//       addNewContent();
//     }
//   });
// };

// // IntersectionsObserver 생성
// const observer = new IntersectionObserver(callback, option);

// // target 관찰
// observer.observe(sentinel);
// window.addEventListener("scroll", callback, {
//   passive: true
// });