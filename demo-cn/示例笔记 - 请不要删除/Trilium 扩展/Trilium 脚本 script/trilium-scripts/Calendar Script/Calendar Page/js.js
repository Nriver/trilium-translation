
// ---- Options -------------------------------------------

// Edit names for localization
const months = [
    "January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December"
];
const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

// Toggle displaying the current AND next month together
const doubleMonthView = true;

// Add or change events here. Array format: [ Name, icon, icon color ]
const events = [
    ["Test", "bxs-pencil", "#ff4c4c"],
    ["Deadline", "bxs-time", "#ff7b42"],
    ["Meeting", "bxs-briefcase-alt-2", "#dbc745"],
    ["Holiday", "bxs-flag-alt", "#57c94f"],
    ["Birthday", "bxs-cake", "#dd5594"],
    ["Event", "bxs-calendar-alt", "#4bb4cd"],
    ["Note", "bxs-info-circle", "#888"]
]


// ---- Code ----------------------------------------------

const today = new Date();
var currentMonth = today.getMonth();
var currentYear = today.getFullYear();

// Create header row for days of the week
var dayHeader = "<tr>";
for (let day in days) {
    dayHeader += "<th>" + days[day] + "</th>";
}
dayHeader += "</tr>";
document.getElementById("thead-month").innerHTML = dayHeader;

// Calendar buttons
document.getElementById("previous").addEventListener("click", previous);
document.getElementById("next").addEventListener("click", next);
document.getElementById("month").addEventListener("change", jump);
document.getElementById("year").addEventListener("change", jump);

var yearDropdown = "";
for (var i = currentYear-20; i <= currentYear+20; i++) {
    yearDropdown += "<option value='" + i + "'>" + i + "</option>";
}
document.getElementById("year").innerHTML = yearDropdown;

// Get needed HTML elements
const selectYear = document.getElementById("year");
const selectMonth = document.getElementById("month");
const calendarTitle = document.getElementById("monthAndYear");
const table = document.getElementById("calendar-body");


showCalendar(currentMonth, currentYear);



// Displays the given month and year on the calendar.
// Month starts at zero. Both args are numbers.
async function showCalendar(month, year) {
    
    // Used to determine which day of the week the month starts on
    const firstDay = (new Date(year, month)).getDay();
    
    // Used for the double month view.
    // nextYear refers to what year it is next month.
    const nextMonth = (month + 1) % 12;  
    const nextYear = (month === 11) ? year + 1 : year;
    
    // Update the table with new values
    table.innerHTML = "";
    selectYear.value = year;
    selectMonth.value = month;
    if (doubleMonthView) {
        calendarTitle.innerHTML = months[month] + " " + year + 
        "<span style='font-size: 65%'> / " + months[nextMonth] + " " + nextYear+ "</span>";
    } else {
        calendarTitle.innerHTML = months[month] + " " + year;
    }
    
    // Create arrays that will contain the month's day notes 
    // and their attributes.    
    var monthArray = [];
    var attributeArray = [];
    await makeNoteArrays(month, year, monthArray, attributeArray);
    
    if (doubleMonthView) {
        var nextMonthArray = [];
        var nextAttributeArray = [];
        await makeNoteArrays(nextMonth, nextYear, nextMonthArray, nextAttributeArray);
    }

    var date = 1;
    var weekMax = 12;
    var stop = false;
    // Loop for each week (make a table row)
    for (var i = 0; i < weekMax && !stop; i++) {
        
        var row = document.createElement("tr");
        
        // Loop for each day (make a cell for every day)
        for (var j = 0; j < 7 && !stop; j++) {
            
            var cell;
            
            // Cells before 1st of the month (blank square)
            if (i === 0 && j < firstDay) { 
                cell = createBlankCell();
            } 
            // Cells of next month (only drawn if enabled)
            else if (date > daysInMonth(month, year)) {
                if (doubleMonthView) {
                    var nextDate = date - daysInMonth(month, year);

                    // Cells of next NEXT month
                    if (nextDate > daysInMonth(nextMonth, nextYear)) {
                        // Don't draw a completely empty week
                        if (j===0) {
                            stop = true;
                            continue;
                        }
                        cell = createBlankCell();
                        row.appendChild(cell);
                        weekMax = i;
                        continue;
                    }

                    cell = createCell(nextDate, nextMonth, nextYear);
                    applyLink(cell, nextDate, nextMonth, nextYear, nextMonthArray);
                    stylizeCell(cell, nextDate, nextMonthArray, nextAttributeArray);
                    date++;
                } else {
                    // Don't draw a completely empty week
                    if (j===0) {
                        stop = true;
                        continue;
                    }
                    cell = createBlankCell();
                    weekMax = i;
                }
            } 
            // Cells of this month
            else {
                cell = createCell(date, month, year);
                applyLink(cell, date, month, year, monthArray);
                stylizeCell(cell, date, monthArray, attributeArray);
                
                // If current cell is today
                if (date === today.getDate() && year === today.getFullYear() 
                    && month === today.getMonth()) {
                    cell.className = "date-picker selected";
                }

                row.appendChild(cell);
                date++;
            }
            
            row.appendChild(cell);
            
        } // End of day
        
        table.appendChild(row);
        
    } // End of week
}

