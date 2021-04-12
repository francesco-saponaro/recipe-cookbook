//Get added image URL
let url = document.getElementById("recipe-img").src;
//Get image outer container
let imgContainer = document.getElementById("img-container")

//Check if the URL is wrong by checking for a 404 error, if so  add class to container
//and replace image tag with with error info headers
function checkImage(url, cont) {
  var request = new XMLHttpRequest();
  request.open("GET", url, true);
  request.send();
  request.onload = function() {
    status = request.status;
    if (request.status == 404) { 
      cont.className = "image-error-text col s8 offset-s2"
      cont.innerHTML = `
        <h3 class="center-align small-error-first">Oops! 404 Error...<i class="far fa-sad-cry"></i></h3>
        <h5 class="center-align small-error-second">The uploaded image URL is invalid</h5>`;
    } 
  }
}

checkImage(url, imgContainer);