python table-api.py

https://flink.apache.org/2021/02/10/native-k8s-with-ha.html#example-application-cluster-with-ha

https://nightlies.apache.org/flink/flink-docs-release-1.14/docs/deployment/resource-providers/standalone/kubernetes/#introduction

https://nightlies.apache.org/flink/flink-docs-release-1.14/docs/deployment/resource-providers/standalone/docker/#enabling-python

$ docker run \
    --mount type=bind,src=/host/path/to/custom/conf,target=/opt/flink/conf \
    flink:1.14.2-scala_2.11 <jobmanager|standalone-job|taskmanager>