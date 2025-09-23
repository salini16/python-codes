<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Air Quality Alert System</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    body { background:#f9fafb; font-family:'Segoe UI',sans-serif; }
    .card { border-radius:16px; box-shadow:0 4px 15px rgba(0,0,0,.1); }
    .gauge { width:200px;height:200px;border-radius:50%;margin:auto;position:relative;
             display:flex;align-items:center;justify-content:center;
             background:conic-gradient(#22c55e 0deg 120deg,#eab308 120deg 240deg,#ef4444 240deg 360deg);}
    .gauge span { position:absolute;font-size:22px;font-weight:bold;text-align:center;color:#333; }
    .forecast-card { border-radius:10px;padding:10px;margin:5px;flex:1;text-align:center;color:#fff;font-weight:bold;}
    .good{background:#22c55e;} .moderate{background:#eab308;} .unhealthy{background:#ef4444;}
  </style>
</head>
<body>
<div class="container py-4">
  <h2 class="text-center text-primary fw-bold mb-4">🌍 Air Quality Alert System</h2>
  
  <!-- City Selector -->
  <div class="d-flex justify-content-center mb-4">
    <select id="citySelect" class="form-select w-50">
      <option value="Delhi">Delhi</option>
      <option value="Chennai">Chennai</option>
      <option value="Hyderabad">Hyderabad</option>
      <option value="Mumbai">Mumbai</option>
      <option value="Bengaluru">Bengaluru</option>
      <option value="Kolkata">Kolkata</option>
      <option value="Pune">Pune</option>
      <option value="Jaipur">Jaipur</option>
      <option value="Ahmedabad">Ahmedabad</option>
      <option value="Lucknow">Lucknow</option>
      <option value="Patna">Patna</option>
    </select>
  </div>

  <!-- Dashboard -->
  <div class="row g-4">
    <!-- Gauge -->
    <div class="col-md-4">
      <div class="card p-3 text-center">
        <h5 id="stationName">City</h5>
        <div class="gauge"><span id="aqiValue">0<br><small>Status</small></span></div>
      </div>
    </div>

    <!-- Forecast -->
    <div class="col-md-8">
      <div class="card p-3">
        <h5>7-Day Forecast</h5>
        <div class="d-flex flex-wrap" id="forecastBox"></div>
      </div>
    </div>
  </div>

  <!-- Pollutants -->
  <div class="row g-4 mt-2">
    <div class="col-md-8">
      <div class="card p-3">
        <h5>Pollutant Concentrations</h5>
        <canvas id="pollutantChart" height="100"></canvas>
      </div>
    </div>

    <!-- Alerts -->
    <div class="col-md-4">
      <div class="card p-3">
        <h5>Active Alerts</h5>
        <ul id="alertsList" class="list-group"></ul>
      </div>
    </div>
  </div>
</div>

<script>
  // Mock Data for Cities (You can link to real API later)
  const cityData = {
    "Delhi": {
      aqi: 160,
      forecast:[50,60,120,150,160,180,140],
      pollutants:{ "00:00":{pm25:40,pm10:80,o3:60},
                   "06:00":{pm25:60,pm10:90,o3:70},
                   "12:00":{pm25:100,pm10:150,o3:80},
                   "18:00":{pm25:120,pm10:160,o3:85},
                   "24:00":{pm25:90,pm10:140,o3:75} }
    },
    "Chennai": {
      aqi: 90,
      forecast:[40,50,80,70,90,95,85],
      pollutants:{ "00:00":{pm25:20,pm10:40,o3:30},
                   "06:00":{pm25:25,pm10:45,o3:35},
                   "12:00":{pm25:35,pm10:55,o3:50},
                   "18:00":{pm25:40,pm10:60,o3:55},
                   "24:00":{pm25:30,pm10:50,o3:40} }
    },
    "Hyderabad": {
      aqi: 110,
      forecast:[60,70,85,95,100,110,120],
      pollutants:{ "00:00":{pm25:25,pm10:55,o3:40},
                   "06:00":{pm25:30,pm10:60,o3:50},
                   "12:00":{pm25:50,pm10:90,o3:70},
                   "18:00":{pm25:60,pm10:100,o3:75},
                   "24:00":{pm25:55,pm10:95,o3:65} }
    },
    "Mumbai": {
      aqi: 75,
      forecast:[40,55,60,70,80,85,75],
      pollutants:{ "00:00":{pm25:15,pm10:30,o3:25},
                   "06:00":{pm25:20,pm10:35,o3:30},
                   "12:00":{pm25:30,pm10:50,o3:40},
                   "18:00":{pm25:35,pm10:55,o3:45},
                   "24:00":{pm25:25,pm10:45,o3:35} }
    }
    // ➕ Add more cities here
  };

  let chart;

  function loadCity(city){
    const data = cityData[city];
    if(!data) return;

    // AQI Status
    let status="Good";
    if(data.aqi<=50) status="Good";
    else if(data.aqi<=100) status="Moderate";
    else status="Unhealthy";

    // Gauge
    document.getElementById("stationName").textContent=city;
    document.getElementById("aqiValue").innerHTML=`${data.aqi}<br><small>${status}</small>`;

    // Forecast
    const days=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"];
    const box=document.getElementById("forecastBox");
    box.innerHTML="";
    data.forecast.forEach((aqi,i)=>{
      let cls=aqi<=50?"good":aqi<=100?"moderate":"unhealthy";
      box.innerHTML+=`<div class="forecast-card ${cls}">${days[i]}<br>AQI ${aqi}</div>`;
    });

    // Alerts
    const alerts=[];
    if(data.aqi>100) alerts.push("⚠️ Unhealthy for Sensitive Groups");
    if(data.aqi>150) alerts.push("🚨 High Pollution Levels Expected");
    if(data.aqi<=100) alerts.push("✅ Moderate Air Quality");
    const alertBox=document.getElementById("alertsList");
    alertBox.innerHTML="";
    alerts.forEach(a=>{alertBox.innerHTML+=`<li class="list-group-item">${a}</li>`;});

    // Pollutant Chart
    const ctx=document.getElementById("pollutantChart").getContext("2d");
    if(chart) chart.destroy();
    chart=new Chart(ctx,{
      type:"line",
      data:{
        labels:Object.keys(data.pollutants),
        datasets:[
          {label:"PM2.5",data:Object.values(data.pollutants).map(p=>p.pm25),borderColor:"#ef4444",fill:false},
          {label:"PM10",data:Object.values(data.pollutants).map(p=>p.pm10),borderColor:"#3b82f6",fill:false},
          {label:"O₃",data:Object.values(data.pollutants).map(p=>p.o3),borderColor:"#22c55e",fill:false}
        ]
      },
      options:{responsive:true,
        plugins:{legend:{labels:{color:"#333"}}},
        scales:{x:{ticks:{color:"#333"}},y:{ticks:{color:"#333"},beginAtZero:true}}}
    });
  }

  // Load first city on page load
  document.getElementById("citySelect").addEventListener("change",e=>loadCity(e.target.value));
  loadCity("Delhi");
</script>
</body>
</html>
