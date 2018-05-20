from flask import Flask, url_for, render_template

app = Flask(__name__, static_url_path='')


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/poi/get")
def get_poi_by_coords(request):
    print(request.data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)