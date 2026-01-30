const eventsContainer = document.getElementById('events');
const countdownEl = document.getElementById('countdown');
let countdown = 15;

function renderEvents(events) {
    if (!events || events.length === 0) {
        eventsContainer.innerHTML = '<div class="empty">No events yet. Waiting for webhook data...</div>';
        return;
    }

    eventsContainer.innerHTML = events.map(event => {
        let message = '';
        if (event.action === 'PUSH') {
            message = `<code>${event.author}</code> pushed to <code>${event.to_branch}</code>`;
        } else if (event.action === 'PULL_REQUEST') {
            message = `<code>${event.author}</code> submitted a pull request from <code>${event.from_branch}</code> to <code>${event.to_branch}</code>`;
        } else if (event.action === 'MERGE') {
            message = `<code>${event.author}</code> merged branch <code>${event.from_branch}</code> to <code>${event.to_branch}</code>`;
        }

        return `
            <div class="event">
                <span class="event-type ${event.action.toLowerCase()}">${event.action.replace('_', ' ')}</span>
                <strong>${event.author}</strong>
                <div class="event-message">${message}</div>
                <div class="event-time">${event.timestamp}</div>
            </div>
        `;
    }).join('');
}

async function fetchEvents() {
    try {
        const response = await fetch('/api/events');
        const events = await response.json();
        renderEvents(events);
    } catch (error) {
        eventsContainer.innerHTML = '<div class="empty">Error loading events. Retrying...</div>';
    }
}

function tick() {
    countdown--;
    if (countdown <= 0) {
        countdown = 15;
        fetchEvents();
    }
    countdownEl.textContent = `Refreshing in ${countdown}s`;
}

fetchEvents();
setInterval(tick, 1000);
