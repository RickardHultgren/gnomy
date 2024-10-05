function updateDateTime() {
	const datetimeElement = document.getElementById('datetime');
	const now = new Date();
	datetimeElement.textContent = now.toLocaleString();
}

setInterval(updateDateTime, 1000);
updateDateTime(); // Call immediately to avoid delay





const circularTable = [
		{ position: 'top', value: 1 }, { position: 'top', value: 2 }, { position: 'top', value: 3 },
		{ position: 'top-right', value: 1 }, { position: 'top-right', value: 2 }, { position: 'top-right', value: 3 },
		{ position: 'right', value: 1 }, { position: 'right', value: 2 }, { position: 'right', value: 3 },
		{ position: 'bottom-right', value: 1 }, { position: 'bottom-right', value: 2 }, { position: 'bottom-right', value: 3 },
		{ position: 'bottom', value: 1 }, { position: 'bottom', value: 2 }, { position: 'bottom', value: 3 },
		{ position: 'bottom-left', value: 1 }, { position: 'bottom-left', value: 2 }, { position: 'bottom-left', value: 3 },
		{ position: 'left', value: 1 }, { position: 'left', value: 2 }, { position: 'left', value: 3 },
		{ position: 'left-top', value: 1 }, { position: 'left-top', value: 2 }, { position: 'left-top', value: 3 }
];



