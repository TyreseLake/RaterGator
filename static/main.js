const server = "https://safe-shore-44211.herokuapp.com";

document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.modal');
  var instances = M.Modal.init(elems);
});

document.addEventListener('DOMContentLoaded', function() {
  var el = document.querySelectorAll('.tabs');
  var instance = M.Tabs.init(el);
});

document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.sidenav');
  var instances = M.Sidenav.init(elems);
});

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
    result = await deleteData(url);
    url = server + "/ratings/" + instid;
    window.location.href = url;
  }
}

//Add to Favorites
async function addFavs(instid, btn1, btn2){
  url = server + "/favorites/" + instid;
  result = await postDataNoBody(url);
  if (result){
    M.toast({html: 'Added to favorites', classes:'z-depth-3 toastStyle'});
    document.querySelector(btn1).style.display="none";
    document.querySelector(btn2).style.display="";
  }
}

//Remove from Favorites
async function removeFavs(instid, btn1, btn2){
  url = server + "/favorites/" + instid;
  result = await deleteData(url);
  if (result){
    M.toast({html: 'Removed from favorites', classes:'z-depth-3 toastStyle'});
    document.querySelector(btn1).style.display="none";
    document.querySelector(btn2).style.display="";
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
    //console.log(response)
    return response.ok;
  }catch(error){
    console.log(error);
    return false;
  }
}

async function postDataNoBody(url){
  try{
    let response = await fetch(
      url,
      {
        method: 'POST'
      },
    );
    //console.log(response)
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
    //console.log(response);
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
    //console.log(response);
    return response.ok;  
  }catch(error){
    console.log(error);
    return false;
  }
}

function initCharts(rating){
  data = [rating.rating1, rating.rating2, rating.rating3, rating.rating4, rating.rating5, rating.rating6];
  data = data.map(function(x){
    return Math.round(x * 10) / 10;
  });
  //drawChart(data);
  drawColumnChart(data);
  data = [rating.rating7, rating.rating8, rating.rating9, rating.rating10, rating.rating11]
  data = data.map(function(x){
    return Math.round(x * 10) / 10;
  });
  drawSpiderFigure(data);
  //drawFigure(data);
}

function drawColumnChart(data){
  var options = {
    chart: {
      type: 'bar',
      height: '280px'
    },
    series: [{
      name: 'Teaching Style',
      data: data
    }],
    xaxis: {
      categories: ['Presentation', 'Material Accessability', 'Material Coverage', 'Pacing', 'Conciseness', 'Practical Demonstation']
    },
    yaxis: {
      tickAmount: 5,
      min: 0,
      max: 5,
    },
    legend: {
      show: false
    },
    colors: ['#1e5631', '#a4de02', '#76ba1b', '#4c9a2a', '#acdf87', '#68bb59'],
    plotOptions: {
        bar: {
            horizontal: true,
            distributed: true,
            barHeight: '100%'
          }
    }
  }
  
  var chart = new ApexCharts(document.querySelector("#chartBar"), options);
  
  chart.render();
}

function drawSpiderFigure(data){
  var options = {
    chart: {
      type: 'radar',
      height: '280px',
      offsetY: 20,
      offsetX: 12
    },
    series: [
      {
        name: "Personality",
        data: data
      }
    ],
    labels: ['Helpful', 'Friendly', 'Interesting', 'Enthusiasm', 'Expertise'],
    yaxis: {
      tickAmount: 5,
      min: 0,
      max: 5,
    },
    markers: {
      size: 5,
      hover: {
        size: 10
      }
    },
    colors: ['#00e676'],
    dataLabels: {
      enabled: true,
      distributed: true,
      background: {
        enabled: true,
        borderRadius:2,
      }
    },
    plotOptions: {
      radar: {
        polygons: {
          strokeColor: '#e8e8e8',
          fill: {
              colors: ['#f8f8f8', '#fff']
          }
        }
      }
    }
  }

  var chart = new ApexCharts(document.querySelector("#chartSpider"), options);
  
  chart.render();
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
function checkFavorites(favorites, instructors){
  fav = document.querySelector('#favCheckBox');
  if (fav.checked == true){
    for (instructor in instructors){
      instructor = JSON.stringify(instructors[instructor]);
      instructor = JSON.parse(instructor);
      document.querySelector(`#inst${instructor['id']}`).style.display = "none";
    }
    for (favorite in favorites){
      favorite = JSON.stringify(favorites[favorite]);
      favorite = JSON.parse(favorite);
      //console.log(favorite["instructorid"]);
      document.querySelector(`#inst${favorite["instructorid"]}`).style.display = "";
    }
  }else{
    for (instructor in instructors){
      instructor = JSON.stringify(instructors[instructor]);
      instructor = JSON.parse(instructor);
      document.querySelector(`#inst${instructor['id']}`).style.display = "";
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