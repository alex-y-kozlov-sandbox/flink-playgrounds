

org.apache.flink.table.api.ValidationException: Querying an unbounded table '' in batch mode is not allowed. The table source is unbounded.

## How to build pyflink container
- [docs](https://nightlies.apache.org/flink/flink-docs-release-1.14/docs/deployment/resource-providers/standalone/docker/#enabling-python)

## How to run flink in K8s

### Simples - single image, Application mode, HA
- [docs](https://flink.apache.org/2021/02/10/native-k8s-with-ha.html#example-application-cluster-with-ha)

### Cluster in session mode
- [docs](https://nightlies.apache.org/flink/flink-docs-release-1.14/docs/deployment/resource-providers/standalone/kubernetes/#introduction)

### How to flink on docker
```sh
docker run --mount type=bind,src=/host/path/to/custom/conf,target=/opt/flink/conf flink:1.14.3-scala_2.11 <jobmanager|standalone-job|taskmanager>
```
