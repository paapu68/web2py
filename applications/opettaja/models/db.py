#Heroku begin
from gluon.tools import Auth

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    try: db = DAL(os.environ.get('DATABASE_URL'))
    except: db = DAL('sqlite://storage.sqlite')
#Heroku end
auth = Auth(db)
auth.define_tables(username=True)

db.define_table('kurssit',
   Field('title', unique=True),
   format = '%(title)s')
