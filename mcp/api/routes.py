from mcp.api import server, source, user

routes = {}

routes.update(server.routes)
routes.update(source.routes)
routes.update(user.routes)
