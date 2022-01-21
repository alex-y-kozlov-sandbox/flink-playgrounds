from time import sleep
from json import dumps
from kafka import KafkaConsumer
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

consumer = KafkaConsumer( topic,
                          bootstrap_servers=[bootstrap_server],
                          security_protocol=security_protocol,
                          ssl_cafile=ssl_cafile,
                          auto_offset_reset='earliest', 
                          enable_auto_commit=False,
                          #api_version=(0, 10),
                          #ssl_context=context,
                          ssl_check_hostname=True,
                          ssl_cafile=ssl_cafile,
                          #sasl_mechanism = sasl_mechanism,
                          #sasl_plain_username = username,
                          #sasl_plain_password = password)
                          #ssl_certfile='../keys/certificate.pem',
                          #ssl_keyfile='../keys/key.pem')#,api_version = (0, 10)
)

for message in consumer:
    message = message.value
    print('{} received'.format(message))
