document.addEventListener('DOMContentLoaded', function () {
    var tasksInput = document.getElementById('tasks');
    tasksInput.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            tasksInput.value += '\n- ';
        }
    });
    tasksInput.value = '- ';  // Initialize with a starting task
});
function updateDayName() {
    var selectedDate = document.getElementById("choose_date").value;
    var dateObj = new Date(selectedDate);
    var days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    var dayName = days[dateObj.getDay()];
    document.getElementById("day_name").innerText = dayName;
}
