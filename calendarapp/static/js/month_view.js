let DateTime = luxon.DateTime;
const urlParams = new URLSearchParams(window.location.search);

const year = JSON.parse(document.querySelector("#year").textContent);
const month = JSON.parse(document.querySelector("#month").textContent);
const eventDatesList = JSON.parse(
  document.querySelector("#event_list_data").textContent,
);

const daysContainer = document.querySelector("#days-container");
daysContainer.innerHTML = "";

const weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
weekdays.forEach((day) => {
  const dayElement = document.createElement("div");
  dayElement.classList.add("font-bold");
  dayElement.innerText = day;
  daysContainer.appendChild(dayElement);
});

const numDays = new Date(year, month, 0).getDate();

const firstDayOfMonth = new Date(year, month - 1, 1).getDay();

for (let day = 1; day <= numDays; day++) {
  const dayElement = document.createElement("a");
  dayElement.innerText = day.toString();
  date = new Date(year, month - 1, day);
  const dt = DateTime.fromISO(date.toISOString()).toFormat("yyyy-MM-dd");
  const encodedDate = encodeURIComponent(dt);
  if (eventDatesList.includes(dt)) {
    dayElement.style.color = "blue";
  } else {
    dayElement.style.color = "black";
  }

  dayElement.href = `/day_list/${encodedDate}`;
  if (day === 1) {
    dayElement.classList.add(`col-start-${firstDayOfMonth + 1}`);
  }
  daysContainer.appendChild(dayElement);
}
