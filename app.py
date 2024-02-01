from flask import Flask, render_template, request
app = Flask(__name__) #to make the application run on the server

@app.route('/') 
def index():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True)
