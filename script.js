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




const wheel = document.getElementById('wheel');

// Center Hub for value 1
const hub = document.createElement('div');
hub.className = 'hub';
hub.innerText = '1';
wheel.appendChild(hub);

// Place the peripheral fields for all "3" and the spokes for "2"
const count = circularTable.filter(item => item.value === 3).length;

circularTable.forEach((item, index) => {
		if (item.value === 3) {
				// Calculate angle for the peripheral fields
				const angle = (index / count) * 2 * Math.PI;
				const radius = 150;
				const x = radius * Math.cos(angle) + 200; // 200 is to center it in the container
				const y = radius * Math.sin(angle) + 200;

				const field = document.createElement('div');
				field.className = 'field';
				field.style.left = `${x}px`;
				field.style.top = `${y}px`;
				field.innerText = item.value;
				wheel.appendChild(field);

				// Place spoke for value "2" between the hub and periphery
				const spokeRadius = radius / 2; // Midway between hub and peripheral field
				const spokeX = spokeRadius * Math.cos(angle) + 200;
				const spokeY = spokeRadius * Math.sin(angle) + 200;

				const spoke = document.createElement('div');
				spoke.className = 'spoke';
				spoke.style.left = `${spokeX}px`;
				spoke.style.top = `${spokeY}px`;
				spoke.innerText = '2';
				wheel.appendChild(spoke);
		}
});
