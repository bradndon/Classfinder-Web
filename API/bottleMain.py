import bottle
from bottle import HTTPError, run, route, template, request, response
from api import getClasses
import menu
import json



@route('/menu')
def getLighter():
    return menu.extractData(menu.getHTTP())

@route('/class/:term')
def getAllClasses(term):
    return getClasses('All', term)


# run(
#         app,                    # Run |app| Bottle() instance
#         host     = '0.0.0.0',
#         port     = 8080,
#         reloader = True,        # restarts the server every time edit a module file
#         debug    = True         # Comment out it before deploy
#         )
