# CPSC-449-Project4
Group members: Cindy Quach, Dalisa Nguyen, Tevin Vu

1. In the terminal, run this command to start microservices

foreman start 

2. Gateway

Testing request made to port 5000 are successfully proxied to the Users service.

$ http POST localhost:5000/users/ username=tester email=test@example.com pw=testing
HTTP/1.0 201 Created
Content-Length: 71
Content-Type: application/json
Date: Sun, 04 Apr 2021 22:54:32 GMT
Link: </users/8>; rel=self, </users/8>; rel=related
Server: Werkzeug/1.0.1 Python/3.8.5

{
    "email": "test@example.com",
    "id": 8,
    "pw": "testing",
    "username": "tester"
}

3. Configuration

Take a look at etc/gateway.ini

If the provided URL includes 'users' or 'followers', the request is routed to the users service through port 5100. If the provided URL includes 'posts', the request is routed to the timelines service through port 5200. When the same request is made by different users, the request is routed to instances of the same (timelines)service through ports such as 5201 and 5202.
[routes]
'/users/' = ["http://localhost:5100"] 
'/posts/' = ["http://localhost:5200", "http://localhost:5201", "http://localhost:5202"]
'/followers/' = ["http://localhost:5100"] 



4. Routing

Take a look at gateway.py @route and gateway().
Requests made to the User services are routed from port 5000 to port 5100.
Requests made to the Timelines services are routed from port 5000 to port 5200.

Sample API calls for TESTING:

$ http GET 'localhost:5000/users/?username=JohnLegend&pw=John*123'
HTTP/1.0 200 OK
Content-Length: 104
Content-Type: application/json
Date: Sun, 04 Apr 2021 23:04:38 GMT
Etag: "2498c55731d598b4ee08eb64cd5500db"
Server: Werkzeug/1.0.1 Python/3.8.5

{
    "resources": [
        {
            "email": "JohnLegend@csu.fullerton.edu",
            "id": 1,
            "pw": "John*123",
            "username": "JohnLegend"
        }
    ]
}

$ http POST localhost:5000/followers/ username=ElonMusk usernameToFollow=JohnLegend
HTTP/1.0 201 Created
Content-Length: 64
Content-Type: application/json
Date: Sun, 04 Apr 2021 23:17:49 GMT
Link: </followers/11>; rel=self, </followers/11>; rel=related, </users/5>; rel=related
Server: Werkzeug/1.0.1 Python/3.8.5

{
    "id": 11,
    "username": "ElonMusk",
    "usernameToFollow": "JohnLegend"
}


removefollower() -- did not get this work 
id=$(http GET 'localhost:5000/followers/?username=JohnLegend&usernameToFollow=TaylorSwift' | jq .resources[0].id)
student@tuffix-vm:~/Desktop/P2/CPSC-449-Project2/Project2$ http DELETE localhost:5000/followers/$id
HTTP/1.0 500 Internal Server Error
Content-Length: 34
Content-Type: application/json
Date: Sun, 04 Apr 2021 23:32:43 GMT
Server: WSGIServer/0.2 CPython/3.8.5

{
    "error": "Internal Server Error"
}


http GET 'localhost:5000/posts/?username=JohnLegend&sort=-timestamp'
HTTP/1.0 200 OK
Content-Length: 202
Content-Type: application/json
Date: Sun, 04 Apr 2021 23:41:04 GMT
Etag: "6821fe5a9cb8fd1522ca5a94902bb01a"
Server: Werkzeug/1.0.1 Python/3.8.5

{
    "resources": [
        {
            "id": 7,
            "post": "Check out my new album!",
            "timestamp": "2021-03-09 06:07:23",
            "username": "JohnLegend"
        },
        {
            "id": 1,
            "post": "All of me",
            "timestamp": "2021-03-09 05:57:51",
            "username": "JohnLegend"
        }
    ]
}


$ http GET localhost:5000/posts/?sort=-timestamp
HTTP/1.0 200 OK
Content-Length: 690
Content-Type: application/json
Date: Sun, 04 Apr 2021 23:42:41 GMT
Etag: "d181728b7db1f50745841a304797d6e7"
Server: Werkzeug/1.0.1 Python/3.8.5

