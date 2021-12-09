import json, re
def read_json(name):
    with open(name, "r", encoding='utf-8') as file:
        return json.load(file)

def counts_comments(items, comments_path):
    item_pk = [item['pk'] for item in items]
    comments_list_by_posts = {}
    for comments in read_json(comments_path):
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

def view_tag(profile_path):
    tags = []
    for i in read_json(profile_path):
        for tag in i['content'].split():
            if tag.startswith("#"):
                tags.append(tag.lstrip("#").lower())
    tags = set(tags)
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

def serialize_sets(obj):
    if isinstance(obj, set):
        return list(obj)
    return obj

def add_bookmarks(post_id, bookmarks_path):
    data = read_json(bookmarks_path)
    data.append(post_id)
    with open(bookmarks_path, "w", encoding='utf-8') as f:
        json.dump(set(data), f, default=serialize_sets)

def delete_bookmarks(post_id, bookmarks_path):
    data = read_json(bookmarks_path)
    data.remove(post_id)
    with open(bookmarks_path, "w", encoding='utf-8') as f:
        json.dump(set(data), f, default=serialize_sets)