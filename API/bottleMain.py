import bottle
from bottle import HTTPError, run, route, template, request, response, static_file, get, install
from api import getClasses
from sql_ex import Base, Apikey
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine

import menu
import json

engine = create_engine('mysql+pymysql://root:7rebrahuxetrewuc@localhost/apidb?charset=utf8&use_unicode=0', pool_recycle=3600)
Base.metadata.bind = engine

plugin = sqlalchemy.Plugin(
    engine, # SQLAlchemy engine created with create_engine function.
    keyword='db', # Keyword used to inject session database in a route (default 'db').
    create=False, # If it is true, execute `metadata.create_all(engine)` when plugin is applied (default False).
    commit=True, # If it is true, plugin commit changes after route is executed (default True).
    use_kwargs=False # If it is true and keyword is not defined, plugin uses **kwargs argument to inject session database (default False).
)
install(plugin)

# Static Routes
@get('/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='./docs')

@get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='./docs')

@get('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='./docs')

@get('/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
    return static_file(filename, root='./docs')

@route('/docs')
def mainPage():
    return static_file('index.html', root='./docs/')



"""
@api {get} /menu Request Menu information
@apiName GetWholeMenu
@apiVersion 0.1.0
@apiGroup Menu

@apiSuccess {String[]} Term  Dictionary of the terms and their associated term number
@apiSuccess {String[]} End  Time options for when classes can end
@apiSuccess {String[]} GUR/Course Attribute  Dictionary of the GURS and their associated acronyms
@apiSuccess {String[]} Begin  Time options for when classes can begin
@apiSuccess {String[]} Credit Hours  Credit hour options
@apiSuccess {String[]} Instructor  Dictionary of the instructors and their associated instructor number
@apiSuccess {String[]} Subject  Dictionary of the subjects and their associated acronyms
"""
@route('/v1/menu')
def getMenu(db):
    if not request.GET.get('apikey','').strip():
        return json.dumps({"message": "Not authorized - No Key"})
    try:
        apikey = request.GET.get('apikey','').strip()
        key = db.query(Apikey).filter(Apikey.apikey == apikey).one()
        if key:
            return menu.extractData(menu.getHTTP())
    except:
        return json.dumps({"message": "Not authorized - Invalid Key"})


"""
@api {get} /class/:term Request Class information for Term
@apiName GetAllClasses
@apiVersion 0.1.0
@apiGroup Classes

@apiParam {Number} term Class term unique ID.

@apiSuccess {Object[]} Classes  Dictionary of classes sorted by class
@apiSuccess {Object[]} Classes.Class  Class object that has all the information for a class
@apiSuccess {String} Classes.Class.restrictions  Class restrictions or null if none
@apiSuccess {String} Classes.Class.dates  Dates of the class for the quarter (Will be the same for all classes)
@apiSuccess {String} Classes.Class.crenum  Number of credits for course
@apiSuccess {String} Classes.Class.title  Title of class
@apiSuccess {String} Classes.Class.prerequisites  Class prerequisites or null if none
@apiSuccess {String} Classes.Class.crn  Course Reserve Number(CRN)
@apiSuccess {Number} Classes.Class.cap  Class cap
@apiSuccess {String} Classes.Class.time1  Meeting time
@apiSuccess {String} Classes.Class.time2  Second meeting time or null if none
@apiSuccess {String} Classes.Class.class  Class name with the subject and number (i.e. CSCI 101)
@apiSuccess {Number} Classes.Class.avail  Number of available seats
@apiSuccess {String} Classes.Class.gur  GUR/Course Attribute(s) or null if none
@apiSuccess {String} Classes.Class.other  Other information or null if none
@apiSuccess {String} Classes.Class.inst  Class instructor
@apiSuccess {String} Classes.Class.room1  Classroom
@apiSuccess {String} Classes.Class.room2  Second Classroom or null if none
@apiSuccess {String} Classes.Class.addl  Additional Charges
@apiSuccess {Boolean} Classes.Class.open  true if class is open, false if it is closed
@apiSuccess {Number} Classes.Class.enrol  Class restrictions
"""
@route('/v1/class/:term')
def getAllClasses(db, term):
    if not request.GET.get('apikey','').strip():
        return json.dumps({"message": "Not authorized - No Key"})
    try:
        apikey = request.GET.get('apikey','').strip()
        key = db.query(Apikey).filter(Apikey.apikey == apikey).one()
        if key:
            return getClasses('All', term)
    except:
        return json.dumps({"message": "Not authorized - Invalid Key"})



# run(
#         host     = '0.0.0.0',
#         port     = 8080,
#         reloader = True,        # restarts the server every time edit a module file
#         debug    = True         # Comment out it before deploy
#         )
