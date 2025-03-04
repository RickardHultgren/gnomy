# -*- coding: utf-8 -*-

from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# Configuration
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    db = DAL('google:datastore+ndb')
    session.connect(request, response, db=db)

# Generic patterns for views
response.generic_patterns = []
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# Form style
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# Authentication
auth = Auth(db, host_names=configuration.get('host.names'))
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# Email configuration
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# Auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# Meta information
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# Google Analytics
response.google_analytics_id = configuration.get('google.analytics_id')

# Scheduler
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# Define user id
me = auth.user.id if auth.is_logged_in() else None


###new tables

# Define the 'situation' table
db.define_table('situation',
    Field('tree_name', 'string', notnull=True),
    Field('garden_name', 'string', notnull=True),
    format='%(tree_name)s')

# Define the 'situationTOsituation' table (relationships between situations)
db.define_table('situationTOsituation',
    Field('from_tree', 'reference situation', notnull=True),
    Field('to_tree', 'reference situation', notnull=True))

# Define the 'action_status' table
db.define_table('action_status',
    Field('status_name', 'string', unique=True, notnull=True),
    Field('status_message', 'text'),
    format='%(status_name)s')

# Define the 'autonomy' table
db.define_table('autonomy',
    Field('autonomy_name', 'string', unique=True, notnull=True),
    format='%(autonomy_name)s')

# Define the 'actions2situation' table (tracking actions in situations)
db.define_table('actions2situation',
    Field('situation', 'reference situation', notnull=True),
    Field('date_time', 'datetime', notnull=True),
    Field('action_status', 'reference action_status', notnull=True),
    Field('status_message', 'text'),
    Field('autonomy', 'reference autonomy'))

# Define the 'autonomy TO relatedness AND com' table (mapping autonomy to relatedness & competence)
db.define_table('autonomy_to_relatedness_competence',
    Field('autonomy', 'reference autonomy', notnull=True),
    Field('relatedness_and_competence', 'reference relatedness_and_competence', notnull=True))

# Define the 'relatedness AND competence' table
db.define_table('relatedness_and_competence',
    Field('relatedness_and_competence_name', 'string', unique=True, notnull=True),
    format='%(relatedness_and_competence_name)s')
