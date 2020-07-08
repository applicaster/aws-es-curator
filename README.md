# aws-es-curator
# AWS Docker Elasticsearch Index Cleanup

## Overview
This Docker allows you to delete the old Elasticsearch indexes using SigV4Auth authentication.
This Docker need to be configure as a cornjob, once a day,
This docker need to get permissions, assume role by the node worker (trust_policy.json),
and access to the AWS-ES (es_policy.json)
The docker configuration role  can be set by using "kube2iam" or other

## Prequirement
* using kubernetes with installed "kube2iam"
## Getting Started
* create aws-role using "trust_policy.json" and "es_policy.json"
* create cronjob using this container that run once a day  (0 1 * * *)
* using "kube2iam" annotations (iam.amazonaws.com/role) to attach role to the cronjob

### Cronjob configuration environment varible parameters

Using AWS environment variable you can easily modify the behaviour of the Cronjob

| Variable Name | Example Value | Description | Default Value | Required |
| --- | --- | --- | --- |  --- |
| es_endpoint | search-es-demo-zveqnhnhjqm5flntemgmx5iuya.eu-west-1.es.amazonaws.com  | AWS ES fqdn | `None` | True |
| index |  `logstash*` | Index/indices to process comma separated, with `all` every indlaex will be processed except the one listed in `skip_index` | `.*` | False |
| skip_index |  `.kibana,.kibana_5` | Index/indices to skip  | `.kibana*` | False |
| index_format  | `%Y.%m.%d` | Combined with `index` varible is used to evaluate the index age | `%Y.%m.%d` |  False |
| delete_after | `7` | Numbers of days to preserve | `15` |  False |
