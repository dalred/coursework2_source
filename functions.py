import json
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