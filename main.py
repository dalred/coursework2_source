import os
from flask import Flask, render_template, send_from_directory, request
from functions import read_json, counts_comments

json_dir = 'data'
BASEDIR = os.path.abspath(os.path.dirname(__file__))
profile_path = os.path.join(BASEDIR, json_dir, 'data.json')
comments_path = os.path.join(BASEDIR, json_dir, 'comments.json')
images_path = os.path.join(BASEDIR, 'static\img')
app = Flask(__name__)


@app.route("/")
def page_index():
    profile = read_json(profile_path)
    return render_template('index.html', profile=profile)


@app.route("/posts/<int:post_id>")
def posts(post_id):
    post = {}
    for item in read_json(profile_path):
        if item['pk'] == post_id:
            post = item
    comments = [item for item in read_json(comments_path) if item['post_id'] == post_id]
    return render_template('post.html', **post, comments=comments, count=len(comments))


@app.route("/uploads/images/<name>")
def images(name):
    return send_from_directory(images_path, name)


@app.route("/search", methods=["GET"])
def search_():
    try:
        search = request.args.get('s')
        items = [item for item in read_json(profile_path) if search in item['content']]
        comments = counts_comments(items[:10], comments_path)
        return render_template('search.html', comments=comments, items=items, count=len(items), search=search)
    except:
        return '', 400



@app.route("/users/<username>")
def username(username):
    items = [item for item in read_json(profile_path) if item['poster_name'] == username]
    comments = counts_comments(items, comments_path)
    return render_template('user-feed.html', comments=comments, items=items)


if __name__ == "__main__":
    app.run('127.0.0.1', 8000)