{
    "resources": [
        {
            "id": 7,
            "post": "Check out my new album!",
            "timestamp": "2021-03-09 06:07:23",
            "username": "JohnLegend"
        },
        {
            "id": 1,
            "post": "All of me",
            "timestamp": "2021-03-09 05:57:51",
            "username": "JohnLegend"
        },
        {
            "id": 2,
            "post": "You belong with me",
            "timestamp": "2021-03-09 05:57:51",
            "username": "TaylorSwift"
        },
        {
            "id": 3,
            "post": "Time to tell a story about SPACEX and Tesla",
            "timestamp": "2021-03-09 05:57:51",
            "username": "ElonMusk"
        },
        {
            "id": 4,
            "post": "Good morning",
            "timestamp": "2021-03-09 05:57:51",
            "username": "ElonMusk"
        },
        {
            "id": 5,
            "post": "It's the climb",
            "timestamp": "2021-03-09 05:57:51",
            "username": "MileyCyrus"
        },
        {
            "id": 6,
            "post": "Locked out of heaven",
            "timestamp": "2021-03-09 05:57:51",
            "username": "BrunoMars"
        }
    ]
}


getHomeTimeline(username) -- did not get to work 
friends=$(http GET 'localhost:5200/users/following.json?_facet=username&username=ProfAvery&_shape=array' | jq --raw-output 'map(.friendname) | join(",")')
$ http GET "http://localhost:5300/timelines/posts.json?_sort_desc=timestamp&_shape=array&username__in=$friends"


$ http POST localhost:5000/posts/ username=tester post='This is a test.'
HTTP/1.0 201 Created
Content-Length: 88
Content-Type: application/json
Date: Sun, 04 Apr 2021 23:43:49 GMT
Link: </posts/8>; rel=self, </posts/8>; rel=related
Server: Werkzeug/1.0.1 Python/3.8.5

{
    "id": 8,
    "post": "This is a test.",
    "timestamp": "2021-04-04 23:43:49",
    "username": "tester"
}


5. Adding a new REST endpoint

	We were unable to implement this feature in the gateway.

6. Load Balancing

	To create one instance of the gateway, three instances of timelines, and one instance of users: foreman start -m gateway=1,timelines=3,users=1

	etc/gateway.ini is updated to list a pool of upstream servers for the timelines service ('/posts/' = ["http://localhost:5200", "http://localhost:5201", "http://localhost:5202"])

	We were unable to modify gateway.py to forward each request for that service to an instance in the pool.

7. Authentication

	Call is allowed when user is authenticated, otherwise, 401 Unauthorized is returned.

Testing:
When visiting 'localhost:5000' in browser, a window pops up asking the user for their login information. Inputting the username'JohnLegend' and the password 'John*123' authenticates the user and takes them to a page that says "yo, you are authenticated".  
*incorrect password*
http -a JohnLegend:Jon*1234 GET "http://localhost:5000"
HTTP/1.0 401 Unauthorized
Content-Length: 26
Content-Type: application/json
Date: Tue, 06 Apr 2021 22:41:37 GMT
Server: WSGIServer/0.2 CPython/3.8.5
Www-Authenticate: Basic realm="private"

{
    "error": "Access denied"
}

*correct password*
http -a JohnLegend:John*123 GET "http://localhost:5000"
HTTP/1.0 200 OK
Content-Length: 26
Content-Type: text/html; charset=UTF-8
Date: Tue, 06 Apr 2021 22:41:32 GMT
Server: WSGIServer/0.2 CPython/3.8.5

yo, you are authenticated!

*incorrect username*
http POST localhost:5000/users/ username=tester1 email=test@example.com pw=testing
HTTP/1.0 401 Unauthorized
Content-Length: 26
Content-Type: application/json
Date: Tue, 06 Apr 2021 22:46:53 GMT
Server: WSGIServer/0.2 CPython/3.8.5
Www-Authenticate: Basic realm="private"

{
    "error": "Access denied"
}

