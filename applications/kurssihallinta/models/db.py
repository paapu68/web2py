#Heroku begin
from gluon.tools import Auth

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    try: db = DAL(os.environ.get('DATABASE_URL'))
    except: db = DAL('sqlite://storage.sqlite')
#Heroku end
auth = Auth(db)
auth.define_tables(username=True)

db.define_table('kurssi',
   Field('title', unique=True),
   format = '%(title)s')

db.define_table('tyo',
   Field('title', unique=True),
   Field('kurssi_id', 'reference kurssi'),
   format = '%(title)s')

db.define_table('oppilas',
   Field('user_id', 'reference auth_user'),
   Field('kurssi_id', 'reference kurssi'),
   Field('tyo_id', 'reference tyo'),
   format = '%(auth.user.last_name)s')

db.define_table('opettaja',
   Field('user_id', 'reference auth_user'),
   Field('kurssi_id', 'reference kurssi'),
   Field('tyo_id', 'reference tyo'),
   Field('oppilas_id', 'reference oppilas'),
   format = '%(auth.user.last_name)s')

db.define_table('kurssityo',
   Field('palautettu', 'upload'),
   Field('korjattu', 'upload'),
   Field('arvosana'),
   Field('kurssi_id', 'reference kurssi'),
   Field('tyo_id', 'reference tyo'),
   Field('oppilas_id', 'reference oppilas'),
   format = '%(id)s')

#db.tyo.title.requires = IS_NOT_IN_DB(db, db.tyo.title)
#db.post.image_id.requires = IS_IN_DB(db, db.image.id, '%(title)s')
#db.post.author.requires = IS_NOT_EMPTY()
#db.post.email.requires = IS_EMAIL()
#db.post.body.requires = IS_NOT_EMPTY()

#db.post.image_id.writable = db.post.image_id.readable = False
