python table-api.py

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

# Ververica - apache Flink commercial K8S platform
Community edition is free. 
[Community Limitations](https://www.ververica.com/pricing-editions):
- No support
- Single namespace
- No auto-scaling
- No OpenID Auth
- No API Tokens
- Local only platform state storage

## Deployment Architecture
- [docs](https://docs.ververica.com/v1.3/platform/index.html)
Is as follows:
- vvp namespace: 
  - control plane - vervetica/flink components
  - minio as an UBS/S3
- vvp-jobs: 
  - workload (Apache Flink jobs)

## Get started guide/tutorial
- [Getting Started docs](https://docs.ververica.com/getting_started/index.html)
- [Getting Started GH: Fork](https://github.com/alex-y-kozlov-sandbox/ververica-platform-playground)
- [SQL Labs](https://docs.ververica.com/getting_started/sql_development.html)

CREATE TABLE orders (
  id BIGINT,
  ordertime TIMESTAMP(3),
  totalprice DECIMAL(6,2),
  customerid BIGINT,
  WATERMARK FOR ordertime AS ordertime
) WITH (
  'connector' = 'datagen',
  'rows-per-second' = '10'
)

### Install Promi and Elk for logging
**Check out custom fluend chart: https://kokuwaio.github.io/helm-charts**

```sh
install_prometheus_operator() {
  helm_install prometheus-operator kube-prometheus-stack "$VVP_NAMESPACE" \
    --repo https://prometheus-community.github.io/helm-charts \
    --values values-prometheus-operator.yaml \
    --set prometheusOperator.namespaces.additional="{$JOBS_NAMESPACE}" \

  kubectl --namespace "$JOBS_NAMESPACE" apply -f prometheus-operator-resources/service-monitor.yaml
}
install_grafana() {S
  helm_install grafana grafana "$VVP_NAMESPACE" \
    --repo https://grafana.github.io/helm-charts \
    --values values-grafana.yaml \
    --set-file dashboards.default.flink-dashboard.json=grafana-dashboard.json
}
install_elasticsearch() {
  helm_install elasticsearch elasticsearch "$VVP_NAMESPACE" \
    --repo https://helm.elastic.co \
    --values values-elasticsearch.yaml
}
install_fluentd() {
  helm_install fluentd fluentd-elasticsearch "$VVP_NAMESPACE" \
    --repo https://kokuwaio.github.io/helm-charts \
    --values values-fluentd.yaml
}
install_kibana() {
  helm_install kibana kibana "$VVP_NAMESPACE" \
    --repo https://helm.elastic.co \
    --values values-kibana.yaml
}
```
## Deployment
1. namespace 
```
kubectl create namespace vvp; 
kubectl create namespace vvp-jobs
```
### 2. Deploy Minio
```sh
helm repo add stable https://charts.helm.sh/stable
helm repo update
helm upgrade --install minio -n vvp --repo https://helm.min.io -f https://raw.githubusercontent.com/alex-y-kozlov-sandbox/ververica-platform-playground/release-2.6/values-minio.yaml minio

```
### 3. Deploy ververica on K8S - helm chart
- [docker images docs](https://docs.ververica.com/v1.3/platform/installation/images.html)
- [helm chart docs](https://docs.ververica.com/v1.3/platform/installation/helm.html)
- [How to private registry on K8s](https:/kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#add-imagepullsecrets-to-a-service-account)

Docker registry: registry.platform.data-artisans.net
Require ` default ` StorageClass defined

```sh

# Add help chart
helm repo add ververica https://charts.ververica.com
# Get helm chart values
helm show values ververica/ververica-platform  >> ververica-helm-default-values.yaml

# Get helm output using template command:
helm template -n vvp ververica/ververica-platform --set acceptCommunityEditionLicense=true >> ververica-helm-tmpl.yaml

# Get helm output using template command:
helm template dap -n vvp ververica/ververica-platform -f ververica-helm-dap-values.yaml >> ververica-helm-dap-tmpl.yaml

# install release daplatform into ververica NS
helm upgrade --install dap -n vvp -f ververica-helm-dap-values.BROKEN.yaml ververica/ververica-platform

helm upgrade --install dap -n vvp -f vvp-values.yaml ververica/ververica-platform

helm get values vvp -n vvp >> /Users/alex.kozlovibm.com/program/repos/sandbox/flink-playgrounds/py-sandbox/ververica/vvp-values.yaml

helm delete dap -n vvp

# portforward to service/vvp-ververica-platform:80
kubectl port-forward -n vvp service/vvp-ververica-platform 8080:80
curl http://.../api/v1/namespaces/defaults/deployments -H "Accept: application/yaml"
```