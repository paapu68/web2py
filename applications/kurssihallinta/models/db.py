#Heroku begin
from gluon.tools import Auth

def format_opiskelija(record):
    """ opiskelijan esitys """
    return '%s %s' % (record.opiskelija.user_id.last_name,
                      record.opiskelija.user_id.last_name)

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    try: db = DAL(os.environ.get('DATABASE_URL'))
    except: db = DAL('sqlite://storage.sqlite')
#Heroku end
auth = Auth(db)
auth.define_tables(username=True)

db.define_table('opettaja',
   Field('user_id', 'reference auth_user'),
                format=lambda r: '%s %s' \
                    % (db.auth_user[r.user_id].last_name,
                       db.auth_user[r.user_id].first_name))

db.define_table('opiskelija',
                Field('user_id', 'reference auth_user'),
                format=lambda r: '%s %s' \
                    % (db.auth_user[r.user_id].last_name,
                       db.auth_user[r.user_id].first_name))

db.define_table('kurssi',
   Field('title', unique=True),
   Field('opettaja_id', 'reference opettaja'),
   format = '%(title)s')

db.define_table('kurssityon_nimi',
   Field('title'),
   Field('kurssi_id','reference kurssi'),
   Field('opettaja_id', 'reference opettaja'),
   #format = '%(title)s')
   format = lambda r: '%s %s' \
                    % (r.title,  \
                           '('+db.kurssi[r.kurssi_id].title+')')
   )             

db.define_table('kurssityo',
   Field('kurssityon_nimi','reference kurssityon_nimi'),
   Field('palautettu', 'upload'),
   Field('korjattu', 'upload',writable = auth.has_membership(auth.id_group('opettaja'))),
   Field('arvosana',writable = auth.has_membership(auth.id_group('opettaja'))),
   Field('kurssi_id', 'reference kurssi'),
   Field('opiskelija_id', 'reference opiskelija'),
   format=lambda r: '%s' \
       % (db.kurssityon_nimi[r.kurssityon_nimi].title)
   )

db.kurssi.title.requires = IS_NOT_IN_DB(db, db.kurssi.title)
db.kurssityon_nimi.title.requires = IS_NOT_IN_DB(db, db.kurssityon_nimi.title)

