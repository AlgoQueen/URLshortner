from flask import Flask, render_template, request,redirect
from models import db, User
#import shortuuid
app = Flask(__name__) #to make the application run on the server
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///link.db'
db.init_app(app)
#url_database = {}


@app.route('/', methods=['GET', 'POST'])
def index():
#     if request.method == 'POST':
#         suggested_name = request.form['suggested_name']
#         long_url = request.form['long_url']
#         if suggested_name and long_url:
#             # Check if the name already exists
#             existing_user = User.query.filter_by(short=suggested_name).first()
#             if existing_user:
#                 return 'Error: Name already exists. Please enter a different name.'
#             else:
#                 new_user = User(short=suggested_name, long=long_url)
#                 db.session.add(new_user)
#                 db.session.commit()
#                 short_url = request.host_url + suggested_name
#                 #return 'Thank you for submitting your information!'
#         else:
#             return 'Please enter both your name and place.'
    return render_template('index.html')


@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['long_url']
    suggested_name = request.form['suggested_name']

    # Check if the suggested short URL already exists
    existing_mapping = User.query.filter_by(short=suggested_name).first()
    if existing_mapping:
        return f'The suggested short URL "{suggested_name}" already exists. Please choose a different suggestion.'

    # Store the mapping in the database
    url_mapping = User(short=suggested_name, long=long_url)
    db.session.add(url_mapping)
    db.session.commit()

    short_url = request.host_url + suggested_name
    return f'Short URL: <a href="{short_url}">{short_url}</a>'

@app.route('/show')
def show_data():
    links = User.query.all()
    return render_template('show.html', links=links)


@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    user = User.query.filter_by(short=short_url).first()
    if user:
        return redirect(user.long)
    else:
        return "Short URL not found", 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
