function addPost(e) {
    e.preventDefault();;

    fetch("/new_post", {
        method: "POST",
        body: JSON.stringify({
            title: document.querySelector("#title").value,
            body: document.querySelector("#body").value
        })
    })
        .then(response => {
            location.reload();
            return response.json();
        })
        .catch(error => error.message ? error.message : error)
}


document.querySelector("#new-post-form").addEventListener("submit", addPost);

document.querySelectorAll(".edit-post").forEach(button => button.addEventListener("click", (e) => {
    let postBody = button.parentElement.querySelector(".post-body");
    let newPostBody = document.createElement('textarea');
    newPostBody.innerText = postBody.innerText;

    postBody.parentNode.replaceChild(newPostBody, postBody);
    button.innerText = "Save changes";
    button.addEventListener("click", (e) => {
        fetch("/update_post/" + button.id, {
            method: "PUT",
            body: JSON.stringify({
                body: newPostBody.value
            })
        })
            .then(response => {
                console.log(newPostBody.value);
                location.reload();
                return response.json();
            })
            .catch(error => error.message ? error.message : error);
    });
}));