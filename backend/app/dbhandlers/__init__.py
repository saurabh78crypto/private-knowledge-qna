from app.dbhandlers.qdrant_handler import QdrantHandler

def init_handlers(app):
    app.qdrant_handler = QdrantHandler()