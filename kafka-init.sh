#!/bin/bash

# Start Kafka in the background
/etc/confluent/docker/run &

# Wait for Kafka to become available
echo "Waiting for Kafka to become available..."
cub kafka-ready -b localhost:9092 1 20

# Create topics
kafka-topics --bootstrap-server localhost:9092 --create --topic transactions --partitions 1 --replication-factor 1
kafka-topics --bootstrap-server localhost:9092 --create --topic user_interactions --partitions 1 --replication-factor 1
kafka-topics --bootstrap-server localhost:9092 --create --topic inventory_updates --partitions 1 --replication-factor 1

# Keep the script running
wait

