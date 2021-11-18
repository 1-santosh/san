"""
GraphQL schema for extracting results from a website.
"""
import graphene
import extraction
import requests

## extractor for website url
def extract(url):
    html = requests.get(url).text
    extracted = extraction.Extractor().extract(html, source_url=url)
    print(extracted)
    return extracted

## twitter response


## modifying schemas to accommodate different crawling pipelines for websites
class Websites(graphene.ObjectType):
    url = graphene.String(required=True)
    title = graphene.String()
    description = graphene.String()
    image = graphene.String()
    feed = graphene.String()
### simialr to type Website{ type Website {"url":String}
## schema creation
## we can create multiple schemas and multiple resolvers according to the ap
class Website(graphene.ObjectType):
    url = graphene.String(required=True)
    title = graphene.String()
    description = graphene.String()
    image = graphene.String()
    feed = graphene.String()


class Query(graphene.ObjectType):
    #parses the url from the input string we passed
    ## this is where field website and url is appearing
    website = graphene.Field(Website, url=graphene.String())
    websites = graphene.Field (Websites, url=graphene.String ())
    print("website",website)
     ## resolve is used for internal logic of graphql
    def resolve_website(self, url):
        extracted = extract(url)
        ## return field for graphql query
        return Website(url=url,
                       title=extracted.title,
                       description=extracted.description,
                       image=extracted.image,
                       feed=extracted.feed
        )

    def resolve_websites(self, url):
        extracted = extract(url)
        print("resolved url is",url)
        ## return field for graphql query
        ## json s3 dumps
        return Website(url=url,
                       title=extracted.title,
                       description=extracted.description,
                       image=extracted.image,
                       feed=extracted.feed
        )

schema = graphene.Schema(query=Query)
### execute schema acts as graphql query