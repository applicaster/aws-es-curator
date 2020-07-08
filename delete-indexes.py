import boto3
import os
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection
import curator

source_type    = os.environ.get("source_type","name")
direction_type = os.environ.get("direction_type","older")
delete_after   = int(os.environ.get("delete_after",30))
idx_format     = os.environ.get("index_format","%Y.%m.%d")
unit_type      = os.environ.get("unit_type","days")
host           = os.environ.get("es_endpoint") # For example, search-my-domain.region.es.amazonaws.com
if not host:
    raise Exception("[es_endpoint] OS variable is not set")

region = host.split(".")[1] # For example, us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# Build the Elasticsearch client.
es = Elasticsearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

index_list = curator.IndexList(es)

# Filters by age, anything with a time stamp older than 30 days in the index name.
index_list.filter_by_age(source=source_type, direction=direction_type, timestring=idx_format, unit=unit_type, unit_count=delete_after)

print("Found %s indices to delete" % len(index_list.indices))

# If our filtered list contains any indices, delete them.
if index_list.indices:
    curator.DeleteIndices(index_list).do_action()
