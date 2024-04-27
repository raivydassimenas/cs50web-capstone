let DateTime = luxon.DateTime;

const eventDatesList = JSON.parse(
  document.querySelector("#event_list_data").textContent,
);

const daysContainer = document.querySelector("#days-container");
daysContainer.innerHTML = "";

let currentDate = new Date();
currentDate.setDate(1);
const firstDayOfMonth = currentDate.getDay();

let currentMonth = new Date().getMonth();
currentDate.setMonth(currentMonth + 1);
currentDate.setDate(0);
const numDays = currentDate.getDate();

const weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
weekdays.forEach((day) => {
  const dayElement = document.createElement("div");
  dayElement.classList.add("font-bold");
  dayElement.innerText = day;
  daysContainer.appendChild(dayElement);
});

for (let day = 1; day <= numDays; day++) {
  const dayElement = document.createElement("a");
  dayElement.innerText = day.toString();
  date = new Date();
  date.setDate(day);
  encodedDate = encodeURIComponent(date.toUTCString());
  const dt = DateTime.fromISO(date.toISOString()).toFormat("yyyy-MM-dd");
  if (eventDatesList.includes(dt)) {
    dayElement.classList.add("hover:text-green-800");
    console.log(dayElement.innerText);
  } else {
    dayElement.classList.add("hover:text-black");
  }

  dayElement.href = `/day_list/${encodedDate}`;
  if (day === 1) {
    dayElement.classList.add(`col-start-${firstDayOfMonth + 1}`);
  }
  daysContainer.appendChild(dayElement);
}
