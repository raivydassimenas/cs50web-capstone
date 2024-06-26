flatpickr("#datetime", {
  enableTime: true,
  dateFormat: "Y-m-d H:i",
  minDate: "today",
});

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

const csrftoken = getCookie("csrftoken");

document.querySelector("#submitButton").addEventListener("click", (e) => {
  e.preventDefault();

  const description = document.querySelector("#description").value;
  const place = document.querySelector("#place").value;
  const datet = document.querySelector("#datetime").value;
  const title = document.querySelector("#title").value;

  const formData = {
    description,
    place,
    datet,
    title,
  };

  fetch("/insert_event", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(formData),
  })
    .then((response) => {
      if (response.ok) {
        window.location.href = response.url;
      } else {
        return response.json();
      }
    })
    .then((data) => {
      console.log(data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
