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