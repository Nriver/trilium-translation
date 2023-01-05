// --- Configuration ----------------------------------------------------

// Time range to display for timetable
const startTime = "7:00";
const endTime = "19:00";

// Labels for days of the week. The timetable will have one
// column for every entry here.
const headersArray = [
    "MON",
    "TUE",
    "WED",
    "THU",
    "FRI"
]

// Two-dimensional array representing events.
// Array format: [ event name, day of week, start time, end time, color ]
const eventArray = [
    [ "Example event", 1, "11:00", "14:00", "#3366AA"],
    [ "Thursday 1", 3, "9:30", "12:00", "#668811"],
    [ "Thursday 2", 3, "12:00", "13:30", "#668811"]
];

// Labels for each 30-minute block. By default, blocks are labeled in
// one hour intervals.
const timesArray = [
    "0:00", "",
    "1:00",  "",
    "2:00",  "",
    "3:00",  "",
    "4:00",  "",
    "5:00",  "",
    "6:00",  "",
    "7:00",  "",
    "8:00",  "",
    "9:00",  "",
    "10:00",  "",
    "11:00",  "",
    "12:00",  "",
    "13:00",  "",
    "14:00",  "",
    "15:00",  "",
    "16:00",  "",
    "17:00",  "",
    "18:00",  "",
    "19:00",  "",
    "20:00",  "",
    "21:00",  "",
    "22:00",  "",
    "23:00",  "",
    "00:00",  ""
];




// ---- Code ---------------------------------------------------------------

// A block's position in a day's column is used to locate said block. 
// So if the schedule starts at 7:00, then 7:00-7:30 will be block 0 
// and 7:30-8:00 will be block 1.

// Two-dimensional array representing X and Y 
// coordinates of blocks on the timetable.
var blockArray = [];

createTable();
addEvents();

// Create the empty timetable with columns for each day (and one
// column for the time).
function createTable() {

    var table = document.createElement("table");
    table.id = "timetable";
    document.getElementById("schedule-wrapper").appendChild(table);

    // Table header
    var header = document.createElement("tr");
    header.className = "schedule-header";
    addToTable(header);

    // Time column header
    var timehead = document.createElement("th");
    timehead.className = "schedule-corner";
    header.appendChild(timehead);

    // Add labels for days of the week
    for (let i = 0; i < headersArray.length; i++) {
        var heading = document.createElement("th");
        heading.className = "schedule-heading";
        heading.appendChild(document.createTextNode(headersArray[i]));
        header.appendChild(heading);
    }

    var tableBlocks = timeToBlockCount(startTime, endTime);

    // Cells
    for (let i = 0; i < tableBlocks; i++) {
        var row = makeRow(i);
        addToTable(row);
        blockArray[i] = [];

        // Time column
        var cell = document.createElement("td");
        cell.className = "schedule-time";
        // Create time label
        var label = timesArray[ Number(startTime.split(":")[0]) * 2 + i ];
        cell.appendChild(document.createTextNode(label));
        row.appendChild(cell);

        for (let j = 0; j < headersArray.length; j++) {
            var cell = makeCell(i, j);
            row.appendChild(cell);
            blockArray[i][j] = cell;
        }
    }
}

// Add events from the global events array to the timetable.
function addEvents() {

    // Iterate through each event and add to table
    for (let event of eventArray) {

        // Retrieve starting cell
        var cell = blockArray[ timeToBlockPosition(event[2]) ][ event[1] ];

        // Apply styling
        expandBlock(cell, timeToBlockCount(event[2], event[3]));
        cell.style.backgroundColor = event[4];
        cell.appendChild(document.createTextNode(event[0]));

    }
}



// ---- Helper Functions -------------------------------------------------

// Returns the position of a block found at a given time (in)
function timeToBlockPosition(time) {
    var parts = time.split(":");
    return(parts[0] - startTime.split(":")[0]) * 2 + (parts[1] / 30);
}

// Returns how many 30-minute blocks the given hour range needs
function timeToBlockCount(start, end) {
    var startParts = start.split(":");
    var endParts = end.split(":");
    var minutesSum;
    if (startParts[1] == endParts[1]) 
        minutesSum = 0;
     else if (startParts[1] > endParts[1]) 
        minutesSum = -1;
     else 
        minutesSum = 1;
    
    return(((endParts[0] - startParts[0]) * 2) + minutesSum);
}

function addToTable(element) {
    document.getElementById("timetable").appendChild(element);
}

function makeCell(x, y) {
    var element = document.createElement("td");
    element.id = x + "," + y;
    element.className = "schedule-cell";
    return element;
}

function makeRow(id) {
    var element = document.createElement("tr");
    element.id = id;
    element.className = "schedule-row";
    return element;
}

function deleteCell(cell) {
    cell.parentNode.removeChild(cell);
}

function getBlockCol(cell) {
    return Number(cell.id.split(",")[1]);
}

function getBlockPos(cell) {
    return Number(cell.id.split(",")[0]);
}

// Merges the given cell with X amount of cells downward
function expandBlock(cell, amount) {
    cell.setAttribute("rowspan", amount);

    var pos = getBlockPos(cell);
    var col = getBlockCol(cell);
    for (let i = 1; i < amount; i++) {
        deleteCell(blockArray[pos + i][col]);
    }
}
