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

from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.table import StreamTableEnvironment, DataTypes, EnvironmentSettings, BatchTableEnvironment
from pyflink.table.udf import udf


provinces = ("Beijing", "Shanghai", "Hangzhou", "Shenzhen", "Jiangxi", "Chongqing", "Xizang")


@udf(input_types=[DataTypes.STRING()], result_type=DataTypes.STRING())
def province_id_to_name(id):
    return provinces[id]


def log_processing():
    t_env = BatchTableEnvironment.create(
        environment_settings=EnvironmentSettings.new_instance()
        .in_batch_mode().use_blink_planner().build())
    t_env._j_tenv.getPlanner().getExecEnv().setParallelism(1)

    create_kafka_source_ddl = """
            CREATE TABLE payment_msg(
                createTime VARCHAR,
                orderId BIGINT,
                payAmount DOUBLE,
                payPlatform INT,
                provinceId INT
            ) WITH (
              'connector.type' = 'kafka',
              'connector.version' = 'universal',
              'topic' = 'payment_msg',
              'properties.bootstrap.servers' = 'bootstrap.kafka.20.42.24.68.nip.io:443',
              'properties.security.protocol' = 'SSL',
              'properties.ssl.truststore.location' = '/opt/pyflink-walkthrough/truststore.jks',
              'properties.ssl.truststore.password' = 'password',
              'properties.group.id' = 'test_3',
              'connector.startup-mode' = 'latest-offset',
              'format' = 'json'
            )
            """

    create_es_sink_ddl = """
            CREATE TABLE es_sink (
                province VARCHAR PRIMARY KEY,
                pay_amount DOUBLE
            ) with (
                'connector.type' = 'elasticsearch',
                'connector.version' = '7',
                'connector.hosts' = 'http://elasticsearch:9200',
                'connector.index' = 'platform_pay_amount_1',
                'connector.document-type' = 'payment',
                'update-mode' = 'upsert',
                'connector.flush-on-checkpoint' = 'true',
                'connector.key-delimiter' = '$',
                'connector.key-null-literal' = 'n/a',
                'connector.bulk-flush.max-size' = '42mb',
                'connector.bulk-flush.max-actions' = '32',
                'connector.bulk-flush.interval' = '1000',
                'connector.bulk-flush.backoff.delay' = '1000',
                'format.type' = 'json'
            )
    """

    create_file_sink_ddl = """
            CREATE TABLE file_sink (
                province STRING,
                pay_amount DOUBLE,
                `file.path` STRING NOT NULL METADATA
            ) with (
                'connector' = 'filesystem',
                'path' = '/tmp/job_out/flink_out_1.json',
                'format' = 'json'
            )
    """
    try:
        t_env.execute_sql(create_kafka_source_ddl)
        t_env.execute_sql(create_es_sink_ddl)
        t_env.execute_sql(create_file_sink_ddl)
        t_env.register_function('province_id_to_name', province_id_to_name)
        r1 = t_env.from_path("payment_msg")
        r2 = r1.select("province_id_to_name(provinceId) as province, payAmount")
        r3 = r2.group_by("province")
        r4 = r3.select("province, sum(payAmount) as pay_amount")
        r5 = r4.execute_insert("file_sink")
        #r5 = r4.execute_insert("es_sink")

        #t_env.from_path("payment_msg") \
        #    .select("province_id_to_name(provinceId) as province, payAmount") \
        #    .group_by("province") \
        #    .select("province, sum(payAmount) as pay_amount") \
        #    .execute_insert("es_sink")
    except Exception as err:
        print('Handling run-time error:', err)

        


if __name__ == '__main__':
    log_processing()

