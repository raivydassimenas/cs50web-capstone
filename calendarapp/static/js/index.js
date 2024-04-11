const daysContainer = document.querySelector("#days-container");
daysContainer.innerHTML = '';

let currentDate = new Date();
currentDate.setDate(1);
const firstDayOfMonth = currentDate.getDay();

let currentMonth = new Date().getMonth();
currentDate.setMonth(currentMonth + 1);
currentDate.setDate(0);
const numDays = currentDate.getDate();

const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
weekdays.forEach(day => {
    const dayElement = document.createElement('div');
    dayElement.classList.add('font-bold');
    dayElement.innerText = day;
    daysContainer.appendChild(dayElement);
});

for (let day = 1; day <= numDays; day++) {
    const dayElement = document.createElement('a');
    dayElement.innerText = day;
    let date = new Date(`${currentDate.getFullYear()}-${currentDate.getMonth()}-${day}`);
    const dateString = date.toISOString();
    const encodedDateString = encodeURIComponent(dateString);
    dayElement.href = `/insert_event/${encodedDateString}`;
    if (day === 1) {
        dayElement.classList.add(`col-start-${firstDayOfMonth + 1}`);
    }
    daysContainer.appendChild(dayElement);
}