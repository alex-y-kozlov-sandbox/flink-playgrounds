from time import sleep
from json import dumps
from kafka import KafkaProducer
import os

event_count = os.environ.get('EVENT_COUNT',10)
sleep_seconds = os.environ.get('SLEEP_SECONDS',1)
topic = os.environ.get('TOPIC',"topic1")
bootstrap_server = os.environ.get('BOOTSTRAP_SERVER',"bootstrap.kafka.20.42.24.68.nip.io:443")
security_protocol = os.environ.get('SSL',"SSL")
if "SSL" == security_protocol:
  ssl_cafile = os.environ.get('SSL_CAFILE',"/Users/kozlova/program/repos/kb-docs/kafka/artifacts/kafka-ca.crt")

#sasl_mechanism = "PLAIN"
#username = "username"
#password = "password"
#context = ssl.create_default_context()
#context.options &= ssl.OP_NO_TLSv1
#context.options &= ssl.OP_NO_TLSv1_1

producer = KafkaProducer( bootstrap_servers=[bootstrap_server],
                          security_protocol=security_protocol,
                          ssl_cafile=ssl_cafile,
                          value_serializer=lambda x: dumps(x).encode('utf-8'),
                          #api_version=(0, 10),
                          #ssl_context=context,
                          ssl_check_hostname=True,
                          #sasl_mechanism = sasl_mechanism,
                          #sasl_plain_username = username,
                          #sasl_plain_password = password)
                          #ssl_certfile='../keys/certificate.pem',
                          #ssl_keyfile='../keys/key.pem')#,api_version = (0, 10)
)

for i in range(event_count):
    data = {'number' : i}
    producer.send(topic, value=data)
    producer.flush()
    sleep(sleep_seconds)
