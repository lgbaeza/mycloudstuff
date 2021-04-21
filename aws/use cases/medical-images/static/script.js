const API_KEY = ''
const API_GW_ENDPOINT=''
const API_GW_URL= API_GW_ENDPOINT + '/?key=' + API_KEY;

async function loaddata(){
    const Http = new XMLHttpRequest();
    Http.open("GET", API_GW_URL);
    Http.send();
    
    Http.onreadystatechange = (e) => {
        var items = JSON.parse(Http.responseText)
        var tbodyRef = document.getElementById('myTable').getElementsByTagName('tbody')[0];
        if(items.length > 0){
            tbodyRef.innerHTML = ''
            items.forEach(element => {
                var newRow = tbodyRef.insertRow();
                //image
                var newCell = newRow.insertCell();
                var img = document.createElement("img");
                img.src = element.s3path
                newCell.appendChild(img);
                //text
                var newCell = newRow.insertCell();
                var p = document.createElement("span");
                p.innerHTML = element.fullText
                newCell.appendChild(p);
                //medical
                var newCell = newRow.insertCell();
                element.medical.forEach(entity => {
                    var div = document.createElement("div")
                    div.innerHTML = `<div class="container medical">
                                        <div class="title">${entity.Category}</div>
                                        <div class="value">${entity.Text}</div>
                                    </div>`
                    newCell.appendChild(div);
                })
                //comprehend
                var newCell = newRow.insertCell();
                element.comprehend.forEach(entity => {
                    var div = document.createElement("div")
                    div.innerHTML = `<div class="container comprehend">
                                        <div class="title">${entity.Type}</div>
                                        <div class="value">${entity.Text}</div>
                                    </div>`
                    newCell.appendChild(div);
                })
                
            })
        }
        else{
            var newRow = tbodyRef.insertRow();
            var newCell = newRow.insertCell();
            newCell.colSpan = 4
            newCell.innerText = "No hay registros"
        }
    }
}