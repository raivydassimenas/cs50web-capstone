function loadAllPosts() {
    fetch("/all_posts")
        .then(response => response.json())
        .then(results => {
            results.forEach(item => {
                const post = document.createElement("div");
                post.classList.add("border", "mb-1", "p-1");

                const title = document.createElement("h3")
                title.innerText = item.title;
                const author = document.createElement("p");
                author.innerText = "Written by: " + item.author;
                const body = document.createElement("p");
                body.innerText = item.body;
                const likes = document.createElement("p")
                likes.innerText = "Likes: " + item.likes;
                const createdAt = document.createElement("p");
                createdAt.innerText = "Created at: " + item.created;

                post.append(title, author, body, likes, createdAt);
                document.querySelector("#all-posts").append(post);
            })
        })
        .catch(err => err.message ? err.message : err);
}

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

loadAllPosts();