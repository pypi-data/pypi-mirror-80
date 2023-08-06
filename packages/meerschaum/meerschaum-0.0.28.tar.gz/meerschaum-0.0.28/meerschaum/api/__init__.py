#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

__version__ = "0.0.5"
from meerschaum.config import system_config
from meerschaum.connectors import get_connector
from meerschaum.utils.misc import attempt_import
fastapi, graphene, starlette_graphql = attempt_import('fastapi', 'graphene', 'starlette.graphql', lazy=True)

connector = get_connector(type="sql", label="meta")
database = connector.db

### TODO move GraphQL queries somewhere
class Query(graphene.ObjectType):
    hello = graphene.String(
        name = graphene.String(default_value="stranger")
    )
    def resolve_hello(self, info, name):
        return 'hello' + name

sys_config = system_config['api']
fast_api = fastapi.FastAPI()
fast_api.add_route("/graphql", starlette_graphql.GraphQLApp(schema=graphene.Schema(query=Query)))

endpoints = sys_config['endpoints']

### import WebAPI routes
import meerschaum.api.routes as routes
import meerschaum.api._events

