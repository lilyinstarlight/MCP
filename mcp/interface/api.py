from mcp.interface import servers, sources, users

routes = {}

routes.update(servers.routes)
routes.update(sources.routes)
routes.update(users.routes)
