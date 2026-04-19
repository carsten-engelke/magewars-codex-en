"use strict";
const urlParams = new URLSearchParams(window.location.search);
const search = urlParams.get('q');
var fuse;
var db;
if (search !== null && search !== "") {
    document.getElementById("searchbar").value = search;
}
loadFile("autolinked-db_en.json");
var searchBar = document.getElementById("searchbar");
var timeout = null;
searchBar.addEventListener('keyup', function (e) {
    clearTimeout(timeout);
    timeout = setTimeout(function () {
        updateSearch(searchBar.value);
        }, 1000);
    });
updateList();

function updateList() {
    updateSearch(document.getElementById("searchbar").value);
}

function updateSearch(searchTerm) {
    if (searchTerm == "") {
        updateCards(db);
    } else {
        //document.getElementById("result").innerHTML = "<div>" + fuse.search(searchTerm) + "</div>";
        updateCards(fuse.search(searchTerm));
    }
}

function updateCards(list) {
    document.getElementById("result").innerHTML = "";
    for (const obj of list) {
    
        var card = document.createElement("div")
        card.className = "card";
        if (obj.image !== null) {
            var image = document.createElement("img");
            image.src = obj.image;
            image.alt = obj.title;
            image.style = "float:left;margin:10px"
            card.appendChild(image);
        }
            var container = document.createElement("div")
            container.className = "container";
            container.innerHTML = "<h4><b>" + obj.title + " <p style=\"color:Gray;\">(" + obj.title_EN + ")</p></b></h4>"+
            "<h5>" + obj.type + "</h5><p>" + obj.text + "</p>";
            card.appendChild(container);
       
        document.getElementById("result").appendChild(card);
    }
}

function loadFile(filePath) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", filePath, false);
    xmlhttp.onload = function(e) {
        if (xmlhttp.status==200) {
            db = JSON.parse(xmlhttp.responseText);
            var options = {
                shouldSort: true,
                threshold: 0.6,
                location: 0,
                distance: 100,
                maxPatternLength: 32,
                minMatchCharLength: 1,
                keys: [
                  "title",
                  "title_EN",
                  "text"
                ]
            };
            fuse = new Fuse(db, options);
            updateList();
        }
    }
    xmlhttp.send();
  }