// Populates monthArray with all existing day notes in that month. Each 
// element's index represents the day. Ex: March 5th is monthArray[5], 
// which would contain a note ID if the page exists.
//
// Also populates attributeArray with any events for the day.
async function makeNoteArrays(month, year, monthArray, attributeArray) {
    
    var monthNote = await api.getMonthNote((month < 9) ? year+"-0"+(month+1) : year+"-"+(month+1) );
    var monthChildren = await monthNote.getChildNotes();
    
    for (let dayNote of monthChildren) {
        var indexDay = Number(dayNote.getLabel("dateNote").value.substring(8, 10)); 
        monthArray[indexDay] = dayNote.noteId;
        
        // Look for events defined by global array (line 15)
        attributeArray[indexDay] = [];
        for (let event of events) {            
            attributeArray[indexDay].push(dayNote.getLabels(event[0]));
        }
        
        
    } 
}

// Returns an empty table cell for squares with no date.
function createBlankCell() {
    var cell = document.createElement("td");
    var cellText = document.createTextNode("");
    cell.className = "date-picker"
    cell.appendChild(cellText);
    return cell;
}

// Returns a cell with the given date.
function createCell(date, month, year) {
    var cell = document.createElement("td");
    cell.setAttribute("data-date", date);
    cell.setAttribute("data-month", month + 1);
    cell.setAttribute("data-year", year);
    cell.setAttribute("data-month_name", months[month]);
    cell.className = "date-picker";
    return cell;
}

// Adds the day number to the cell. Clicking it activates or creates
// the respective day note.
function applyLink(cell, date, month, year, monthArray) {
    
    // Create a string in the format YYYY-MM-DD 
    if (month < 9) {
      var todayStr = year + "-0" + (month + 1);
    } else {
      var todayStr = year + "-" + (month + 1);
    }
    if (date < 10) {
        todayStr = todayStr + "-0" + date;
    } else {
        todayStr = todayStr + "-" + date;
    }
    
    // Use string for 'calendar-date' HTML attribute, which gives the
    // ability to create a day note by clicking the link.
    var link = document.createElement("a");
    link.setAttribute("calendar-date", todayStr);
    link.innerHTML = date;
    link.addEventListener("click", goToDay);
    link.className = 'day-number';
    cell.appendChild(link);
   
    // If a note already exists for this day, make a link to it.
    if (monthArray[date] != undefined) {
        link.setAttribute("data-note-path", monthArray[date]);
    }
    
}

// Looks through the attribute array to create any neccessary event markers
// on the given calendar cell.
function stylizeCell(cell, date, monthArray, attributeArray) {
    
    // Stop if there's no day note on this date
    if (monthArray[date] == undefined) {
        return;
    }
    
    // 'attribute' contains a two-dimensional array.
    // First array dictates which event type it is, second contains event descriptions.
    var attribute = attributeArray[date];
    
    for(let i = 0; i < attribute.length; i++) {
        for(let j = 0; j < attribute[i].length; j++) {
            
            if(attribute[i][j].value != "") {
                var marker = document.createElement("div");
                marker.classList.add("marker");
                var markerIcon = document.createElement("span");
                markerIcon.classList.add("bx");
                
                // Icon is created by adding Box Icon class (see line 15)
                markerIcon.classList.add(events[i][1]);
                markerIcon.classList.add("marker-icon");
                markerIcon.style.color = events[i][2];
                
                marker.appendChild(markerIcon);
                marker.appendChild(document.createTextNode(" "+ attribute[i][j].value ))
                
                // Hover tooltip
                var tooltip = document.createElement("span");
                tooltip.classList.add("marker-tooltip");
                tooltip.appendChild(document.createTextNode(attribute[i][j].value));
                marker.appendChild(tooltip);
                
                cell.appendChild(marker);   
            }
        }  
    }
}

// Returns how many days there are in the given month
function daysInMonth(iMonth, iYear) {
    return 32 - new Date(iYear, iMonth, 32).getDate();
}


// ---- Calendar event handlers ---------------------------

// View the next month
function next() {
    currentYear = (currentMonth === 11) ? currentYear + 1 : currentYear;
    currentMonth = (currentMonth + 1) % 12;
    showCalendar(currentMonth, currentYear);
}

// View the previous month
function previous() {
    currentYear = (currentMonth === 0) ? currentYear - 1 : currentYear;
    currentMonth = (currentMonth === 0) ? 11 : currentMonth - 1;
    showCalendar(currentMonth, currentYear);
}

// View a month specified from the calendar controls
function jump() {
    currentYear = parseInt(selectYear.value);
    currentMonth = parseInt(selectMonth.value);
    showCalendar(currentMonth, currentYear);
}

// Activate the clicked day note
async function goToDay() {
    var day = await api.getDateNote(event.currentTarget.getAttribute("calendar-date"));
    api.activateNote(day.noteId);
}

