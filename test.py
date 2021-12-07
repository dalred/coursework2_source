from functions import read_json
import os

post_id = 1
poster_name = 'leo'
json_dir = 'data'
BASEDIR = os.path.abspath(os.path.dirname(__file__))
profile_path = os.path.join(BASEDIR, json_dir, 'data.json')
comments_path = os.path.join(BASEDIR, json_dir, 'comments.json')
images_path = os.path.join(BASEDIR, 'static\img')
content = 'тарелка'

items = [item for item in read_json(profile_path) if content in item['content']]
item_pk = [item['pk'] for item in items]
comments_list_by_posts = {}
for comments in read_json(comments_path):
    if comments['post_id'] in item_pk:
        if comments['post_id'] not in comments_list_by_posts.keys():
            comments_list_by_posts[comments['post_id']] = 1
        else:
            comments_list_by_posts[comments['post_id']] += 1

profile = read_json(profile_path)

profile = [item for item in profile]