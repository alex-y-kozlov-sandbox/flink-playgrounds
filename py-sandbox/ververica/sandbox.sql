CREATE TABLE payment_msg (
    createTime VARCHAR
    ,orderId BIGINT
    ,payAmount DOUBLE
    ,payPlatform INT
    ,provinceId INT
)
-- Free text comment
COMMENT ''
WITH (
  -- See https://docs.ververica.com/user_guide/sql_development/connectors.html#apache-kafka
  'connector' = 'kafka'
  ,'properties.bootstrap.servers' = 'aiops-kafka-bootstrap.kafka.svc:9092'
  ,'topic' = 'payment-msg'
  ,'properties.group.id' = 'test_4' -- Required
  ,'format' = 'json'
  ,'scan.startup.mode' = 'earliest-offset' -- Startup mode for Kafka consumer.
);

select count(*) from payment_msg;
select count(*) from payment_agg;
select * from payment_agg LIMIT 100;

select provinceId, payAmount from payment_msg;

drop table payment_agg;

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
  -- See https://docs.ververica.com/user_guide/sql_development/connectors.html#apache-kafka
  'connector' = 'kafka'
  ,'properties.bootstrap.servers' = 'aiops-kafka-bootstrap.kafka.svc:9092'
  ,'topic' = 'payment-agg'
  ,'properties.group.id' = 'test_4' -- Required
  ,'format' = 'json'
  ,'scan.startup.mode' = 'earliest-offset' -- Startup mode for Kafka consumer.
);

INSERT INTO payment_agg
SELECT 
    createTime
    ,orderId
    ,payAmount
    ,payPlatform
    ,provinceId
FROM payment_msg;