def setup_swagger(docs, app):
    docs.init_app(app)

    api_key_scheme = {
        "type": "apiKey",
        "scheme": "Bearer",
        "in": "header",
        "name": "Authorization",
        "description": "API Key",
    }
    docs.spec.components.security_scheme("Bearer", api_key_scheme)
    docs.spec.options["security"] = [{"Bearer": []}]
    return docs
