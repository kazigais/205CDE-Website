from flask import Flask, render_template, redirect, url_for
import os
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
import sqlite3

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
        with sqlite3.connect(app.config['DATABASE']) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO articles_table (title, content) VALUES (?,?)", (title, content))
            con.commit()

        return redirect(url_for('home'))
    return render_template('dashboard.html', form=form)


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



if __name__ == '__main__':
    Bootstrap(app)
    app.run(port=8080, host='0.0.0.0', debug=True)