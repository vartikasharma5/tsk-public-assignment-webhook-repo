let lastTimestamp = null;

function fetchEvents() {
  fetch("/webhook/events")
    .then(res => res.json())
    .then(data => { 
      const ul = document.getElementById("events");

      data.forEach(e => {
        if (lastTimestamp && e.timestamp <= lastTimestamp) return;

        let text = "";

        if (e.event_type === "push") {
          text = `${e.author} pushed to ${e.to_branch} on ${new Date(e.timestamp).toUTCString()}`;
        }

        if (e.event_type === "pull_request") {
          text = `${e.author} submitted a pull request from ${e.from_branch} to ${e.to_branch} on ${new Date(e.timestamp).toUTCString()}`;
        }

        if (e.event_type === "merge") {
          text = `${e.author} merged ${e.from_branch} to ${e.to_branch} on ${new Date(e.timestamp).toUTCString()}`;
        }

        ul.innerHTML += `<li>${text}</li>`;
      });

      if (data.length > 0) {
        lastTimestamp = data[0].timestamp;
      }
    });
}

setInterval(fetchEvents, 15000);
fetchEvents();

