from flask import Flask, render_template, request,redirect
import shortuuid
app = Flask(__name__) #to make the application run on the server
url_database = {}

@app.route('/') 
def index():
    return render_template('index.html', url_db=url_database)


@app.route('/shorten', methods=['POST']) #It is used to update the existing resource or create a new resource. most common HTTP methods.
def shorten():
    long_url = request.form['long_url']
    short_url = generate_short_url()
    url_database[short_url] = long_url
    return render_template('index.html', short_url=short_url,url_db=url_database)


@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    if short_url in url_database:
        long_url = url_database[short_url]
        return redirect(long_url)
    else:
        return "Short URL not found", 404

@app.route('/')
def show_all():
    return render_template('index.html', url_database=url_database)

def generate_short_url():
    return shortuuid.ShortUUID().random(length=6)


if __name__ == '__main__':
    app.run(debug=True)
