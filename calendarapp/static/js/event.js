flatpickr('#datetime', {
            enableTime: true,
            dateFormat: "Y-m-d H:i",
            minDate: "today",
        });

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}


const csrftoken = getCookie('csrftoken');

document.querySelector("#submitButton").addEventListener("click", (e) => {
    e.preventDefault();

    const description = document.querySelector("#description").value;
    const place = document.querySelector("#place").value;
    const datetime = document.querySelector("#datetime").value;
    const title = document.querySelector("#title").value;

    const formData = {
        description,
        place,
        datetime,
        title
    };

    fetch("/insert_event", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
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