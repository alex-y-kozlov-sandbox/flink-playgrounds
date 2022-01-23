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

# Ververica - apache Flink commercial platform
Community edition is free. 
[Community Limitations](https://www.ververica.com/pricing-editions):
- No support
- Single namespace
- No auto-scaling
- No OpenID Auth
- No API Tokens
- Local only platform state storage

## Deploy ververica on K8S - helm chart
- [docker images docs](https://docs.ververica.com/v1.3/platform/installation/images.html)
- [helm chart docs]()

- [HOw to provate registry on K8s](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#add-imagepullsecrets-to-a-service-account)

Docker registry: registry.platform.data-artisans.net
Require ` default ` StorageClass defined

```sh

# Add help chart
helm repo add ververica https://charts.ververica.com
# Get helm chart values
helm show values ververica/ververica-platform  >> ververica-helm-default-values.yaml

# Get helm output using template command:
helm template -n ververica ververica/ververica-platform --set acceptCommunityEditionLicense=true >> ververica-helm-tmpl.yaml

# Get helm output using template command:
helm template dap -n ververica ververica/ververica-platform -f ververica-helm-dap-values.yaml >> ververica-helm-dap-tmpl.yaml

# install release daplatform into ververica NS
kubectl create namespace ververica
helm install dap -n ververica  -f ververica-helm-dap-values.yaml ververica/ververica-platform

# portforward to service/vvp-ververica-platform:80
kubectl port-forward -n ververica service/vvp-ververica-platform 8080:80
curl http://.../api/v1/namespaces/defaults/deployments -H "Accept: application/yaml"
```