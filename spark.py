from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, floor
from pyspark.sql.types import StructType, StringType, IntegerType, TimestampType

# Initialize Spark session with Kafka dependencies
spark = SparkSession.builder \
    .appName("EmojiStreamingJob") \
    .master("local[*]") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0") \
    .getOrCreate()

# Define the schema for the incoming JSON messages
schema = StructType() \
    .add("user_id", IntegerType()) \
    .add("emoji_type", StringType()) \
    .add("timestamp", TimestampType())

# Kafka configuration
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC_INPUT = 'emoji_topic'
KAFKA_TOPIC_OUTPUT = 'aggregated_emoji_topic'

# Read emoji data from Kafka
kafka_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", KAFKA_TOPIC_INPUT) \
    .option("startingOffsets", "latest") \
    .load()

# Parse JSON data from Kafka
emoji_data = kafka_stream.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Convert timestamp to proper type for time-based operations
emoji_data = emoji_data.withColumn("timestamp", col("timestamp").cast("timestamp"))

# Define the aggregation algorithm:
# - Emojis of the same type are aggregated within a 2-second window.
# - Scale down the count: For every 25 emojis, the count is reduced to 1.
aggregated_emojis = emoji_data \
    .withWatermark("timestamp", "2 seconds") \
    .groupBy(window(col("timestamp"), "2 seconds"), col("emoji_type")) \
    .count() \
    .withColumn("scaled_count", floor(col("count") / 25).cast("integer")) \
    .filter(col("scaled_count") > 0)  # Only include emojis with at least 1 scaled count

# Format the output as JSON and send to Kafka
def write_to_kafka(df, epoch_id):
    # Convert the DataFrame rows to JSON strings
    output = df.selectExpr(
        "to_json(named_struct('emoji_type', emoji_type, 'scaled_count', scaled_count, 'window_start', window.start, 'window_end', window.end)) as value"
    )

    # Write the processed data to Kafka
    output.write \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BROKER) \
        .option("topic", KAFKA_TOPIC_OUTPUT) \
        .save()

# Write the processed stream to Kafka
query = aggregated_emojis.writeStream \
    .outputMode("update") \
    .foreachBatch(write_to_kafka) \
    .trigger(processingTime="2 seconds") \
    .start()

# Wait for the query to terminate
query.awaitTermination()
