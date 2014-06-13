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
#   format = '%(id)s')
#   format=lambda r: '%s %s' % (db.auth_user[r.auth_user].first_name,db.auth_user[r.auth_user].last_name))

db.define_table('opiskelija',
                Field('user_id', 'reference auth_user'),
#                format = '%(id)s')
                format=lambda r: '%s %s' \
                    % (db.auth_user[r.user_id].last_name,
                       db.auth_user[r.user_id].first_name))
#   format = '%(user_id.first_name)s %(user_id.last_name)s')
#   format = '%(auth_user.first_name)s')

db.define_table('kurssi',
   Field('title', unique=True),
   Field('opettaja_id', 'reference opettaja'),
   format = '%(title)s')

#liitostaulu, monen suhde moneen oppilaan ja kurssin välillä
#db.define_table('opiskelijatKursseilla',
#   Field('opiskelija_id', 'reference opiskelija'),
#   Field('kurssi_id', 'reference kurssi'),
#   format = '%(title)s')

db.define_table('kurssityon_nimi',
   Field('title'),
   Field('kurssi_id','reference kurssi'),
   Field('opettaja_id', 'reference opettaja'),
   format = '%(title)s')

#sisältää kurssityön nimen, idea että opiskelija voi valita valikosta

db.define_table('kurssityo',
   Field('nimi_id','reference kurssityon_nimi'),
   Field('palautettu', 'upload'),
   Field('korjattu', 'upload',writable = auth.has_permission('opettaja')),
   Field('arvosana',writable = auth.has_permission('opettaja')),
   Field('kurssi_id', 'reference kurssi'),
   Field('opiskelija_id', 'reference opiskelija'),
   format=lambda r: '%s' \
       % (db.kurssityon_nimi[r.nimi_id].title)
   )

#db.kurssityo.arvosana.authorize = auth.requires_membership('opettaja')

#   format = '%(nimi)s')

#db.tyo.title.requires = IS_NOT_IN_DB(db, db.tyo.title)
#db.post.image_id.requires = IS_IN_DB(db, db.image.id, '%(title)s')
#db.post.author.requires = IS_NOT_EMPTY()
#db.post.email.requires = IS_EMAIL()
#db.post.body.requires = IS_NOT_EMPTY()

#db.post.image_id.writable = db.post.image_id.readable = False
