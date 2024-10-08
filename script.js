function updateDateTime() {
	const datetimeElement = document.getElementById('datetime');
	const now = new Date();
	datetimeElement.textContent = now.toLocaleString();
}

setInterval(updateDateTime, 1000);
updateDateTime(); // Call immediately to avoid delay


document.querySelector('.start-button').addEventListener('click', () => {
  alert('Starting Your Adventure!');
  // Redirect or trigger any action here
});
