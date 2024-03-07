from flask import Flask, render_template, request, redirect
from models import db, User
import qrcode
from io import BytesIO
import base64
import shortuuid
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
    forminput = request.form['suggested_name'].strip()
    if not forminput:
        suggested_name = generate_short_url()
    else:
        suggested_name = forminput
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

    # Generate the QR code for the short URL
    qr = qrcode.QRCode(
        version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=4, border=1)
    qr.add_data(short_url)
    qr.make(fit=True)

    # Create an in-memory bytes buffer to save the QR code image
    qr_code_img = BytesIO()
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(qr_code_img)
    qr_code_img.seek(0)
    qr_code_base64 = base64.b64encode(qr_code_img.getvalue()).decode('utf-8')

    # Pass the short URL and QR code to the template for rendering
    return render_template('index.html', short_url=short_url, qr_code=qr_code_base64)


@app.route('/show')
def show_data():
    links = User.query.all()
    hosturl = request.url_root.rstrip('/')
    return render_template('show.html', links=links,hosturl=hosturl)


@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    user = User.query.filter_by(short=short_url).first()
    if user:
        return redirect(user.long)
    else:
        return render_template('error.html')


def generate_short_url():
    return shortuuid.ShortUUID().random(length=6)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
