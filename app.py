import os
import secrets
from werkzeug.utils import secure_filename
from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from  flask_login import LoginManager,UserMixin
from  flask_login import current_user,login_user,logout_user,login_required
from forms import UpdateBlogForm,BlogPostForm,LoginForm,RegistrationForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret_key'
app.config['UPLOAD_FOLDER'] = "static/pics/"

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#DATABASE TABLE
class User(db.Model,UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50), nullable=False)
  email = db.Column(db.String(40), nullable=False)
  password = db.Column(db.String(40), nullable=False)
  date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
  posts = db.relationship('Post',backref='author', lazy=True)
    
class Post(db.Model):   
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(50), nullable=False)
  date_posted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
  description = db.Column(db.Text, nullable=False)
  image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

@app.route('/admin')
def admin():
  user = User.query.all()
  post = Post.query.all()
  return render_template('admin.html',user=user, posts=post)

@app.route('/')
def home():
  user_details = User.query.all()
  post = Post.query.all()
  return render_template('index.html',post=user_details, posts=post)

@app.route('/register',methods = ["GET","POST"])
def register():
    if current_user.is_authenticated:
      return redirect(url_for('home'))
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
      email = reg_form.email.data
      username = reg_form.username.data
      hashed_password = bcrypt.generate_password_hash(reg_form.password.data).decode('utf-8')
      #check the Exsting User
      user_name = User.query.filter_by(username=username).first()
      user_email = User.query.filter_by(email=email).first()
      if user_name:
        msg = "Username Already Exist. Please Take Another."
        return render_template('register.html',form=reg_form,msg=msg)
      elif user_email:
        msg = "Email ID Already Exist. Please Take Another."
        return render_template('register.html',form=reg_form,msg=msg)
      else:  
        user = User(username=username, email=email, password=hashed_password)
        
    # add the new user to the database
      db.session.add(user)
      db.session.commit()
      login_user(user)
        
      return redirect('/login')
  
    return render_template('register.html',form=reg_form)
  
@app.route('/login',methods = ["GET","POST"])
def login():
    if current_user.is_authenticated:
       return redirect(url_for('home'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
      email = login_form.email.data
      password = login_form.password.data  
      
      user = User.query.filter_by(email=email).first()
      
      if user and bcrypt.check_password_hash(user.password,password):
        msg = "Login Successfully"
        login_user(user)
        return redirect('/account')
      else:
        msg = "Invalid Login Credentials!"
        return render_template('login.html', msg=msg,form=login_form)
      #msg="Your Registration has been Successful. You can Login Now."
  
    return render_template('login.html',form=login_form) 
  
@app.route('/logout')
def logout():
  logout_user()
  return redirect('/') 

   
#def save_picture(form_picture):
    #random_hex = secrets.token_hex(8)
    #_, f_ext = os.path.splitext(form_picture.filename)
    #picture_fn = random_hex + f_ext
    #picture_path = os.path.join(app.root_path, 'static/pics', picture_fn)
    #form_picture.save(picture_path)
    
    #return picture_fn
   
@app.route('/post-a-blog',methods = ["GET","POST"])
@login_required
def blogpost():
  form = BlogPostForm()
  if form.validate_on_submit():
    title = form.title.data
    description = form.description.data
    picture = form.file.data
    filename = secure_filename(picture.filename)
    picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    posts = Post(title = title,description=description, author = current_user,image_file=filename)
    
    db.session.add(posts)
    db.session.commit()
    msg = "Your Post has been Successfully Created."
  else:
    return render_template('blogpost.html',form=form)
    
  return render_template('blogpost.html',form=form,msg=msg) 

@app.route("/account")
@login_required
def account():
  posts = current_user.posts
  return render_template('account.html', posts=posts)

@app.route("/update/<int:id>", methods=['GET', 'POST'])
@login_required
def update_blog(id):
    form = UpdateBlogForm()
    if form.validate_on_submit():
      blogs = Post.query.filter_by(id=id).first()
      blogs.title = form.title.data
      blogs.description = form.description.data
      picture = form.file.data
      filename = secure_filename(picture.filename)
      picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
      db.session.commit()
      #msg = "Your Post has been Successfully Created."
      return redirect('/account')
      
    
    blogs = Post.query.filter_by(id=id).first()  
    form.title.data = blogs.title
    form.description.data = blogs.description
    return render_template('update.html', form=form, blogs=blogs)

@app.route('/delete/<int:id>', methods=['GET','POST'])
def delete(id):
  post = Post.query.filter_by(id=id).first_or_404()

  db.session.delete(post)
  db.session.commit()
  return redirect('/account')

@app.route('/blogs/<int:id>', methods=['GET','POST'])
def blogshow(id):
  blog = Post.query.filter_by(id=id).first_or_404()

  return render_template('blogshow.html', blog=blog)
        


if __name__ == '__main__':
    app.run(port=5000,debug=True)