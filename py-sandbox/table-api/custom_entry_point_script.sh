# enable an optional library
ln -fs /opt/flink/opt/flink-queryable-state-runtime-*.jar /opt/flink/lib/
# enable a custom library
ln -fs /mnt/custom_lib.jar /opt/flink/lib/

mkdir -p /opt/flink/plugins/flink-s3-fs-hadoop
# enable an optional plugin
ln -fs /opt/flink/opt/flink-s3-fs-hadoop-*.jar /opt/flink/plugins/flink-s3-fs-hadoop/  

mkdir -p /opt/flink/plugins/custom_plugin
# enable a custom plugin
ln -fs /mnt/custom_plugin.jar /opt/flink/plugins/custom_plugin/

/docker-entrypoint.sh <jobmanager|standalone-job|taskmanager>