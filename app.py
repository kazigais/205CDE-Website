from flask import Flask, render_template, redirect, url_for, request, session
import os
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
import sqlite3, datetime, json, ast


UPLOAD_FOLDER = 'static/upload_folder'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS


app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'articles.db'),
    SECRET_KEY='development key'
))


class ArticleForm(Form):
    title = StringField('Title:', validators=[DataRequired()])
    content = TextAreaField('Content:', validators=[DataRequired(), Length(min=1, max=1024)])
    submit = SubmitField('Submit')
    
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('admin'))
    print ("session",session)
    form = ArticleForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d %H:%M")
        with sqlite3.connect(app.config['DATABASE']) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO articles_table (title, content, articleDate) VALUES (?,?,?)", (title, content, date))
            con.commit()
        return redirect(url_for('home'))
    with sqlite3.connect(app.config['DATABASE']) as con:
        items = {}
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM articles_table ORDER BY id DESC")
        entries = cur.fetchall()
        items.update({'entries':entries})
        items.update({'form':form})
        print(items)
        return render_template('dashboard.html', items=items)
    
@app.route('/dashboard/logout', methods=['GET'])
def logout():
    if 'username' not in session:
        return redirect(url_for('admin'))
    else:
        session.pop("username", None)
        return redirect(url_for('home'))


@app.route('/')
def home():
    with sqlite3.connect(app.config['DATABASE']) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM articles_table ORDER BY id DESC")
        articles = cur.fetchall()
        cur.execute("SELECT * FROM comments_table")
        comments = cur.fetchall()
        entries = {'articles': articles, 'comments':comments}
        return render_template('home.html', entries=entries)

@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')

def credential_check(data):
    with sqlite3.connect(app.config['DATABASE']) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT user_name, user_password FROM user_table WHERE user_name = '%s' AND user_password = '%s'" % (data['username'], data['password']))
        user = cur.fetchall()
        if len(user) != 0:
            return True
        else:
            return False
    
@app.route('/login', methods=['POST'])
def login():
    data = json.loads(request.data)
    print (data)
    if credential_check(data) == True:
        session['username'] = data['username']
        return "200"
    else:
        return "Credentials invalid. Please try again."
    

@app.route('/dashboard/remove', methods=['POST'])
def remove():
    with sqlite3.connect(app.config['DATABASE']) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        print request.data
        cur.execute("DELETE FROM articles_table WHERE id = " + request.data)
        cur.execute("DELETE FROM comments_table WHERE article_id = " + request.data)
        con.commit()
        return "200"
    
@app.route('/comment', methods=['POST'])
def comment():
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M")
    data = json.loads(request.data)
    print (data['content'])
    with sqlite3.connect(app.config['DATABASE']) as con:
        cur = con.cursor()
        cur.execute("INSERT INTO comments_table (article_id, commentContent, commentDate) VALUES (?,?,?)", (data["id"], data["content"], date))
        con.commit()
        return "200"
    
@app.route('/view/<id>', methods=['GET'])
def view(id):
    with sqlite3.connect(app.config['DATABASE']) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM articles_table WHERE id = " + id)
        articles = cur.fetchall()
        cur.execute("SELECT * FROM comments_table WHERE article_id = " + id)
        comments = cur.fetchall()
        entries = {'articles': articles, 'comments':comments}
        return render_template('viewOne.html', entries=entries)
    
@app.route('/dashboard/profileimage', methods=['POST', 'GET'])
def profileimage():
    if request.method == "POST":
        file = request.files['file']
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = "profileImage.jpg"
            # Move the file form the temporal folder to
            # the upload folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
            return redirect(url_for('dashboard'))
        return "File type not supported. Please upload JPG, JPEG or PNG only."
    else:
        return "200"

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
    
@app.route('/dashboard/update/<id>', methods=['GET','POST'])
def update(id):
    if request.method == "GET":
        with sqlite3.connect(app.config['DATABASE']) as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM articles_table WHERE id = " + id)
            articles = cur.fetchall()
            cur.execute("SELECT * FROM comments_table WHERE article_id = " + id)
            comments = cur.fetchall()
            entries = {'articles': articles, 'comments':comments}
            return render_template('updateOne.html', entries=entries)
    elif request.method == "POST":
        data = json.loads(request.data)
        with sqlite3.connect(app.config['DATABASE']) as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            print (id)
            cur.execute("UPDATE articles_table SET title='%s',content='%s' WHERE id = %s" % (data['updateTitle'], data['updateContent'], id))
            con.commit()
            return "200"
    return "400"
    

        





if __name__ == '__main__':
    Bootstrap(app)
    app.run(port=8000, host='0.0.0.0', debug=True)