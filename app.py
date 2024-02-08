from flask import Flask, render_template, request,redirect
from models import db, User
#import shortuuid
app = Flask(__name__) #to make the application run on the server
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///link.db'
db.init_app(app)
#url_database = {}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        suggested_name = request.form['suggested_name']
        long_url = request.form['long_url']
        if suggested_name and long_url:
            # Check if the name already exists
            existing_user = User.query.filter_by(short=suggested_name).first()
            if existing_user:
                return 'Error: Name already exists. Please enter a different name.'
            else:
                new_user = User(short=suggested_name, long=long_url)
                db.session.add(new_user)
                db.session.commit()
                return 'Thank you for submitting your information!'
        else:
            return 'Please enter both your name and place.'
    return render_template('index.html')



@app.route('/show')
def show_data():
    links = User.query.all()
    return render_template('show.html', links=links)

# @app.route('/shorten', methods=['POST']) #It is used to update the existing resource or create a new resource. most common HTTP methods.
# def shorten():
#     long_url = request.form['long_url']
#     short_url = generate_short_url()
#     url_database[short_url] = long_url
#     return render_template('index.html', short_url=short_url)


# @app.route('/<short_url>')
# def redirect_to_long_url(short_url):
#     if short_url in url_database:
#         long_url = url_database[short_url]
#         return redirect(long_url)
#     else:
#         return "Short URL not found", 404

# @app.route('/')
# def show_all():
#     return render_template('index.html', url_database=url_database)

# def generate_short_url():
#     return shortuuid.ShortUUID().random(length=6)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
