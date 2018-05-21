from flask import Flask, url_for, render_template, request

app = Flask(__name__, static_url_path='')


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/poi/get", methods=['GET', 'POST'])
def get_poi_by_coords():
    if request.method == 'POST':
        print(request.get_json(force=True))
    return 'ttt'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)