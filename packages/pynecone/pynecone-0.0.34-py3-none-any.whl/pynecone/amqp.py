import pika
from .broker import Broker
from .consumer import Consumer
from .producer import Producer
from .task import Task


class AMQPConsumer(Consumer):

    def consume(self, args):
        credentials = pika.PlainCredentials(self.get_config().get_amqp_client_key(),
                                            self.get_config().get_amqp_client_secret())
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.get_config().get_amqp_host(),
                                      self.get_config().get_amqp_port(),
                                      self.get_config().get_amqp_path(),
                                      credentials))
        channel = connection.channel()
        channel.queue_declare(queue=args.topic)
        channel.basic_consume(queue=args.topic,
                              on_message_callback=self.callback(args))
        channel.start_consuming()

    @classmethod
    def callback(cls, args):
        return lambda channel, method, properties, body: Task.get_handler(args.script,
                                                                          args.method)({'channel': channel,
                                                                                        'method': method,
                                                                                        'properties': properties,
                                                                                        'body': body,
                                                                                        'args': args})


class AMQPProducer(Producer):

    def produce(self, args):
        credentials = pika.PlainCredentials(self.get_config().get_amqp_client_key(),
                                            self.get_config().get_amqp_client_secret())
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.get_config().get_amqp_host(),
                                      self.get_config().get_amqp_port(),
                                      self.get_config().get_amqp_path(),
                                      credentials))
        connection.channel().basic_publish(exchange=args.exchange,
                                           routing_key=args.topic,
                                           body=args.message)


class AMQP(Broker):

    def get_consumer(self):
        return AMQPConsumer('consumer')

    def get_producer(self):
        return AMQPProducer('producer')
