import json, re
from google_authentication import *

def read_json(name):
    with open(name, "r", encoding='utf-8') as file:
        return json.load(file)

def counts_comments(items, file_id):
    item_pk = [item['pk'] for item in items]
    comments_list_by_posts = {}
    for comments in read_google_json(file_id):
        if comments['post_id'] in item_pk:
            if comments['post_id'] not in comments_list_by_posts.keys():
                comments_list_by_posts[comments['post_id']] = 1
            else:
                comments_list_by_posts[comments['post_id']] += 1
    return comments_list_by_posts


def search_tag(tag_name, profile_path):
    tags = []
    for item in read_json(profile_path):
        if f"#{tag_name}" in item['content'].lower():
            tags.append(item)
    return tags


#Много времени убил на эту функцию не без сторонней помощи, такое ощущение
#что можно было сделать в тысячу раз проще и есть какая-то красивая регулярка
#Буду ждать решения от наставников
#Так же интересно был ли какой-то смысл делать с ней что-то в шаблоне.
def regex_tags(profile_path):
    regexp = re.compile(r'(?<!>|\w)#{1}\w+')
    profile = read_json(profile_path)
    for item in profile:
        while re.search(regexp, item['content']) is not None:
            replacement = re.search(regexp, item['content'])[0][1:]
            item['content'] = re.sub(regexp, f'<a href="/tag/{replacement}#{replacement}">#{replacement}</a>',
                                     item['content'],
                                     count=1)
    return profile



def add_bookmarks(post_id, file_id):
    data = read_google_json(file_id)
    data.append(post_id)
    add_json_file(data, file_id)

def delete_bookmarks(post_id, file_id):
    data = read_google_json(file_id)
    data.remove(post_id)
    add_json_file(data, file_id)

def add_comment(post_id, comment, name, file_id):
    data = read_google_json(file_id)
    data_dict = {
        "post_id": post_id,
        "commenter_name": name,
        "comment": comment,
        "pk": int(data[-1]['pk'] + 1)
    }
    data.append(data_dict)
    add_json_file(data, file_id)