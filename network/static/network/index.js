function addPost(e) {
    e.preventDefault();

    console.log('inside add post');

    fetch("/new_post", {
        method: "POST",
        body: JSON.stringify({
            title: document.querySelector("#title").value,
            body: document.querySelector("#body").value
        })
    })
        .then(response => {
            console.log('after request');
            return response.json();
        })
        .then(result => {
            loadAllPosts();
        })
        .catch(error => error.message ? error.message : error)
}


document.querySelector("#new-post-form").addEventListener("submit", addPost);