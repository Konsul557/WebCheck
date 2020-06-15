let ar_json = []
console.log('===Table Start===')
fetch('/get_data', {method: 'POST'}).then(res => res.json()).then(function (data) {
for (let i = 0; i <= data.url.length; i++){
    ar_json.push(data.url[i])
    var tb = new XMLHttpRequest();
    var ref = '/webcheck';
    tb.open('GET', ref, false);
    tb.send();
    var body = document.getElementById('tb-result');
    for (var j = 0; j <= ar_json.length; j++) {
      var row = document.createElement('tr');
      row.id = j;
      var td_url = document.createElement('td');
      var td_inter = document.createElement('td');
      var td_http = document.createElement('td');
      var td_time = document.createElement('td');
      var button_del = document.createElement('button')
      var cnt = document.createElement('td');
      button_del.setAttribute('class', 'btn')
      button_del.setAttribute('style', 'text-align: center;height: 35px;')
      button_del.id = 'button_del'
      button_del.innerHTML = 'Удалить'
      cnt.appendChild(document.createTextNode(j+" "))
      td_url.appendChild(document.createTextNode(ar_json[i][0] + " "))
      td_inter.appendChild(document.createTextNode(ar_json[i][1] + " "))
      td_http.appendChild(document.createTextNode(ar_json[i][2] + " "))
      td_time.appendChild(document.createTextNode(ar_json[i][3] + " "))
    }
    row.appendChild(cnt);
    row.appendChild(td_url);
    row.appendChild(td_inter);
    row.appendChild(td_http);
    row.appendChild(td_time);
    row.appendChild(button_del)
    body.appendChild(row)
    button_del.onclick = function(){
        var tr_del = document.getElementById(i+1)
        var txt = tr_del.textContent
        txt = txt.split(" ")
        //console.log(txt)
        //console.log(txt[1])
        fetch('/remove_url?url_del='+txt[1]);
    }
}
});