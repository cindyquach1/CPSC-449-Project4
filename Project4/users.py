import sys
import textwrap
import logging.config
import sqlite3
import re

import bottle
from bottle import get, post, delete, error, abort, request, response, HTTPResponse
from bottle.ext import sqlite

# Set up app, plugins, and logging
#
app = bottle.default_app()
app.config.load_config('./etc/api.ini')

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

#   Registers a new user account. 
#   Returns true if username is available, email address is valid, 
#   and password meets complexity requirements.
@post('/users/')
def createUser(db):
    user = request.json
    #logging.debug(user)
    if not user:
        abort(400)

    posted_fields = user.keys()
    required_fields = {'username', 'email', 'pw'}

    if not required_fields <= posted_fields:
        abort(400, f'Missing fields: {required_fields - posted_fields}')

# Check if username is available
    checkUsername = query(db, 'SELECT * FROM users WHERE username = ?;', [user['username']])
    logging.debug(checkUsername)
    if checkUsername:
        abort(400, "Username taken, try again.")
# Check for valid email
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not(re.search(regex, user['email'])):
        abort(400, "Email invalid, try again.")

# Check for valid password
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    pat = re.compile(reg)
    match = re.search(pat, user['pw'])
    if not match:
        abort(400, "Password invalid, try again.")

    try:
        user['id'] = execute(db, '''
            INSERT INTO users(username, email, pw)
            VALUES(:username, :email, :pw)
            ''', user)
    except sqlite3.IntegrityError as e:
        abort(409, str(e))
    
    response.status = 201
    response.set_header('Location', f"/users/{user['id']}")

    return user

#   Returns true if the password parameter matches the password stored for the username.
@get('/users/<username>/')
def checkPassword(username, db):
    user = request.json
    if not user:
        abort(400)
    posted_fields = user.keys()
    required_fields = {'pw'}
    logging.debug(user)
    if not required_fields <= posted_fields:
        abort(400, f'Missing fields: {required_fields - posted_fields}')

    checkPassword = query(db, 'SELECT * FROM users WHERE username = ? AND pw = ?;', [username, user['pw']])
    logging.debug(checkPassword)
    if not checkPassword:
        abort(400, "Your password doesn't match with what we have, try again.")

    return f'Your password match with user: {username}'

def checkuserNameExist(username, db):
    checkUsername = query(db, 'SELECT * FROM users WHERE username = ?;', [username])
    if not checkUsername:
        return False
    return True

#   Start following a new user.  
@post('/users/<username>/<usernameToFollow>/') 
def addFollower(username, usernameToFollow, db):

    checkUsername1 = checkuserNameExist(username, db)
    if not checkUsername1:
        abort(400, 'Invalid username')
    
    checkUsername2 = checkuserNameExist(usernameToFollow, db)
    if not checkUsername2:
        abort(400, ' Username not found')
    
    try:
        addAFollower = execute(db,'''
                INSERT INTO followers(username, usernameToFollow)
                VALUES(?,?)''',[username, usernameToFollow])
    except sqlite3.IntegrityError as e:
        abort(409, str(e))
    
    response.status = 201
    return f"{username} is now following {usernameToFollow}"

#   Stop following a user.
@delete('/users/<username>/<usernameToRemove>/' )
def removeFollower(username, usernameToRemove, db):

    checkUsername1 = checkuserNameExist(username, db)
    if not checkUsername1:
        abort(400, 'Invalid username')
    
    checkUsername = checkuserNameExist(username, db)
    if not checkUsername:
        abort(400, 'Invalid username')
    
    try:
        removeAFollower = execute(db,'''
                DELETE FROM followers
                WHERE username = ? AND usernameToFollow = ?''',[username, usernameToRemove])
    except sqlite3.IntegrityError as e:
        abort(409, str(e))
    
    response.status = 201
    return f"{username} has unfollowed {usernameToRemove}"
