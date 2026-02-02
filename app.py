import pickle as pk
from flask import Flask,redirect,render_template,request,jsonify


app=Flask(__name__)



movies=pk.load(open(r"ml_projects\movie_recommendation_system\movies.pkl","rb"))
similarity=pk.load(open(r"ml_projects\movie_recommendation_system\similarity.pkl","rb"))
def recommend(movie):
  movie_index = movies[movies['title'] == movie].index[0]

  movie_list=sorted(list(enumerate(similarity[movie_index])),reverse=True,key=lambda x : x[1])[1:6]
  reco=[]
  for i in movie_list :
    reco.append(movies.iloc[i[0]]['title']) 
  return reco


# print(recommend("Avatar"))
# print(movies['title'])


@app.route('/')
def main():
   return render_template("main.html")
@app.route('/home')
def home():
    titles = movies['title'].tolist()
    return render_template("home.html", titles=titles)


@app.route("/movie", methods=['POST'])
def movie():
    movie = request.form["movie"]
    reco_movies = recommend(movie)
    titles = movies['title'].tolist()
    return render_template("home.html", reco_movies=reco_movies, titles=titles)


@app.route("/api",methods=['GET'])
def api():
  movie=request.args['movie'].title()
  return jsonify(movie=movie,count=5,recommend=recommend(movie))

app.run(debug=True)
