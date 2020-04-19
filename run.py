
from project import app

if __name__ == '__main__':
	# website_url = '127.0.0.7:4996'
	website_url = '127.0.0.1:4996'
	app.config['SERVER_NAME'] = website_url
	app.run(debug=True)