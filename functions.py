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


def search_tag(tag_name, profile):
    tags = []
    for item in read_json(profile):
        if f"#{tag_name}" in item['content'].lower():
            tags.append(item)
    tag = regex_tags(tags)
    return tag


#Много времени убил на эту функцию не без сторонней помощи, такое ощущение
#что можно было сделать в тысячу раз проще и есть какая-то красивая регулярка
#Буду ждать решения от наставников
#Так же интересно был ли какой-то смысл делать с ней что-то в шаблоне.
def regex_tags(profile):
    regexp = re.compile(r'(?<!>|\w)#{1}\w+')
    for item in profile:
        while re.search(regexp, item['content']) is not None:
            replacement = re.search(regexp, item['content'])[0][1:]
            item['content'] = re.sub(regexp, f'<a href="/tag/{replacement}">#{replacement}</a>',
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

def add_comment(post_id, comment, name, comments_path):
    data = read_json(comments_path)
    data_dict = {
        "post_id": post_id,
        "commenter_name": name,
        "comment": comment,
        "pk": int(data[-1]['pk'] + 1)
    }
    data.append(data_dict)
    with open(comments_path, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)