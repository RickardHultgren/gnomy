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

db.define_table('thedatabase',
    Field('id', 'integer'),
    Field('description', 'string')
)

db.define_table('inventory',
    Field('category', 'string'),
    Field('thedatabase_id', 'reference thedatabase')
)

db.define_table('situation',
    Field('context', 'string'),
    Field('thedatabase_id', 'reference thedatabase')
)

db.define_table('situation_links',
    Field('from_id', 'reference thedatabase'),
    Field('to_id', 'reference thedatabase')
)

db.define_table('ladder',
    Field('thelevel', 'integer'),
    Field('thedatabase_id', 'reference thedatabase')
)

db.define_table('autonomy_subcategory',
    Field('subcategory', 'string'),
    Field('thedatabase_id', 'reference thedatabase')
)

db.define_table('matches_selected',
    Field('Autonomy', 'string'),
    Field('RC', 'string')
)

db.define_table('matches_to_do',
    Field('Autonomy', 'string'),
    Field('thanks', 'string'),
    Field('result_context', 'string'),
    Field('result_situation', 'string')
)



thedatabase_entries = [
    {'description': "Create a portrait of my neighbour"},
    {'description': "I have the permission to paint an image of my neighbour."},
    {'description': "I'm a hobby painter"},
    {'description': "Painting"},
    {'description': "Making friendship with my neighbour."}
]

for entry in thedatabase_entries:
    db.thedatabase.insert(**entry)
    
    
    
    
    
    
def get_data_xml():
    """
    Generates an XML response containing database values in a structure 
    matching the JavaScript data types.
    """
    # Fetch all records from `thedatabase`
    database_entries = db(db.thedatabase).select().as_list()
    
    # Convert database entries into a dictionary structure
    database = {entry["id"]: entry["description"] for entry in database_entries}

    # Define inventory data
    inventory = {
        "Relatedness": sorted([database[1]]),
        "Competence": sorted([database[3]]),
        "Autonomy": sorted([database[2]]),
    }

    # Define situation data
    situation = {
        "Home": [],
        "Work": [],
        "Hobby": [database[4], database[5]],
    }

    # Define situation links
    situation_links = {
        "1": {"from": [database[4]], "to": [database[5]]}
    }

    # Define ladder data
    ladder = {
        "1": [database[1]],
        "2": [database[1]],
        "3": [database[1]],
        "4": [database[1]],
    }

    # Define autonomy subcategory
    autonomy_subcategory = {
        "My": [database[2]],
        "Borrowed": [],
        "Lent": []
    }

    # Construct XML structure
    xml_data = XML(
        f"""
        <data>
            <database>
                {''.join(f'<entry id="{key}">{value}</entry>' for key, value in database.items())}
            </database>
            <inventory>
                <Relatedness>{''.join(f'<item>{item}</item>' for item in inventory["Relatedness"])}</Relatedness>
                <Competence>{''.join(f'<item>{item}</item>' for item in inventory["Competence"])}</Competence>
                <Autonomy>{''.join(f'<item>{item}</item>' for item in inventory["Autonomy"])}</Autonomy>
            </inventory>
            <contexts>
                <Home />
                <Work />
                <Hobby>{''.join(f'<item>{item}</item>' for item in situation["Hobby"])}</Hobby>
            </contexts>
            <situationLinks>
                <link id="1">
                    <from>{situation_links["1"]["from"][0]}</from>
                    <to>{situation_links["1"]["to"][0]}</to>
                </link>
            </situationLinks>
            <ladder>
                {''.join(f'<level id="{key}"><item>{value[0]}</item></level>' for key, value in ladder.items())}
            </ladder>
            <autonomySubCategory>
                <My>{''.join(f'<item>{item}</item>' for item in autonomy_subcategory["My"])}</My>
                <Borrowed />
                <Lent />
            </autonomySubCategory>
        </data>
        """
    )

    # Return XML response
    response.headers['Content-Type'] = 'application/xml'
    return xml_data

    
    
    
    
    
    
    
    
    





   
    
    
    
    















# Define tables
db.define_table('collection',
    Field('name'),
    Field('created_by', db.auth_user, default=me, writable=False, readable=False),
    Field('created_on', 'datetime', default=request.now, writable=False, readable=False),
    format='%(name)s'
)

db.define_table('node',
    Field('collection', 'reference collection'),
    Field('name'),
    Field('start_node', 'boolean', default=False),
    Field('parent_node', 'reference node', default=None),
    Field('ICD9'),
    Field('data_type', requires=IS_IN_SET(['Procedure','Factor binary'])),
    Field('created_by', db.auth_user, default=me, writable=False, readable=False),
    Field('created_on', 'datetime', default=request.now, writable=False, readable=False),
    format='%(name)s'
)
db.node.data_type.default = 'Procedure'
db.node.parent_node.requires = IS_EMPTY_OR(IS_IN_DB(db(db.node.collection == session.coll_id), 'node.id', '%(name)s'))

db.define_table('next_node',
    Field('name', 'list:reference project'),
    Field('created_by', db.auth_user, default=me, writable=False, readable=False),
    Field('created_on', 'datetime', default=request.now, writable=False, readable=False),
    format='%(name)s'
)

db.define_table('next_node_list',
    Field('node', db.node, requires=IS_IN_DB(db(db.node.collection == session.coll_id), db.node, '%(name)s')),
    Field('next_node', db.node, requires=IS_IN_DB(db(db.node.collection == session.coll_id), db.node, '%(name)s')),
    Field('created_by', db.auth_user, default=me, writable=False, readable=False),
    Field('created_on', 'datetime', default=request.now, writable=False, readable=False),
    format='%(node)s'
)

db.define_table('collection_list',
    Field('node'),
    Field('collection'),
    Field('created_by', db.auth_user, default=me, writable=False, readable=False),
    Field('created_on', 'datetime', default=request.now, writable=False, readable=False)
)

# Table for operators
db.define_table('operators',
    Field('the_value', 'string')
)

# Table for equation components
db.define_table('equation_components',
    Field('equation_id'),  # Reference to equation
    Field('component_type', requires=IS_IN_SET(['number', 'operator'])),
    Field('component_id'),  # Reference to numbers or operators
    Field('parenthesis', 'string')  # Store 'open' or 'close'
)

# Table for equations
db.define_table('equation',
    Field('equation_name'),
    Field('equation_description')
)
