from app.neoDB import allResources

from flask import current_app, g

def get_db()  -> allResources:
    if 'db' not in g:
        g.db = allResources(
            "neo4j://localhost:7474",
            "neo4j",
            "neo4j"
        )
    return g.db
def init_app(app):
    app.teardown_appcontext(close_db)
    
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()