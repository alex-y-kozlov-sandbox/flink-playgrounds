################################################################################
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

import random
import os
import time, calendar
from random import randint
from kafka import KafkaProducer
from kafka import errors 
from json import dumps
from time import sleep

event_count = os.environ.get('EVENT_COUNT',10)
sleep_seconds = os.environ.get('SLEEP_SECONDS',1)
topic = os.environ.get('TOPIC',"topic1")
bootstrap_server = os.environ.get('BOOTSTRAP_SERVER',"bootstrap.kafka.20.42.24.68.nip.io:443")
security_protocol = os.environ.get('SSL',"SSL")
if "SSL" == security_protocol:
  ssl_cafile = os.environ.get('SSL_CAFILE',"/Users/kozlova/program/repos/kb-docs/kafka/artifacts/kafka-ca.crt")


def write_data(producer):
    data_cnt = 20000
    order_id = calendar.timegm(time.gmtime())
    max_price = 100000
    topic = "payment-msg"

    for i in range(data_cnt):
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        rd = random.random()
        order_id += 1
        pay_amount = max_price * rd
        pay_platform = 0 if random.random() < 0.9 else 1
        province_id = randint(0, 6)
        cur_data = {"createTime": ts, "orderId": order_id, "payAmount": pay_amount, "payPlatform": pay_platform, "provinceId": province_id}
        producer.send(topic, value=cur_data)
        sleep(0.5)

def create_producer():
    print("Connecting to Kafka brokers")
    for i in range(0, 6):
        try:
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
            print("Connected to Kafka")
            return producer
        except errors.NoBrokersAvailable:
            print("Waiting for brokers to become available")
            sleep(10)

    raise RuntimeError("Failed to connect to brokers within 60 seconds")

if __name__ == '__main__':
    producer = create_producer()
    write_data(producer)
