"""
Python HTTP server for GraphQL.
"""
from flask import Flask
from flask_graphql import GraphQLView
## this statement acts as input for graphql query
from extraction_tutorial.schema import schema


app = Flask(__name__)
### function which hosts graphql as endpoint
app.add_url_rule('/', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))
app.run('')

## type
## resolver for each query
## object
## mutation
## return
