from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db= SQLAlchemy(app)

#database to keep a record of all job seekers
class employee(db.Model):

 	name=db.Column(db.String(100),nullable=False)
 	email=db.Column(db.String(50),unique=True,nullable=False,primary_key=True)
 	password=db.Column(db.String(50),nullable=False)
 	def __init__(self, name, email, password):
 		self.name=name
 		self.email=email
 		self.password=password

#database to keep a record of all employers		
class company(db.Model):

 	name=db.Column(db.String(100),nullable=False)
 	email=db.Column(db.String(50),unique=True,nullable=False,primary_key=True)
 	password=db.Column(db.String(50),nullable=False)
 	def __init__(self, name, email, password):
 		self.name=name
 		self.email=email
 		self.password=password

#database to keep a record of all available jobs
class jobdata(db.Model):

	job=db.Column(db.String(20),nullable=False,primary_key=True)
	name=db.Column(db.String(100),nullable=False)
	position=db.Column(db.String(50))
	vacancy=db.Column(db.String(20))
	def __init__(self,job,name,position,vacancy):
		self.job=job
		self.name=name
		self.position=position
		self.vacancy=vacancy

#database to keep a record of all job applications
class applications(db.Model):

	name=db.Column(db.String(100),nullable=False)
	email=db.Column(db.String(50),unique=True,nullable=False,primary_key=True)
	year=db.Column(db.String(20))
	past=db.Column(db.String(50))
	post=db.Column(db.String(50))
	company=db.Column(db.String(100))

	def __init__(self,name,email,year,past,post,company):
		self.name=name
		self.email=email
		self.year=year
		self.past=past
		self.post=post
		self.company=company
 	
headings= ("Jobid","Company Name","Position","No. of Vacancies","Apply")
head=("Name","Email","Psition Applied for","Years of experience","Past Employer")
head1=("Name","Post","Company")

#home page
@app.route("/")
def home():
	return render_template("landing_page.html")

#job seeker login page
@app.route("/login", methods=['POST', 'GET'])
def log():
	if request.method=='POST':
		email=request.form['mail']
		password=request.form['pass']
		user=employee.query.filter_by(email=email).first()
		if user is None:
			return render_template("login.html")
		else:
			data=jobdata.query.paginate()
			data2=applications.query.filter_by(email=email).all()
			return render_template('display_jobs.html',headings=headings,data=data,head1=head1,data2=data2)
	else:
		return render_template("login.html")

#job seeker signup page
@app.route("/signup", methods=['POST', 'GET'])
def register():
	if request.method=='POST':

		name=request.form['content']
		email=request.form['mail']
		password=request.form['pass']
		new_emp=employee(name,email,password)
		try:
			db.session.add(new_emp)
			db.session.commit()
			return redirect("/login")
		except:
			return 'There was some error adding your data'
	else:
		return render_template("signup.html")

#employer login page
@app.route("/login_company",methods=['POST', 'GET'])
def log_company():
	if request.method=='POST':
		email=request.form['mail']
		name=request.form['name']
		
		password=request.form['pass']
		
		user=company.query.filter_by(email=email).first()
		if user is None:
			return render_template("login_company.html")
		else:
			data2=applications.query.filter_by(company=name).all()

			return render_template('job_applications.html',head=head,data2=data2)
	else:
		return render_template("login_company.html")

#aemployers can add job vacancies here
@app.route("/addjob",methods=['POST','GET'])
def addjob():
	
	if request.method=='POST':
		job=request.form['job']
		name=request.form['content']
		position=request.form['mail']
		vacancy=request.form['pass']
		new_emp=jobdata(job,name,position,vacancy)
		try:
			db.session.add(new_emp)
			db.session.commit()
			data2=applications.query.filter_by(company=name).all()
			return render_template("job_applications.html",head=head,data2=data2)
		except:
			return redirect("/login_company")
		
	else:

		return render_template("addjob.html")

#signup page for employer	
@app.route("/signup_company", methods=['POST', 'GET'])
def register_company():

	if request.method=='POST':

		name=request.form['content']
		email=request.form['mail']
		password=request.form['pass']
		new_comp=company(name,email,password)
		try:
			db.session.add(new_comp)
			db.session.commit()
			return redirect("/login_company")
		except:
			return 'There was some error adding your data'
	else:

		return render_template("signup_company.html")

#job seekers can apply to jobs filling the application form
@app.route("/application_form",methods=['POST', 'GET'])
def application_form():

	if request.method=='POST':

		name=request.form['content']
		email=request.form['mail']
		year=request.form['year']
		past=request.form['past']
		post=request.form['post']
		company=request.form['company']
		new_comp=applications(name,email,year,past,post,company)
		try:
			db.session.add(new_comp)
			db.session.commit()
			data=jobdata.query.paginate()
			data2=applications.query.filter_by(name=name).all()
			return render_template("display_jobs.html",headings=headings,data=data,head1=head1,data2=data2)
		except:
			return 'There was some error applying for the job'
	else:

		return render_template("application_form.html")

if __name__=="__main__":
	app.run(debug=True)