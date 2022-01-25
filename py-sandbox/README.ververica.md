4. run producer and consumer on topic1 in CLI mode:
```sh
# Producer:
~/program/repos/sandbox/kafka_2.13-3.0.0/bin/kafka-console-producer.sh --broker-list bootstrap.kafka.20.42.24.68.nip.io:443 --topic topic1 --producer.config ~/program/repos/sandbox/flink-playgrounds/py-sandbox/secrets/kafka-ssl.properties
# Consumer:
~/program/repos/sandbox/kafka_2.13-3.0.0/bin/kafka-console-consumer.sh --bootstrap-server bootstrap.kafka.20.42.24.68.nip.io:443 --topic topic1 --consumer.config ~/program/repos/sandbox/flink-playgrounds/py-sandbox/secrets/kafka-ssl.properties --from-beginning
# Topics:
  # List:
~/program/repos/sandbox/kafka_2.13-3.0.0/bin/kafka-topics.sh --list --bootstrap-server bootstrap.kafka.20.42.24.68.nip.io:443 --command-config ~/program/repos/sandbox/flink-playgrounds/py-sandbox/secrets/kafka-ssl.properties
    # Describe:
~/program/repos/sandbox/kafka_2.13-3.0.0/bin/kafka-topics.sh --describe --topic topic1 --bootstrap-server bootstrap.kafka.20.42.24.68.nip.io:443 --command-config ~/program/repos/sandbox/flink-playgrounds/py-sandbox/secrets/kafka-ssl.properties
```
========
topics: 
payment_msg
topic1

## ververical sql table kafka preview:
  Asked to create a Session Cluster. Created as follows:
  - name: sql1
  - NS: vvp-jobs
  - 
```yaml
metadata:
  labels: {}
  name: sql-editor-previews
spec:
  deploymentTargetName: sql1
  flinkConfiguration:
    slot.request.timeout: 10000
    taskmanager.numberOfTaskSlots: 32
  flinkImageRegistry: registry.ververica.com/v2.6
  flinkImageRepository: flink
  flinkImageTag: 1.14.3-stream1-scala_2.12-java8
  flinkVersion: '1.14'
  logging:
    log4j2ConfigurationTemplate: null
    log4jLoggers:
      '': INFO
    loggingProfile: default
  numberOfTaskManagers: 1
  resources:
    jobmanager:
      cpu: 1
      memory: 1g
    taskmanager:
      cpu: 1
      memory: 1g
  state: RUNNING
```
log config:
```yaml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<Configuration xmlns="http://logging.apache.org/log4j/2.0/config" strict="true">
    <Appenders>
        <Appender name="StdOut" type="Console">
            <Layout pattern="%d{yyyy-MM-dd HH:mm:ss,SSS} %-5p %-60c %x - %m%n" type="PatternLayout"/>
        </Appender>
        <Appender name="RollingFile" type="RollingFile" fileName="${sys:log.file}" filePattern="${sys:log.file}.%i">
            <Layout pattern="%d{yyyy-MM-dd HH:mm:ss,SSS} %-5p %-60c %x - %m%n" type="PatternLayout"/>
            <Policies>
                <SizeBasedTriggeringPolicy size="5 MB"/>
            </Policies>
            <DefaultRolloverStrategy max="1"/>
        </Appender>
    </Appenders>
    <Loggers>
        <Logger level="INFO" name="org.apache.hadoop"/>
        <Logger level="INFO" name="org.apache.kafka"/>
        <Logger level="INFO" name="org.apache.zookeeper"/>
        <Logger level="INFO" name="akka"/>
        <Logger level="ERROR" name="org.jboss.netty.channel.DefaultChannelPipeline"/>
        <Logger level="OFF" name="org.apache.flink.runtime.rest.handler.job.JobDetailsHandler"/>
        {%- for name, level in userConfiguredLoggers -%}
        <Logger level="{{ level }}" name="{{ name }}"/>
        {%- endfor -%}
        <Root level="{{ rootLoggerLogLevel }}">
            <AppenderRef ref="StdOut"/>
            <AppenderRef ref="RollingFile"/>
        </Root>
    </Loggers>
</Configuration>
```
### Session Cluster
```yaml
apiVersion: v1
kind: SessionCluster
metadata:
  annotations:
    com.dataartisans.appmanager.controller.references: '{"state":"OPEN","references":[]}'
    com.dataartisans.appmanager.controller.sessioncluster.resources.acquired: 'true'
  createdAt: '2022-01-23T18:51:47.845773Z'
  id: 26f33b18-2b83-43da-bb77-2c80090ca03b
  labels: {}
  modifiedAt: '2022-01-23T19:23:09.587190Z'
  name: sql-editor-previews
  namespace: default
  resourceVersion: 13
spec:
  deploymentTargetName: sql1
  flinkConfiguration:
    slot.request.timeout: '10000'
    taskmanager.numberOfTaskSlots: '32'
  flinkImageRegistry: registry.ververica.com/v2.6
  flinkImageRepository: flink
  flinkImageTag: 1.14.3-stream1-scala_2.12-java8
  flinkVersion: '1.14'
  logging:
    log4j2ConfigurationTemplate: null
    log4jLoggers:
      '': INFO
    loggingProfile: default
  numberOfTaskManagers: 1
  resources:
    jobmanager:
      cpu: 1
      memory: 1g
    taskmanager:
      cpu: 1
      memory: 1g
  state: RUNNING
status:
  running:
    lastUpdateTime: '2022-01-23T19:23:09.576757Z'
    startedAt: '2022-01-23T19:23:09.563911Z'
  state: RUNNING
```
