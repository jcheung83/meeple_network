async function getData(x) {
    var response = await fetch("https://api.boardgameatlas.com/api/search?name="+x+"&limit=25&client_id=JLBr5npPhV");
    var data = await response.json();
    var save = [];
    for (x in data.games){
        // console.log(data.games[x].name, data.games[x].year_published);
        save.push( { name: data.games[x].name, year: data.games[x].year_published, id: data.games[x].id } );
    }
    output = "<form action='/add_game' method='POST'>";
    for (y in save){
        output += "<div class = 'container'>"
        output += "<input type='radio' id='name' name='name' value='"+save[y].name+"'>";
        output += "<input type='hidden' id='year' name='year' value='"+save[y].year+"'>";
        output += "<input type='hidden' id='bgg_id' name='bgg_id' value='"+save[y].id+"'>";
        output += "<label for 'name'> Name: "+save[y].name+", Year published: "+save[y].year+"</label>";
        output += "</div>";
    }
    output += "<button type='submit' class='btn btn-primary btn-block mb-3'>Add</button>";
    output += "</form>";
    document.getElementById('search_results').innerHTML = output;
}

function search(element){
    var x = document.getElementById("game_name").value;
    getData(x);
}

async function getaData(x) {
    var response = await fetch("https://api.boardgameatlas.com/api/search?name="+x+"&limit=25&client_id=JLBr5npPhV");
    var data = await response.json();
    var save = [];
    for (x in data.games){
        // console.log(data.games[x].name, data.games[x].year_published);
        save.push( { name: data.games[x].name, year: data.games[x].year_published, id: data.games[x].id } );
    }
    output = "<form action='/add_anticipated_game' method='POST'>";
    for (y in save){
        output += "<div class = 'container'>"
        output += "<input type='radio' id='name' name='name' value='"+save[y].name+"'>";
        output += "<input type='hidden' id='year' name='year' value='"+save[y].year+"'>";
        output += "<input type='hidden' id='bgg_id' name='bgg_id' value='"+save[y].id+"'>";
        output += "<label for 'name'> Name: "+save[y].name+", Year published: "+save[y].year+"</label>";
        output += "</div>";
    }
    output += "<button type='submit' class='btn btn-primary btn-block mb-3'>Add</button>";
    output += "</form>";
    document.getElementById('search_results').innerHTML = output;
}

function a_search(element){
    var x = document.getElementById("game_name").value;
    getaData(x);
}