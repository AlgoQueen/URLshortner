from flask import Flask, render_template, request, redirect
from models import db, User
# import shortuuid
# to make the application run on the server
app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///link.db'
db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['long_url']
    suggested_name = request.form['suggested_name']

    # Check if the suggested short URL already exists
    existing_mapping = User.query.filter_by(short=suggested_name).first()
    if existing_mapping:
        Error=f'The suggested short URL "{suggested_name}" already exists. Please choose a different suggestion.'
        return render_template('index.html', error=Error)

    # Store the mapping in the database
    url_mapping = User(short=suggested_name, long=long_url)
    db.session.add(url_mapping)
    db.session.commit()

    short_url = request.host_url + suggested_name
    return render_template('index.html', short_url=short_url)


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
        return render_template('error.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
