# aws-es-curator
# AWS Docker Elasticsearch Index Cleanup
This docker base on AWS guidelines: https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/curator.html

## Overview

This method does not work well with kube2iam
So I use AWS_user credentials

## Getting Started
* create aws-user using  "es_policy.json"
* create cronjob using this container that run once a day  (0 1 * * *)

### Cronjob configuration environment varible parameters

Using AWS environment variable you can easily modify the behaviour of the Cronjob

| Variable Name | Example Value | Description | Default Value | Required |
| --- | --- | --- | --- |  --- |
| es_endpoint | search-es-demo-zveqnhnhjqm5flntemgmx5iuya.eu-west-1.es.amazonaws.com  | AWS ES fqdn | `None` | True |
| index_format  | `%Y.%m.%d` | Combined with `index` varible is used to evaluate the index age | `%Y.%m.%d` |  False |
| delete_after | `7` | Numbers of days to preserve | `15` |  False |
