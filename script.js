function updateDateTime() {
	const datetimeElement = document.getElementById('datetime');
	const now = new Date();
	datetimeElement.textContent = now.toLocaleString();
}

setInterval(updateDateTime, 1000);
updateDateTime(); // Call immediately to avoid delay


