from mcp.api import mcp, servers, sources, users

routes = {}

routes.update(mcp.routes)
routes.update(servers.routes)
routes.update(sources.routes)
routes.update(users.routes)

__all__ = ['routes']
