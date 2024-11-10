from .kafka_pc import KafkaProducer

class Runner:
    def __init__(self, kafka_producer: KafkaProducer):
        self.kafka_producer = kafka_producer

    def process_video(self, video_file: str):
        """
        Обрабатывает видео, разбивая его на фрагменты и отправляя их в Kafka.
        """
        # cap = cv2.VideoCapture(video_file)
        # frame_count = 0

        # while cap.isOpened():
        #     ret, frame = cap.read()
        #     if not ret:
        #         break

        #     # Разделяем видео на фрагменты
        #     frame_count += 1
        #     frame_filename = f"frame_{frame_count}.jpg"
        #     cv2.imwrite(frame_filename, frame)

        #     # Отправляем фрагмент в Kafka
        #     asyncio.run(self.kafka_producer.send_message(frame_filename))
            
        #     # Пример: отправка имени файла кадра
        #     print(f"Sent frame {frame_filename} to Kafka")

        # cap.release()
