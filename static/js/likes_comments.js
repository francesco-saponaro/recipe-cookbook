//Get form's like button
let likesButtons = document.querySelectorAll('.like-btn');

//Change Icon class and input value on click
likesButtons.forEach(likeButton => {
    likeButton.addEventListener('click', e => {
        if (e.target.classList.contains('far')) {
            e.target.classList.remove('far');
            e.target.classList.add('fas');
            e.target.previousElementSibling.value = true;
        } else {
            e.target.classList.remove('fas');
            e.target.classList.add('far');
            e.target.previousElementSibling.value = false;
        }
    });
});





