import praw
from functools import partial
import os
import credentials
from pprint import pprint
import platform

####################### Credentials ##################################
reddit = praw.Reddit(client_id= credentials.login['client_id'],
                     client_secret= credentials.login['client_secret'],
                     username= credentials.login['username'],
                     password= credentials.login['password'],
                     user_agent= credentials.login['user_agent'])
######################################################################

continued = True

def get_posts():
    print('Subreddit: ')
    subred = input()
    print(90 * '-')
    subreddit = reddit.subreddit(subred)
    top_posts = subreddit.hot(limit=20)
    top = []
    for index, submission in enumerate(top_posts):
        print(str(index + 1) + '. ' + submission.title)
        top.append(submission)

    print(90 * '-')
    print('choose a post: ')
    number = input()
    try:
        number = int(number) - 1
    except ValueError:
        print("not a valid number \n")
        get_posts()

    print('\n' + top[number].id)
    print('\n' + 'Upvotes: ' + str(top[number].score))
    print('\n' + top[number].selftext + '\n' + top[number].url)
    print('\n' + 40 * '-' + 'END OF POST' + 40 * '-' + '\n')

    return top[number]

def get_comment(top_post):
    top_post.comments.replace_more(limit=0)
    for comment in top_post.comments:
        print('{' + str(comment.score) + '} >> ' + comment.body)
    print('\n' + 40 * '-' + 'END OF Comments' + 40 * '-' + '\n')


def all_comments(top_post):
    top_post.comments.replace_more(limit=0)
    comments = top_post.comments.list()
    d = {}
    for comment in comments:
        if comment.id not in d.keys():
            d[comment.id] = {'id': comment.id,
                             'parent_id': comment.parent().id,
                             'body': comment.body,
                             'children': []}

    for c in list(d.keys())[::-1]:
        comment = d[c]
        if comment['parent_id'] != top_post.id:
            d[comment['parent_id']]['children'].append(comment)
            del d[c]

    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    p(list(d.values()), top_post.id)

    return d

def p(coms, post_id, depth=0):
    for comobj in coms:
        if comobj['parent_id'] == post_id:
            print('-' * 80)
        print(depth * '>>>> ' + comobj['body'] + '\n')
        if len(comobj['children']) > 0:
            p(comobj['children'], post_id, depth = depth+1)
        
def back():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    global post_lst
    post_lst = get_posts()

def stop_browsing():
    global continued
    continued = False
    os.system("cls")

def help():
    print(
        "\n(m) Top comments for this post \n"
        "(lm) All comments for this post \n"
        "(b) Back to subreddit \n"
        "(q or quit) Stop browsing \n"
    )
    looper()
#############################################################
# Endless Browse

def looper():
    print('options: ')
    try:
        num = input()
    except TypeError:
        print("\n \n")
        looper()

    switcher = {
        'm': partial(get_comment, post_lst),
        'lm': partial(all_comments, post_lst),
        'b': back,
        'back': back,
        'q': stop_browsing,
        'quit': stop_browsing,
        '-h': help,
        'h': help,
        'help': help
    }
    func = switcher.get(num, lambda: "invalid option")
    func()


#############################################################
# Run
post_lst = get_posts()
while continued:
    looper()
