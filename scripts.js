// Load events from localStorage
function loadEvents() {
    const events = localStorage.getItem('events');
    return events ? JSON.parse(events) : [];
}

// Save events to localStorage
function saveEvents(events) {
    localStorage.setItem('events', JSON.stringify(events));
}

// Render events list in the UI
function renderEvents() {
    const events = loadEvents();
    const eventList = document.getElementById('event-list');
    eventList.innerHTML = '';

    events.forEach((event, index) => {
        const li = document.createElement('li');
        li.innerHTML = `
            <strong>${event.EventName}</strong> (Start Time: ${event.StartTime})
            <button onclick="editEvent(${index})">Edit</button>
            <button onclick="deleteEvent(${index})">Delete</button>
        `;
        eventList.appendChild(li);
    });
}

// Add a new event
function addEvent(event) {
    const events = loadEvents();
    events.push(event);
    saveEvents(events);
    renderEvents();
}

// Edit an existing event
function editEvent(index) {
    const events = loadEvents();
    const event = events[index];
    document.getElementById('event_name').value = event.EventName;
    document.getElementById('start_time').value = event.StartTime;
    document.getElementById('custom_function').value = event.CustomFunction;

    // Change the form's action to update the event
    const form = document.getElementById('event-form');
    form.onsubmit = function (e) {
        e.preventDefault();
        events[index] = {
            EventName: document.getElementById('event_name').value,
            StartTime: document.getElementById('start_time').value,
            CustomFunction: document.getElementById('custom_function').value
        };
        saveEvents(events);
        renderEvents();
        form.reset();
        form.onsubmit = addNewEvent;
    };
}

// Delete an event
function deleteEvent(index) {
    const events = loadEvents();
    events.splice(index, 1);
    saveEvents(events);
    renderEvents();
}

// Handle form submission to add new event
function addNewEvent(e) {
    e.preventDefault();

    const event = {
        EventName: document.getElementById('event_name').value,
        StartTime: document.getElementById('start_time').value,
        CustomFunction: document.getElementById('custom_function').value,
    };

    addEvent(event);

    // Clear the form after submission
    document.getElementById('event-form').reset();
}

// Initialize event manager
document.getElementById('event-form').onsubmit = addNewEvent;
renderEvents();  // Initially render the events
