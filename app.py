from flask import Flask,render_template,url_for,redirect,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ("DATABASE_URL")
db = SQLAlchemy(app)

class posts(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	post_title = db.Column(db.String(200),nullable=False)
	post_content = db.Column(db.String,nullable=False)
	post_date = db.Column(db.DateTime,default=datetime.utcnow)

	def __repr__(self):
		return "<post %r>" % self.id

@app.route("/")
def index():
	all_posts = posts.query.order_by(posts.post_date).all()
	for x in all_posts:
		x.post_date = str(x.post_date).split(".")[0]
	return render_template("index.html",posts_data=all_posts)

@app.route("/add",methods=['POST','GET'])
def add():
	if request.method=='POST':
		post_title = request.form['post_title']
		post_content = request.form['post_content']
		new_post = posts(post_title=post_title,post_content=post_content)
		try:
			db.session.add(new_post)
			db.session.commit()
			return redirect("/")
		except:
			return "something went wrong"

	return render_template("add.html")

if __name__ == "__main__":
	app.run(debug=True)
