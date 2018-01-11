import alt_parse
from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = set(['txt', 'log'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test', methods=['GET', 'POST'])
def test_endpoint():
    return alt_parse.parse_test_file()

@app.route('/upload', methods=['POST'])
def capture_upload():
    if request.method == 'POST':
        if 'logfile' not in request.files:
            return 'Missing logfile'
    file = request.files['logfile']
    if file.filename == '' or not allowed_file(file.filename):
        return 'No selected file or incorrect file type'
    else:
        return alt_parse.parse_uploaded_file(file)


def handle_uploaded_file(upload):
    return alt_parse.parse_uploaded_file(upload)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=False)