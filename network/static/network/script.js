function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);

    if (parts.length == 2) return parts.pop().split(";").shift();
}

function editPost(id) {
    const postValue = document.querySelector(`#textarea_${id}`).value;
    const content = document.querySelector(`#content_${id}`);
    const modal = document.querySelector(`#modal_edit_post_${id}`);
    const main = document.querySelector("main");

    fetch(`/edit/${id}`, {
        method: "POST",
        headers: { "Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken") },
        body: JSON.stringify({
            content: postValue,
        }),
    })
        .then((response) => response.json())
        .then((result) => {
            content.innerHTML = result.data;
        });
}

function likePost(id) {
    const btn = document.querySelector(`#btn-like-${id}`);
    const liked = btn.dataset.liked === "true";
    const likesCounter = document.querySelector(`#likes-counter-${id}`);

    if (liked) {
        fetch(`/unlike/${id}`)
            .then((response) => response.json())
            .then((result) => {
                btn.classList.remove("bi-heart-fill");
                btn.classList.add("bi-heart");
                btn.style.color = "";
                btn.dataset.liked = "false";
                likesCounter.innerHTML = `${result.likes_count} Likes`;
            });
    } else {
        fetch(`/like/${id}`)
            .then((response) => response.json())
            .then((result) => {
                btn.classList.remove("bi-heart");
                btn.classList.add("bi-heart-fill");
                btn.style.color = "red";
                btn.dataset.liked = "true";
                likesCounter.innerHTML = `${result.likes_count} Likes`;
            });
    }
}