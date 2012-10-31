from flask import Flask

app = Flask(__name__)

app.config.from_pyfile('settings.py')
app.config.from_pyfile('local_settings.py', silent=True)

@app.route('/')
def hello_world():
	return 'Hello World!'

if __name__ == '__main__':
	app.run()
