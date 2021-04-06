import sys
import textwrap
import logging.config
import sqlite3

import bottle
from bottle import get, post, error, abort, request, response, HTTPResponse
from bottle.ext import sqlite

# Set up app, plugins, and logging
#
app = bottle.default_app()
app.config.load_config('./etc/timelines.ini')

plugin = sqlite.Plugin(app.config['sqlite.dbfile'])
app.install(plugin)

logging.config.fileConfig(app.config['logging.config'])


# Return errors in JSON
#
# Adapted from # <https://stackoverflow.com/a/39818780>
#
def json_error_handler(res):
    if res.content_type == 'application/json':
        return res.body
    res.content_type = 'application/json'
    if res.body == 'Unknown Error.':
        res.body = bottle.HTTP_CODES[res.status_code]
    return bottle.json_dumps({'error': res.body})


app.default_error_handler = json_error_handler

# Disable warnings produced by Bottle 0.12.19.
#
#  1. Deprecation warnings for bottle_sqlite
#  2. Resource warnings when reloader=True
#
# See
#  <https://docs.python.org/3/library/warnings.html#overriding-the-default-filter>
#
if not sys.warnoptions:
    import warnings
    for warning in [DeprecationWarning, ResourceWarning]:
        warnings.simplefilter('ignore', warning)


# Simplify DB access
#
# Adapted from
# <https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/#easy-querying>
#
def query(db, sql, args=(), one=False):
    cur = db.execute(sql, args)
    rv = [dict((cur.description[idx][0], value)
          for idx, value in enumerate(row))
          for row in cur.fetchall()]
    cur.close()

    return (rv[0] if rv else None) if one else rv


def execute(db, sql, args=()):
    cur = db.execute(sql, args)
    id = cur.lastrowid
    cur.close()

    return id


# Check if username exists
def checkuserNameExist(username, db):
    checkUsername = query(db, 'SELECT * FROM users WHERE username = ?;', [username])
    if not checkUsername:
        return False
    return True

# Returns recent posts from a user.
@get('/timelines/<username>/')
def getUserTimeline(username, db):
    logging.debug(username)
    checkUsername = checkuserNameExist(username, db)
    if not checkUsername:
        abort(400, 'Invalid Username')
    logging.debug(checkUsername)    
    userPosts = query(db, 'SELECT * FROM posts WHERE username = ? ORDER BY timestamp DESC LIMIT 25;', [username])
    logging.debug(userPosts)
    return {f"{username}'s Timeline" : userPosts}


#   Returns recent posts from all users.
@get('/timelines/public/')
def getPublicTimeline(db):
    
    allPosts = query(db, 'SELECT * FROM posts ORDER BY timestamp DESC LIMIT 25;')

    return {'Public Timeline': allPosts}


#   Returns recent posts from all users that this user follows.
@get('/timelines/<username>/followings/')
def getHomeTimeline(username, db):
    
    checkUsername1 = checkuserNameExist(username, db)
    if not checkUsername1:
        abort(400, 'Invalid Username')

    # followingsPosts = query(db, '''SELECT * 
    #                             FROM posts 
    #                             WHERE username IN ( 
    #                                 SELECT usernameToFollow 
    #                                 FROM followers 
    #                                 WHERE username = ?)''', [username])
                                

    followingsPosts = query(db, '''SELECT DISTINCT *
                                    FROM posts
                                    INNER JOIN followers ON posts.username=followers.usernameToFollow
                                    WHERE followers.username = ?
                                    ORDER BY timestamp DESC LIMIT 2;''', [username])


    return {'followingsPosts':followingsPosts}


#   Post a new tweet.
@post('/timelines/<username>/')
def postTweet(username, db):
    user = request.json
    #logging.debug(user)
    if not user:
        abort(400)

    posted_fields = user.keys()
    required_fields = {'post'}

    if not required_fields <= posted_fields:
        abort(400, f'Missing fields: {required_fields - posted_fields}')

    checkUsername = checkuserNameExist(username, db)
    if not checkUsername:
        abort(400, 'Invalid username')
    
    try:
        addPost = execute(db,'''
                INSERT INTO posts(username, post)
                VALUES(?,?)''',[username, user['post']])
    except sqlite3.IntegrityError as e:
        abort(409, str(e))

    response.status = 201
    return f"{username} just tweeted!"

