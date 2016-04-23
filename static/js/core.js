removeById = function(id){
    var xhr = new XMLHttpRequest();
    console.log(id);
    xhr.open('POST', "http://localhost:8080/dashboard/remove", true);
    xhr.onload = function () {
        console.log(this.responseText);
        window.location.hash = 'deleteArticle';
        window.location.reload();
    };
    xhr.send(id.toString());
}