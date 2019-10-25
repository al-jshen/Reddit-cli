import praw
from functools import partial
import os
import credentials

reddit = praw.Reddit(client_id= credentials.login['client_id'],
                     client_secret= credentials.login['client_secret'],
                     username= credentials.login['username'],
                     password= credentials.login['password'],
                     user_agent= credentials.login['user_agent'])

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
    number = int(input()) - 1
    print('\n' + 'Upvotes: ' + str(top[number].score))
    print('\n' + top[number].selftext + '\n' + top[number].url)
    print('\n' + 40 * '-' + 'END OF POST' + 40 * '-' + '\n')

    return top[number]

def get_comment(top_post):
    for comment in top_post.comments:
        print('{' + str(comment.score) + '} >> ' + comment.body)
    print('\n' + 40 * '-' + 'END OF Comments' + 40 * '-' + '\n')

def back():
    os.system("cls")
    global post_lst
    post_lst = get_posts()

def stop_browsing():
    global continued
    continued = False
    os.system("cls")

def help():
    print(
        "\n(m) Read comments for this post \n"
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