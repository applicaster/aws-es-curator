import boto3
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection
import curator

host = 'search-audience-us1-t47naux7n5bvu3wkapaiz3nzdu.us-east-1.es.amazonaws.com' # For example, search-my-domain.region.es.amazonaws.com
region = 'us-east-1' # For example, us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# Lambda execution starts here.
# def lambda_handler(event, context):

    # Build the Elasticsearch client.
es = Elasticsearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

# A test document.
document = {
    "title": "Moneyball",
    "director": "Bennett Miller",
    "year": "2011"
}

# Index the test document so that we have an index that matches the timestring pattern.
# You can delete this line and the test document if you already created some test indices.
es.index(index="movies-2017.01.31", doc_type="movie", id="1", body=document)

index_list = curator.IndexList(es)

# Filters by age, anything with a time stamp older than 30 days in the index name.
index_list.filter_by_age(source='name', direction='older', timestring='%Y.%m.%d', unit='days', unit_count=30)

# Filters by naming prefix.
# index_list.filter_by_regex(kind='prefix', value='my-logs-2017')

# Filters by age, anything created more than one month ago.
# index_list.filter_by_age(source='creation_date', direction='older', unit='months', unit_count=1)

print("Found %s indices to delete" % len(index_list.indices))

# If our filtered list contains any indices, delete them.
if index_list.indices:
    curator.DeleteIndices(index_list).do_action()
