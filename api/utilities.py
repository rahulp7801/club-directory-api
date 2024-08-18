# '''

# This utils model is generally the entire backend for our project.
# It makes the app.py file with the routes look simple but all the
# detailed coding will be here and utilized there in a simple manner.

# So far this is just being used for login/registration purposes but as

# we need features those will go here too (like API stuff ya feel).


# BCRYPT is the module we are using for encryption of passwords/user IDs
# Introduce the firebase module to work with Google Authentication (trust)
# '''


from flask import make_response



# # Initialize CORS
def init_curs():
    response = make_response()
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
