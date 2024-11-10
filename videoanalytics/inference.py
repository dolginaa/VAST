from internal.kafka_pc import KafkaConsumer

class Inference:
    def __init__(self, kafka_consumer: KafkaConsumer):
        self.kafka_consumer = kafka_consumer

    async def process(self):
        await self.kafka_consumer.start()
        await self.kafka_consumer.consume_messages()
