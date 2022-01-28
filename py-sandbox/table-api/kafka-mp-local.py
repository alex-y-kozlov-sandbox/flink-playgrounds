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
from pyflink.table import (TableEnvironment, DataTypes, StreamTableEnvironment, EnvironmentSettings)
from pyflink.table.udf import udf
import os

provinces = ("Beijing", "Shanghai", "Hangzhou", "Shenzhen", "Jiangxi", "Chongqing", "Xizang")

base_path='/Users/kozlova/program/repos/sandbox/flink-playgrounds/py-sandbox/table-api'
# base_path='/opt/table-api'

@udf(input_types=[DataTypes.STRING()], result_type=DataTypes.STRING())
def province_id_to_name(id):
    return provinces[id]


def log_processing():
    # Create streaming environment
    env = StreamExecutionEnvironment.get_execution_environment()
    settings = EnvironmentSettings.new_instance()\
                      .in_streaming_mode()\
                      .use_blink_planner()\
                      .build()
    # create table environment
    tbl_env = StreamTableEnvironment.create(stream_execution_environment=env,
                                            environment_settings=settings)
    # add kafka connector dependency
    # kafka_jar = os.path.join(base_path,'flink-sql-connector-kafka_2.12-1.14.3.jar')
    # kafka_jar = './flink-sql-connector-kafka_2.12-1.14.3.jar'
    tbl_env.get_config()\
            .get_configuration()\
            .set_boolean("python.fn-execution.memory.managed", True) #\
            # .set_string("pipeline.jars", "file://{}".format(kafka_jar))\

    create_kafka_source_ddl = """
            CREATE TABLE payment_msg(
                createTime VARCHAR
                ,orderId BIGINT
                ,payAmount DOUBLE
                ,payPlatform INT
                ,provinceId INT
            ) WITH (
                'connector' = 'kafka'
                ,'topic' = 'payment-msg'
                ,'properties.bootstrap.servers' = 'bootstrap.kafka.20.42.24.68.nip.io:443'
                ,'properties.security.protocol' = 'SSL'
                ,'properties.ssl.truststore.password' = 'password'
                ,'properties.ssl.truststore.location' = '{0}/config/secrets/truststore.jks'
                ,'properties.group.id' = 'test_1'
                ,'scan.startup.mode' = 'earliest-offset'
                ,'format' = 'json'
            )
            """.format(base_path)

    create_print_sink_ddl = """
            CREATE TABLE print_sink (
                province VARCHAR
                ,payAmount DOUBLE
            )
            -- Free text comment
            COMMENT ''
            WITH (
                'connector' = 'print' -- Must be set to 'print' to configure this connector.
            )
            """

    create_kafka_sink_ddl = """
            CREATE TABLE kafka_sink (
                provinceId INT
                ,payAmount DOUBLE
            )
            -- Free text comment
            COMMENT ''
            WITH (
                'connector' = 'kafka'
                ,'topic' = 'payment-agg'
                ,'properties.bootstrap.servers' = 'bootstrap.kafka.20.42.24.68.nip.io:443'
                ,'properties.security.protocol' = 'SSL'
                ,'properties.ssl.truststore.password' = 'password'
                ,'properties.ssl.truststore.location' = '{0}/config/secrets/truststore.jks'
                ,'format' = 'json'
            )
            """.format(base_path)

    create_payment_agg_ddl = """
            CREATE TABLE payment_agg (
                createTime VARCHAR
                ,orderId BIGINT
                ,payAmount DOUBLE
                ,payPlatform INT
                ,provinceId INT
            )
            -- Free text comment
            COMMENT ''
            WITH (
                'connector' = 'kafka'
                ,'topic' = 'payment-agg'
                ,'properties.bootstrap.servers' = 'bootstrap.kafka.20.42.24.68.nip.io:443'
                ,'properties.security.protocol' = 'SSL'
                ,'properties.ssl.truststore.password' = 'password'
                ,'properties.ssl.truststore.location' = '{0}/config/secrets/truststore.jks'
                ,'format' = 'json'
            )
            """.format(base_path)

    insert_sql = """
            INSERT INTO payment_agg
            SELECT 
                createTime
                ,orderId
                ,payAmount
                ,payPlatform
                ,provinceId
            FROM payment_msg
            """

    print( "before tbl_env.execute_sql(create_kafka_source_ddl)" )
    tbl_env.execute_sql(create_kafka_source_ddl)
    print( "before tbl_env.execute_sql(create_print_sink_ddl)" )
    tbl_env.execute_sql(create_print_sink_ddl)
    print( "before tbl_env.execute_sql(create_payment_agg_ddl)" )
    tbl_env.execute_sql(create_payment_agg_ddl)
    print( "before tbl_env.register_function" )
    tbl_env.register_function('province_id_to_name', province_id_to_name)
    #print( "before insert_sql" )
    #tbl_env.execute_sql(insert_sql)
    

    print( "start query" )
    #tbl_env.from_path("payment_msg") \
    #    .select("province_id_to_name(provinceId) as province, payAmount") \
    #    .select("'test_province' as province, payAmount") \
    #    .group_by("province") \
    #    .select("province, sum(payAmount) as pay_amount") \
    #    .execute_insert("kafka_sink")
    tbl_env.from_path("payment_msg") \
        .select("createTime, orderId, payAmount, payPlatform, provinceId") \
        .execute_insert("payment_agg")
    print( "finish query" )


if __name__ == '__main__':
    log_processing()

