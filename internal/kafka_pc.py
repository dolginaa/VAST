from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

class KafkaProducer:
    def __init__(self, bootstrap_servers: str, topic_name: str):
        self.bootstrap_servers = bootstrap_servers
        self.topic_name = topic_name
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers
        )
        await self.producer.start()

    async def send_message(self, message: str):
        if self.producer:
            await self.producer.send_and_wait(self.topic_name, message.encode())

    async def stop(self):
        if self.producer:
            await self.producer.stop()


class KafkaConsumer:
    def __init__(self, bootstrap_servers: str, topic_name: str, group_id: str):
        self.bootstrap_servers = bootstrap_servers
        self.topic_name = topic_name
        self.group_id = group_id
        self.consumer = None

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            self.topic_name,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id
        )
        await self.consumer.start()

    async def consume_messages(self):
        if self.consumer:
            async for msg in self.consumer:
                print(f"Received message: {msg.value.decode()}")
                # Обработка видео фрагмента здесь

    async def stop(self):
        if self.consumer:
            await self.consumer.stop()
