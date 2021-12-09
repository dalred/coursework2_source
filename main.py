import os, re
from flask import Flask, render_template, send_from_directory, request,redirect
from functions import read_json, counts_comments, search_tag, view_tag, regex_tags, add_bookmarks, delete_bookmarks

json_dir = 'data'
BASEDIR = os.path.abspath(os.path.dirname(__file__))
profile_path = os.path.join(BASEDIR, json_dir, 'data.json')
comments_path = os.path.join(BASEDIR, json_dir, 'comments.json')
images_path = os.path.join(BASEDIR, 'static\img')
bookmarks_path = os.path.join(BASEDIR, json_dir, 'bookmarks.json')
app = Flask(__name__)


@app.route("/")
def page_index():
    bookmarks__ = read_json(bookmarks_path)
    profile = regex_tags(profile_path)
    return render_template('index.html', profile=profile, count=len(bookmarks__), bookmarks=bookmarks__)


@app.route("/posts/<int:post_id>")
def posts(post_id):
    post = {}
    profile = regex_tags(profile_path)
    for item in profile:
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

@app.route("/tag/<tagname>", methods=["GET"])
def page_tag(tagname):
    if not tagname:
        return "Record not found", 400
    items = search_tag(tagname, profile_path)
    comments = counts_comments(items, comments_path)
    return render_template('tag.html', items=items, comments=comments, tagname=tagname)

@app.route("/bookmarks/add/<int:post_id>")
def bookmarks_add(post_id):
    add_bookmarks(post_id, bookmarks_path)
    return redirect("/", code=302)

@app.route("/bookmarks/")
def bookmarks_():
    data = read_json(bookmarks_path)
    items = [item for item in read_json(profile_path) if item['pk'] in data]
    comments = counts_comments(items, comments_path)
    return render_template('bookmarks.html', items=items, comments=comments)


@app.route("/bookmarks/remove/<int:post_id>")
def delete_bookmarks_(post_id):
    delete_bookmarks(post_id, bookmarks_path)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run('127.0.0.1', 8000)
