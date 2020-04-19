import ntpath
import os
import secrets
from DirectoryHandling import DirectoryHandling as dh
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort,send_file, send_from_directory
from project import app, db, bcrypt
from project.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from project.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

# posts = [
# 	{
# 		"author" : "Muhammad Muneeb",
# 		"title" : "Section 1",
# 		"content" : "Lorem Ipsum de crore",
# 		"date_posted": "August 30, 2019"
# 	},
# 	{
# 		"author" : "Muhammad Uzair",
# 		"title" : "Section 2",
# 		"content" : "Lorem Ipsum de crore",
# 		"date_posted": "August 31, 2019"
# 	}
# ]

folders = [
	{
		'title': 'textFiles',
		'date_created' : 'October 24, 2019',
		'link' : 'home',
		'current_location': 'drive',
		'parent_folder': ''
	},
	{
		'title': 'word',
		'date_created' : 'October 24, 2019',
		'link' : 'home',
		'current_location': 'drive',
		'parent_folder': ''
	},
	{
		'title': 'Images',
		'date_created' : 'October 24, 2019',
		'link' : 'about',
		'current_location': 'word',
		'parent_folder': 'word'
	}
]

files = []
dirs = []
root_dir = ''
dih = dh.dirHandling()


@app.route("/")
@app.route("/home")
def home():
	posts = Post.query.all()
	return render_template('home.html', posts=posts)

@app.route("/about")
def about():
	return render_template('about.html', title='About')

# folder = 'pdf'

@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash("Your account has been created! You are now able to log in", 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		initUser()
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next') #args is a dictionary we use get method so that if the next prameter dost not exits it gives none so dont use square brackets with the key
			initUser()
			flash("Login Successful" , "success")
			return redirect(next_page) if next_page else redirect(url_for('home')) # this is done so that if login page is directed from a restricted page then after login it redirects to that page instead of home page
		else:
			flash("Login Unsuccessful, Please check your email and password" , "danger")
	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))


def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
	
	outputsize = (125,125)
	pic = Image.open(form_picture)
	pic.thumbnail(outputsize)
	pic.save(picture_path)
	return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your Account has been Successfully Updated!', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file=image_file, form = form)



@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title = form.title.data, content = form.content.data, author = current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your Post has been created!', 'success')
		return redirect(url_for('home'))
	return render_template('create_post.html', title='New Post', form = form , legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash('Post Successfully Updated', 'success')
		return redirect(url_for('post', post_id=post.id))
	elif request.method == 'GET':	
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_post.html', title='Update Post', form = form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Your Post has been deleted!', 'success')
	return redirect(url_for('home'))


def initUser():
	root_dir = dih.getRootDir(userName=current_user.username)	
	dirs = dih.getAllFoldersInAFolder(folder='.')	
	files = dih.getAllFilesInAFolder(folder='.')
	return [root_dir,dirs,files]
	flash(dirs)

@app.route("/drive/")
@login_required
def drive():
	folder_icon = url_for('static', filename='driveIcons/folderIcon.png' )
	# file_icon = url_for('static', filename='driveIcons/document.png')
	
	file_icon = getFolderIcon()
	info = initUser()
	dirs = info[1]
	folder = 'drive'
	return render_template('drive.html', title='Drive', image_file = file_icon, 
							image_folder = folder_icon, dirs= dirs, files = files, 
							cur_folder = folder, prev_folder = "")

def searchFolder(folder):
	root_dir = dih.getRootDir(userName=current_user.username)	
	dirs = dih.getAllFoldersInAFolder(folder='./' + folder)	
	files = dih.getAllFilesInAFolder(folder='./' + folder)
	return [root_dir,dirs,files]
	# flash(dirs)

def getFolderIcon():
	# random_hex = secrets.token_hex(8)
	# _, f_ext = os.path.splitext(icon.filename)
	path = url_for('static', filename='driveIcons/document.png')
	picture_path =  os.getcwd() + '/project' + path	
	outputsize = (100,100)
	pic = Image.open(picture_path)
	pic.thumbnail(outputsize)
	pic.save(picture_path)
	return pic




@app.route("/drive/url=<path:name>")
@login_required
def subFolder(name):
	if name == 'drive':
		name = '.'
	else:
		name = name.replace('drive/', '')
	# name = name.replace('drive', '')

	folder_icon = url_for('static', filename='driveIcons/folderIcon.png' )
	file_icon = url_for('static', filename='driveIcons/document.png')
	# folder_icon = getFolderIcon(icon = folder_icon)
	# file_icon = getFolderIcon()	
	info = searchFolder(name)
	files = info[2]
	dirs = info[1]
	folder = name
	return render_template('drive.html', title='Drive', image_file = file_icon, image_folder = folder_icon,
							 dirs= dirs, files = files, cur_folder = folder, prev_folder = 'drive')

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

@app.route("/downloadFile/<path:abspath>", methods=['GET'])
@login_required
def downloadFile(abspath):
	print(abspath)
	# root_dir,dirs,files = searchFolder(abspath)
	info = searchFolder(abspath)
	root_dir = info[0]
	files = info[2]
	dirs = info[1]
	print(f'userName:{root_dir}, dirs: {dirs}, files{files}')
	
	path = root_dir + '\\'+abspath
	filename = path_leaf(abspath)
	# filename = os.path.splitext(abspath)[0]
	ext = os.path.splitext(abspath)[1]
	# path = "Users\\root_admin686\\textFiles\\README.TXT"
	# filename = path_leaf(name)
	path = path.replace('\\','/')
	
	print('path',path)
	print('filename',filename)
	return send_file(path, attachment_filename=filename, as_attachment=True)
	# return send_from_directory(directory=path, filename='README.TXT', as_attachment=True)


# @app.route("/upload_file")
# @login_required
# def upload():
# 	return render_template('uploadFile.html', title='upload file')


def getDest(file):
	root_dir = dih.getRootDir(userName=current_user.username)	
	destPath = dih.getDestinationPath(file=file)	
	return destPath

@app.route("/drive/upload", methods=['POST'])
@login_required
def upload_file():
	for file in request.files.getlist("file"):
		print(file)
		filename = file.filename
		destination = getDest(file=filename) + '/'+ filename
		print(destination)
		# if os.path.isfile(destination):
		# 	flash('File already Exists!', 'success')
		# 	return redirect(url_for('drive'))
		file.save(destination)
	flash('File(s) Uploaded!', 'success')
	return redirect(url_for('drive'))



# @app.route("/drive/"+folder)
# @login_required
# def folder_page():
# 	folder_icon = url_for('static', filename='driveIcons/folderIcon.png' )
# 	return render_template('drive.html', title='Drive', image_file = folder_icon, folders= folders, link=folder)

