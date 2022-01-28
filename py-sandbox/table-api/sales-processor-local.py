import os

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings

base_path='/Users/kozlova/program/repos/sandbox/flink-playgrounds/py-sandbox/table-api'
# base_path='/opt/table-api'

def main():
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
    kafka_jar = os.path.join(base_path,
                            'flink-sql-connector-kafka_2.12-1.14.3.jar')

    tbl_env.get_config()\
            .get_configuration()\
            .set_string("pipeline.jars", "file://{}".format(kafka_jar))

    #######################################################################
    # Create Kafka Source Table with DDL
    #######################################################################
    src_ddl = """
        CREATE TABLE sales_usd (
            seller_id VARCHAR,
            amount_usd DOUBLE,
            sale_ts BIGINT,
            proctime AS PROCTIME()
        ) WITH (
            'connector' = 'kafka'
            ,'topic' = 'sales-usd'
            ,'properties.bootstrap.servers' = 'bootstrap.kafka.20.42.24.68.nip.io:443'
            ,'properties.security.protocol' = 'SSL'
            ,'properties.ssl.truststore.password' = 'password'
            ,'properties.ssl.truststore.location' = '{0}/config/secrets/truststore.jks'
            ,'properties.group.id' = 'test_1'
            ,'scan.startup.mode' = 'earliest-offset'
            ,'format' = 'json'
        )
    """.format(base_path)

    tbl_env.execute_sql(src_ddl)

    # create and initiate loading of source Table
    tbl = tbl_env.from_path('sales_usd')

    print('\nSource Schema')
    tbl.print_schema()

    #####################################################################
    # Define Tumbling Window Aggregate Calculation (Seller Sales Per Minute)
    #####################################################################
    sql = """
        SELECT
          seller_id,
          TUMBLE_END(proctime, INTERVAL '60' SECONDS) AS window_end,
          SUM(amount_usd) * 0.85 AS window_sales
        FROM sales_usd
        GROUP BY
          TUMBLE(proctime, INTERVAL '60' SECONDS),
          seller_id
    """
    revenue_tbl = tbl_env.sql_query(sql)

    print('\nProcess Sink Schema')
    revenue_tbl.print_schema()

    ###############################################################
    # Create Kafka Sink Table
    ###############################################################
    print('\nBefore tbl_env.execute_sql(sink_ddl)')    
    sink_ddl = """
        CREATE TABLE sales_euros (
            seller_id VARCHAR,
            window_end TIMESTAMP(3),
            window_sales DOUBLE
        ) WITH (
            'connector' = 'kafka'
            ,'topic' = 'sales-euros'
            ,'properties.bootstrap.servers' = 'bootstrap.kafka.20.42.24.68.nip.io:443'
            ,'properties.security.protocol' = 'SSL'
            ,'properties.ssl.truststore.password' = 'password'
            ,'properties.ssl.truststore.location' = '{0}/config/secrets/truststore.jks'
            ,'format' = 'json'
        )
    """.format(base_path)
    tbl_env.execute_sql(sink_ddl)

    # write time windowed aggregations to sink table
    print( "before revenue_tbl.execute_insert('sales_euros').wait()" )
    revenue_tbl.execute_insert('sales_euros').wait()
    #print( "before revenue_tbl.execute_insert('sales_euros')" )
    #revenue_tbl.execute_insert('sales_euros')
    print( "tbl_env.execute('windowed-sales-euros')" )
    tbl_env.execute('windowed-sales-euros')


if __name__ == '__main__':
    main()