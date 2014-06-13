# coding: utf8
@auth.requires_login()
def post():
    return dict(form=SQLFORM(db.comment_post).process(),
                comments=db(db.comment_post).select())
