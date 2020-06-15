console.log('===Lite Start===')
let ar_json = []
var btn = document.getElementById('btn_check');
    fetch('/get_data_light', {method: 'POST'}).then(res => res.json()).then(function (data) {
        console.log(data.url[1])
        var resp = document.getElementById('resp');
        var tb = new XMLHttpRequest();
        var ref = '/webcheck-light';
        tb.open('GET', ref, false);
        tb.send();
        var row = document.createElement('tr');
        var td_url = document.createElement('td');
        var td_http = document.createElement('td');
        var td_time = document.createElement('td');
        td_url.appendChild(document.createTextNode(data.url[0] + " "))
        td_http.appendChild(document.createTextNode(data.url[1] + " "))
        td_time.appendChild(document.createTextNode(data.url[2] + " "))
        row.appendChild(td_url);
        row.appendChild(td_http);
        row.appendChild(td_time);
        resp.appendChild(row)
    });