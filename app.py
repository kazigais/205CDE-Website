from flask import Flask, render_template, redirect, url_for, request
import os
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
import sqlite3, datetime

app = Flask(__name__)

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
        items = {};
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM articles_table")
        entries = cur.fetchall()
        items.update({'entries':entries});
        items.update({'form':form});
        print(items);
        return render_template('dashboard.html', items=items)


@app.route('/')
def home():
    with sqlite3.connect(app.config['DATABASE']) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM articles_table")
        entries = cur.fetchall()
        return render_template('home.html', entries=entries)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/dashboard/remove', methods=['POST'])
def remove():
    with sqlite3.connect(app.config['DATABASE']) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        print request.data
        cur.execute("DELETE FROM articles_table WHERE id = " + request.data)
        con.commit()
        return "200"





if __name__ == '__main__':
    Bootstrap(app)
    app.run(port=8080, host='0.0.0.0', debug=True)