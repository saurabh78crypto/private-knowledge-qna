from app.custom_fastapi import CustomFastAPI

def create_app() -> 'CustomFastAPI':
    from app.dbhandlers import init_handlers
    from app.services import init_services
    from app.routes import init_routes

    app = CustomFastAPI(title="Private Knowledge Q&A")

    init_handlers(app)
    init_services(app)
    init_routes(app)

    return app