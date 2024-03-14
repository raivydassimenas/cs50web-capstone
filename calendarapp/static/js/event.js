document.querySelector("#submitButton").addEventListener("click", () => {
    const description = document.querySelector("#description");
    const place = document.querySelector("#place");
    const date = "{{ date }}"
    const title = document.querySelector("#title")

    const formData = {
        description,
        place,
        date,
        title
    };

    fetch("/insert_event", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
    })
        .then(response => {
            if (response.ok) {
                console.log("Event inserted successfully");
            } else {
                console.log("Error inserting event");
            }
        })
        .catch(error => {
            console.error("Error:", error);
        })
})