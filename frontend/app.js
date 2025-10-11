//const map = L.map('map').setView([10.762622, 106.660172], 12);
//L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

document.getElementById('run').addEventListener('click', async () => {
  const res = await fetch('http://127.0.0.1:8000/api/calculate/', {
    method: "GET",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: "Bro" })
  });
  const data = await res.json();
  console.log(data);
});
