const server = "http://localhost:8080";

async function login(event){
  event.preventDefault();
  let myform = event.target.elements;

  let data = {
    username: myform['username'].value,
    password: myform['password'].value,
  };

  url = server + "/auth";
  
  result = await postData(url, data)
  if (result){
    url = server + "/";
    window.location.href = url;
  }else{
    url = server + "/login";
    window.location.href = url;
  }
}

async function signup(event){
  event.preventDefault();
  let myform = await event.target.elements;

  let data = {
    username: myform['username'].value,
    password: myform['password'].value,
    email: myform['email'].value,
    fname: myform['fname'].value,
    lname: myform['lname'].value
  };

  url = server + "/signup";
  
  result = await postData(url, data)
  if (result){
    url = server + "/login";
    window.location.href = url;
  }else{
    url = server + "/login?signup";
    window.location.href = url;
  }
}

//Rate Instructor
async function rateInstructor(event, instid){
  event.preventDefault();
  let myform = event.target.elements;

  let data = {
    rating1 : myform['rating1'].value, 
    rating2 : myform['rating2'].value, 
    rating3 : myform['rating3'].value, 
    rating4 : myform['rating4'].value, 
    rating5 : myform['rating5'].value, 
    rating6 : myform['rating6'].value, 
    rating7 : myform['rating7'].value, 
    rating8 : myform['rating8'].value, 
    rating9 : myform['rating9'].value, 
    rating10 : myform['rating10'].value, 
    rating11 : myform['rating11'].value 
  }

  url = server + "/myratings/" + instid;

  result = await postData(url, data);

  url = server + "/ratings/" + instid;
  window.location.href = url;
}

//Updating Teaching Style
async function updateTeaching(event, instid){
  event.preventDefault();
  let myform = event.target.elements;
  let data = {
    section : "teaching",
    rating1 : myform['rating1'].value, 
    rating2 : myform['rating2'].value, 
    rating3 : myform['rating3'].value, 
    rating4 : myform['rating4'].value, 
    rating5 : myform['rating5'].value, 
    rating6 : myform['rating6'].value
  }

  url = server + "/myratings/" + instid;

  await putData(url, data);

  url = server + "/ratings/" + instid;
  window.location.href = url;
}

//Update Personality
async function updatePersonality(event, instid){
  event.preventDefault();
  let myform = event.target.elements;
  let data = {
    section : "personality",
    rating7 : myform['rating7'].value, 
    rating8 : myform['rating8'].value, 
    rating9 : myform['rating9'].value, 
    rating10 : myform['rating10'].value, 
    rating11 : myform['rating11'].value
  }

  url = server + "/myratings/" + instid;

  await putData(url, data);

  url = server + "/ratings/" + instid;
  window.location.href = url;
}

//Remove Rating
async function deleteRating(instid){
  choice = confirm("Are you sure you want to remove your rating for this instructor?");
  if (choice){
    url = server + "/myratings/" + instid;
    await deleteData(url);
    url = server + "/ratings/" + instid;
    window.location.href = url;
  }
}

async function postData(url, data){
  try{
    let response = await fetch(
      url,
      {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {'Content-Type' : 'application/json'}
      },
    );
    console.log(response)
    return response.ok;
  }catch(error){
    console.log(error);
    return false;
  }
}

async function putData(url, data){
  try{
    let response = await fetch(
      url,
      {
        method: 'PUT',
        body: JSON.stringify(data),
        headers: {'Content-Type' : 'application/json'}
      },
    );
    console.log(response);
  }catch(error){
    console.log(error);
  }
}

async function deleteData(url){
  try{
    let response = await fetch(
      url,
      {
        method: 'DELETE'
      },
    );
    console.log(response);
  }catch(error){
    console.log(error);
  }
}

/*
async function getData(url){
  try{
    let response = await fetch(url);
    let result = await response.json(); //.text()
    
    console.log(result); //do somthing
  }catch(error){
    console.log(error);
  }
}*/

function initCharts(rating){
  data = [rating.rating1, rating.rating2, rating.rating3, rating.rating4, rating.rating5, rating.rating6];
  drawChart(data);
  data = [rating.rating7, rating.rating8, rating.rating9, rating.rating10, rating.rating11]
  drawFigure(data);
}

function drawChart(data){
  var myChart = Highcharts.chart('chartBar', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Instructor Teaching Skill Rating Summary'
    },
    xAxis: {
        categories: ['Presentation', 'Material Accessability', 'Material Coverage', 'Pacing', 'Conciseness', 'Practical Demonstation']
    },
    yAxis: {
        title: {
            text: 'Teaching Style'
        },
        max: 5,
        min: 0,
        tickInterval: 1
    },
    legend: {
      enabled: false
    },
    series: [{
        name: 'Rating Score',
        data: data
    }],
  });
}

function drawFigure(data){
  Highcharts.chart('chartSpider', {

    chart: {
      polar: true,
      type: 'line',
    },

      title: {
      text: 'Instructor Personality Rating Summary'
    },

    pane: {
      size: '100%'
    },

    xAxis: {
      categories: ['Helpful', 'Friendly', 'Interesting', 'Enthusiasm',
        'Expertise'],
      tickmarkPlacement: 'on',
      lineWidth: 0
    },

    yAxis: {
      gridLineInterpolation: 'polygon',
      lineWidth: 0,
      max: 6,
      min: 0,
      tickInterval: 1
    },

    tooltip: {
      split: false,
      pointFormat: '<span style="color:{series.color}">{point.y}</span>'
    },

    legend: {
      enabled: false
      /*
      align: 'right',
      verticalAlign: 'middle',
      layout: 'vertical'*/
    },

    series: [{
      name: 'Rating Score',
      data: [data[0], data[1], data[2], data[3], data[4]],
      pointPlacement: 'on'
    }],

    responsive: {
      rules: [{
        condition: {
          maxWidth: 500
        },
        chartOptions: {
          legend: {
            align: 'center',
            verticalAlign: 'bottom',
            layout: 'horizontal'
          },
          pane: {
            size: '70%'
          }
        }
      }]
    }

  });
}

//modal show
function modalShow(modalId){
  modal = document.querySelector(modalId);
  modal.style.display = "block";
}

//modal hide
function modalHide(modalId){
  modal = document.querySelector(modalId);
  modal.style.display = "none";
}

//window modal hide
window.onclick = function(event) {
  if (event.target.classList.contains("modal")) {
    event.target.style.display = "none";
  }
}

//favorites
function checkFavorites(favorites, count){
  fav = document.querySelector('#favCheckBox');
  if (fav.checked == true){
    for (num = 1; num<=count; num++){
      console.log(`#inst${num}`);
      document.querySelector(`#inst${num}`).style.display = "none";
    }
    for (favorite in favorites){
      favorite = JSON.stringify(favorites[favorite]);
      favorite = JSON.parse(favorite);
      console.log(favorite["instructorid"]);
      document.querySelector(`#inst${favorite["instructorid"]}`).style.display = "";
    }
  }else{
    for (num = 1; num<=count; num++){
      document.querySelector(`#inst${num}`).style.display = "";
    }
  }
  
}

//Tabs
function openTab(evt, cityName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}