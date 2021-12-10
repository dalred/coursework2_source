from flask import Flask, render_template, send_from_directory, request, redirect
from functions import *
from google_file_id import dict_file_id

json_dir = 'data'
BASEDIR = os.path.abspath(os.path.dirname(__file__))
profile_path = os.path.join(BASEDIR, json_dir, 'data.json')
images_path = os.path.join(BASEDIR, 'static\img')

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def page_index():
    bookmarks__ = read_google_json(dict_file_id['bookmarks_fileId'])
    profile = read_json(profile_path)
    profile_html = regex_tags(profile)
    return render_template('index.html', profile=profile_html, count=len(bookmarks__), bookmarks=bookmarks__)


@app.route("/posts/<int:post_id>", methods=["GET", "POST"])
def posts(post_id):
    if request.method == "POST":
        comment = request.form.get('comment-form__textarea')
        name = request.form.get('comment-form__input')
        add_comment(post_id, comment, name, dict_file_id['comments_fileid'])
    post = {}
    profile = read_json(profile_path)
    profile_html = regex_tags(profile)
    for item in profile_html:
        if item['pk'] == post_id:
            post = item
    data = read_google_json(dict_file_id['bookmarks_fileId'])
    comments = [item for item in read_google_json(dict_file_id['comments_fileid']) if item['post_id'] == post_id]
    return render_template('post.html', **post, comments=comments, count=len(comments), bookmarks=data)


@app.route("/uploads/images/<name>")
def images(name):
    return send_from_directory(images_path, name)


@app.route("/search", methods=["GET"])
def search_():
    try:
        search = request.args.get('s')
        items = [item for item in read_json(profile_path) if search in item['content']]
        comments = counts_comments(items[:10], dict_file_id['comments_fileid'])
        return render_template('search.html', comments=comments, items=items, count=len(items), search=search)
    except:
        return '', 400


@app.route("/users/<username>")
def username_(username):
    profile = read_json(profile_path)
    items = [item for item in regex_tags(profile) if item['poster_name'] == username]
    comments = counts_comments(items, dict_file_id['comments_fileid'])
    data = read_google_json(dict_file_id['bookmarks_fileId'])
    return render_template('user-feed.html', comments=comments, items=items, bookmarks=data)


@app.route("/tag/<tagname>", methods=["GET"])
def page_tag(tagname):
    if not tagname:
        return "Record not found", 400
    profile = read_json(profile_path)
    items = search_tag(tagname, profile)
    comments = counts_comments(items, dict_file_id['comments_fileid'])
    return render_template('tag.html', items=items, comments=comments, tagname=tagname)


@app.route("/bookmarks/add/<int:post_id>")
def bookmarks_add(post_id):
    add_bookmarks(post_id, dict_file_id['bookmarks_fileId'])
    return redirect("/", code=302)


@app.route("/bookmarks/")
def bookmarks_():
    data = read_google_json(dict_file_id['bookmarks_fileId'])
    items = [item for item in read_json(profile_path) if item['pk'] in data]
    comments = counts_comments(items, dict_file_id['comments_fileid'])
    return render_template('bookmarks.html', items=items, comments=comments)


@app.route("/bookmarks/remove/<int:post_id>")
def delete_bookmarks_(post_id):
    delete_bookmarks(post_id, dict_file_id['bookmarks_fileId'])
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run('127.0.0.1', 8000)
