from flask import *
import requests

app = Flask(__name__)

API_KEY = "f72af88da7fb07d1b77c6c2dd970599b"
API_READ_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNzJhZjg4ZGE3ZmIwN2QxYjc3YzZjMmRkOTcwNTk5YiIsIm5iZiI6MTczOTA4NjYxOS4xNTgwMDAyLCJzdWIiOiI2N2E4NWIxYjg5ZjA1ZTE2MTlmMTMyMzciLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.NqBddMfGUtkSHyb_nUykNbX9B0iWq-HL0uq9JSqkoFs"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/getMovie", methods=["GET", "POST"])
def getMovie():
    if request.method == "POST":
        name = request.form["search"]
        name1 = name.strip().replace(" ", "%20")
        url = f"https://api.themoviedb.org/3/search/movie?query={name1}&include_adult=false&language=en-US&page=1"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {API_READ_ACCESS_TOKEN}"
        }
        response = requests.get(url, headers=headers)
        response = response.json()
        return render_template("index.html", data=response['results'])
    return redirect(url_for('index'))

@app.route("/getMovieDetails", methods=["GET", "POST"])
def getMovieDetails():
    if request.method == "POST":
        movie_id = request.form["id"]
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {API_READ_ACCESS_TOKEN}"
        }
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
        response = requests.get(url, headers=headers)
        response = response.json()
        cast = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US", headers=headers).json()
        review = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?language=en-US&page=1", headers=headers).json()
        similar = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/similar?language=en-US&page=1", headers=headers).json()
        
        return render_template("index.html", details=response, cast=cast, review=review, similar=similar)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=8100)