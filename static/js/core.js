removeById = function (id) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', "/dashboard/remove", true);
    xhr.onload = function () {
        console.log(this.responseText);
        window.location.hash = 'deleteArticle';
        window.location.reload();
    };
    xhr.send(id.toString());
}

comment = function (id, content) {
    document.getElementById("comment" + id).value = "";
    var items = {
        "id": id
        , "content": content
    };
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/comment", true);
    xhr.onload = function () {
        console.log(this.responseText);
    }
    xhr.send(JSON.stringify(items));
}

login = function (user, pass) {
    console.log("iet");
    var items = {
        "username": user
        , "password": pass
    }
    var xhr = new XMLHttpRequest();
    xhr.open('POST', "/login", true);
    xhr.onload = function () {
        console.log(this.responseText);
        window.location = "/dashboard";
    };
    xhr.send(JSON.stringify(items));
}

count_comments = function () {
    console.log("{{entries.comments}}"); // TODO: make counter. Pass variable using Jinja
}

fileUpload = function (file) {
    var formData = new FormData();
    formData.append('photo', file);
    console.log(file);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', "/dashboard/profileimage", true);
    xhr.onload = function () {
        console.log(this.responseText);
    };
    xhr.send(formData);
}
update = function (title, content, id) {
    
    console.log(title);
    console.log(content);
    var items = {
        "updateTitle": title
        , "updateContent": content
    };
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/dashboard/update/"+id, true);
    xhr.onload = function () {
        console.log(this.responseText);
    }
    xhr.send(JSON.stringify(items));
    
}