from mcp.api import mcp, server, source, user

routes = {}

routes.update(mcp.routes)
routes.update(server.routes)
routes.update(source.routes)
routes.update(user.routes)

__all__ = ['routes']
