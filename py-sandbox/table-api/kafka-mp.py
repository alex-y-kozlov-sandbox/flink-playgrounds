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
#
#                 
################################################################################


from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.table import (TableEnvironment, DataTypes, EnvironmentSettings)
from pyflink.table.udf import udf

provinces = ("Beijing", "Shanghai", "Hangzhou", "Shenzhen", "Jiangxi", "Chongqing", "Xizang")

base_path='/Users/kozlova/program/repos/sandbox/flink-playgrounds/py-sandbox/table-api'
# base_path='/opt/table-api'

@udf(input_types=[DataTypes.STRING()], result_type=DataTypes.STRING())
def province_id_to_name(id):
    return provinces[id]


def log_processing():
    # 1. create a TableEnvironment
    env_settings = EnvironmentSettings.in_streaming_mode()

    #env_settings = EnvironmentSettings.new_instance()\
    #                    .in_batch_mode()\
    #                    .use_blink_planner()\
    #                    .build()

    tbl_env = TableEnvironment.create(env_settings)
    tbl_env.get_config().get_configuration().set_boolean("python.fn-execution.memory.managed", True)
    tbl_env.get_config().get_configuration().set_string("pipeline.jars", "file:///Users/kozlova/Downloads/flink-1.14.3/lib/flink-sql-connector-kafka_2.11-1.14.3.jar")
    #tbl_env.get_config().get_configuration().set_string("pipeline.jars", "file:///Users/kozlova/Downloads/flink-1.14.3/lib/flink-sql-connector-kafka_2.11-1.14.3.jar;file:///Users/kozlova/Downloads/flink-1.14.3/lib/flink-connector-kafka_2.11-1.14.3.jar")
    #tbl_env.get_config().get_configuration().set_string("pipeline.classpaths", "file:///Users/kozlova/Downloads/flink-1.14.3/lib/flink-sql-connector-kafka_2.11-1.14.3.jar;file:///Users/kozlova/Downloads/flink-1.14.3/lib/flink-connector-kafka_2.11-1.14.3.jar")

    create_kafka_source_ddl = """
            CREATE TABLE payment_msg(
                createTime VARCHAR
                ,orderId BIGINT
                ,payAmount DOUBLE
                ,payPlatform INT
                ,provinceId INT
            ) WITH (
                'connector' = 'kafka'
                ,'topic' = 'payment_msg'
                ,'properties.bootstrap.servers' = 'bootstrap.kafka.20.42.24.68.nip.io:9094'
                ,'properties.security.protocol' = 'SSL'
                ,'properties.ssl.truststore.password' = 'password'
                ,'properties.ssl.truststore.location' = '{0}/config/secrets/truststore.jks'
                ,'properties.group.id' = 'test_5'
                ,'scan.startup.mode' = 'earliest-offset'
                ,'format' = 'json'
            )
            """.format(base_path)

    create_print_sink_ddl = """
        CREATE TABLE print_sink (
            province VARCHAR
            ,pay_amount DOUBLE
        )
        -- Free text comment
        COMMENT ''
        WITH (
            'connector' = 'print' -- Must be set to 'print' to configure this connector.
        )
        """

    tbl_env.execute_sql(create_kafka_source_ddl)
    tbl_env.execute_sql(create_print_sink_ddl)
    tbl_env.register_function('province_id_to_name', province_id_to_name)

    #.select("province_id_to_name(provinceId) as province, payAmount") \
    tbl_env.from_path("payment_msg") \
        .select("'test_province' as province, payAmount") \
        .group_by("province") \
        .select("province, sum(payAmount) as pay_amount") \
        .execute_insert("print_sink")


if __name__ == '__main__':
    log_processing()

