removeById = function(id){
    var xhr = new XMLHttpRequest();
    xhr.open('POST', "http://localhost:8080/dashboard/remove", true);
    xhr.onload = function () {
        console.log(this.responseText);
        window.location.hash = 'deleteArticle';
        window.location.reload();
    };
    xhr.send(id.toString());
}

comment = function(id, content){
    document.getElementById("comment"+ id).value = "";
    var items = {
        "id": id,
        "content": content
    };
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:8080/comment", true);
    xhr.onload = function(){
        console.log(this.responseText);
    }
    xhr.send(JSON.stringify(items));
}