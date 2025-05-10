# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False
#mail = auth.settings.mailer
#mail.settings.server = 'smtp.gmail.com:587'
#mail.settings.sender = 'your_email@gmail.com'
#mail.settings.login = 'your_email@gmail.com:your_password'
#mail.settings.tls = True

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)

if auth.is_logged_in():
   me=auth.user.id
else:
   me=None

#for the context:
db.define_table('pond',
    Field('name'),
    Field('created_by', 'reference auth_user', default=lambda: auth.user.id if auth.user else None, readable=False, writable=False),
    Field('created_on','datetime',default=request.now,writable=False,readable=False) # ,           
    #format='%(name)s'


    #Field('created_by', 'reference auth_user', default=lambda: auth.user.id if auth.user else None, readable=False, writable=False)
)



#db.pond._permissions = {
#    'create': auth.has_permission('create', db.pond),
#    'read': auth.has_permission('read', db.pond),
#    'update': auth.has_permission('update', db.pond),
#    'delete': auth.has_permission('delete', db.pond),
#}

#for the situation:
db.define_table('rootstock',
    Field('pond', 'reference pond'),
    Field('name'),
    Field('created_by', 'reference auth_user', default=lambda: auth.user_id, writable=False, readable=False),
    Field('created_on','datetime',default=request.now,writable=False,readable=False)         ,  
    format='%(name)s'           
               )
try:
    db.rootstock.pond.id = session.pond_id
except:
    pass

#for the next context:
db.define_table('knotstock',
    Field('name', 'list:reference project'),
    Field('created_by',db.auth_user,default=me,writable=False,readable=False),
    Field('created_on','datetime',default=request.now,writable=False,readable=False)             ,
    format='%(name)s'           
               )

#db.define_table('boat',
#    Field('name'),
#    Field('category'),
#    Field('created_by',db.auth_user,default=me,writable=False,readable=False),
#    Field('created_on','datetime',default=request.now,writable=False,readable=False)             
#               )

#db.define_table('knotstock_list',
#    Field('rootstock', requires=IS_IN_DB(db, db.rootstock, '%(name)s')),
#    Field('knotstock',db.rootstock
#         ),                
#    Field('created_by',db.auth_user,default=me,writable=False,readable=False),
#    Field('created_on','datetime',default=request.now,writable=False,readable=False)             ,
#    format='%(rootstock)s'           
#               )
# Define the table 'knotstock_list'
db.define_table(
    'tendril',
    Field('name'),
    Field('rootstock', db.rootstock, requires=IS_IN_DB(db(db.rootstock.pond == session.pond_id), db.rootstock, '%(name)s')),
    Field('knotstock', db.rootstock, requires=IS_IN_DB(db(db.rootstock.pond == session.pond_id), db.rootstock, '%(name)s')),
    #Field('boat', 'reference boat'),            
    Field('boat'),            
    Field('root'),
    Field('created_by', db.auth_user, default=auth.user_id, writable=False, readable=False),
    Field('created_on', 'datetime', default=request.now, writable=False, readable=False),
    format='%(rootstock)s'
)

#Team
#db.define_table('team',
    #Field('name'),
     #Field('gnomeREF'),
     #Field('flowerREF'),
    #Field('description'),
    #Field('category'),
    #Field('created_by',db.auth_user,default=me,writable=False,readable=False),
    #Field('created_on','datetime',default=request.now,writable=False,readable=False)             
#               )



#for the emotions:
# Define the table 'flower'
db.define_table(
    'flower',
    Field('name'),
    Field('rootstock', db.rootstock, requires=IS_IN_DB(db(db.rootstock.pond == session.pond_id), db.rootstock, '%(name)s')),
    Field('fruit'),
    Field('color'),
    Field('team'),            
    #Field('team', 'reference team'),            
     #Field('teamsREF'),
    Field('created_by', db.auth_user, default=auth.user_id, writable=False, readable=False),
    Field('created_on', 'datetime', default=request.now, writable=False, readable=False),
    format='%(rootstock)s'
)

# Now 'rootstock' and 'knotstock' fields in 'knotstock_list' table will be restricted
# to rootstocks that belong to the pond specified by session.pond_id


#db.define_table('pond_list',
#    Field('rootstock'),
#    Field('pond'),                
#    Field('created_by',db.auth_user,default=me,writable=False,readable=False),
#    Field('created_on','datetime',default=request.now,writable=False,readable=False)             
#               )


#db.define_table('gnome',
#    Field('name'),
#    Field('category'),
#    Field('information'),
#    Field('created_by',db.auth_user,default=me,writable=False,readable=False),
#    Field('created_on','datetime',default=request.now,writable=False,readable=False)             
#               )

#db.define_table('team_gnome',
#    Field('gnome', 'reference gnome'),            
#    Field('team', 'reference team'),            
#    Field('created_by',db.auth_user,default=me,writable=False,readable=False),
#    Field('created_on','datetime',default=request.now,writable=False,readable=False)             
#               )

#db.define_table('flower_team',
#    Field('team', 'reference team'),            
#    Field('flower', 'reference flower'),            
#    Field('created_by',db.auth_user,default=me,writable=False,readable=False),
#    Field('created_on','datetime',default=request.now,writable=False,readable=False)             
#               )               

db.define_table('flask',
    Field('name'),
    Field('category'),
    Field('powders'),
    Field('created_by',db.auth_user,default=me,writable=False,readable=False),
    Field('created_on','datetime',default=request.now,writable=False,readable=False)             
               )

db.define_table('spell',
    Field('name'),
    Field('category'),
    Field('formula'),
    Field('created_by',db.auth_user,default=me,writable=False,readable=False),
    Field('created_on','datetime',default=request.now,writable=False,readable=False)             
               )

db.define_table('spell_list',
    Field('spell'),
    Field('contract'),
    Field('created_by',db.auth_user,default=me,writable=False,readable=False),
    Field('created_on','datetime',default=request.now,writable=False,readable=False)             
               )               















# Table for operators
db.define_table(
    'operators',
    Field('the_value', 'string')
)

# Table for equation components
db.define_table(
    'equation_components',
    Field('equation_id'),# 'reference equation'),
    Field('component_type', requires=IS_IN_SET(['number', 'operator'])),
    Field('component_id'),# 'reference numbers' or 'reference operators'),
    Field('parenthesis', 'string')  # You can store 'open' or 'close' here
)

# Table for equations
db.define_table(
    'equation',
    Field('equation_name'),
    Field('equation_description')
)
