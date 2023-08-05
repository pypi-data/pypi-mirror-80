Domination
==========

Real-time application made to monitor and dominate Humans.


## Requirements

- Python >= 3.6
- docker-compose

## Usage

    pip install domination
    
    # Start domination
    docker-compose up -d
    pip install domination
    domination worker -l info
    
    # Stop domination
    Ctrl + C
    docker-compose down
    
    # In case of Kafka broker errors occur:
    docker-compose rm && docker-compose up -d  # recreate containers
    
## Development

    # Install
    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements.txt
    make install
    
    # Build
    make test # coverage tests
    make linter # runs pylint
    make build


# Design
    
    +----------------+                +-------------+              +-------------+
    |  HumanRatings  |                |  dominate   |              |  domination |
    +----------------+                +-------------+              +-------------+
    |                | +------------> |             | +----------> |             |
    | Faust producer |                | Kafka topic |              | python faust|
    |                |                |             |              | agent       |
    +----------------+                +-------------+              +-------------+
                                                                          +
                                                                          |
          +---------------------------------------------------------------+
          |
          v
    +----------------+           +-------------------+           +-------------------+
    |  shadow        |           | shadow_stream     |           |  shadow_consumer  |
    +----------------+           +-------------------+           +-------------------+
    |                | +------>  | clickhouse table  | +------>  | clickhouse table  |
    |  Kafka topic   |           | encapsulate topic |           | materialized view |
    |                |           |                   |           |                   |
    +----------------+           +-------------------+           +-------------------+
                                                                          +
                                                                          |
          +---------------------------------------------------------------+
          |
          v
    +-------------------+
    |  shadow           |
    +-------------------+
    | clickhouse table  |
    | store rows        |
    |                   |
    +-------------------+

     

Structure of Kafka messages:
- topic `dominate`:
    `{"rating": <integer>, "unique_id": "<string>"}`


- topic `shadow`:
    `{"type": <integer>, "unique_id": "<string>", "emit_timestamp": <datetime>}`


Create clickhouse table

    docker exec -it clickhouse bin/bash -c "clickhouse-client --multiline"

    CREATE TABLE IF NOT EXISTS shadow_stream
        (
            `type` String,
            `unique_id` String,
            `emit_timestamp` DateTime
        ) ENGINE = Kafka()
          SETTINGS
            kafka_broker_list = 'localhost:9092',
            kafka_topic_list = 'shadow',
            kafka_group_name = 'shadow-group',
            kafka_format = 'JSONEachRow',
            kafka_skip_broken_messages = 1,
            kafka_num_consumers = 1;
    

    CREATE TABLE shadow as shadow_stream
    ENGINE = MergeTree()
    PARTITION BY toYYYYMM(emit_timestamp)
    ORDER BY emit_timestamp;


    CREATE MATERIALIZED VIEW shadow_consumer 
    TO shadow
    AS SELECT * FROM shadow;
    

## References
- [blog.streamthoughts.fr](https://blog.streamthoughts.fr/2020/06/creer-une-plateforme-analytique-temps-reel-avec-kafka-ksqldb-et-clickhouse/)


## TODO
 - deploy package to pypi
 - setup github actions
