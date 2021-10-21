import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
import pika
import json


DEBUG = True
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


class message_block():
    """
        RabbitMQ Message Format
    """
    def __init__(self, action_type, file_path, check_dir):
        self.action_type = action_type
        self.file_path = file_path
        self.check_dir = check_dir

    def convert_to_json(self):
        tmp_dict = {}
        tmp_dict["type"] = self.action_type #String
        tmp_dict["path"] = self.file_path #String
        tmp_dict["is_dir"] = self.check_dir #Boolean
        return json.dumps(tmp_dict)

def file_changed_send(msg):
    channel.queue_declare(queue='file')
    channel.basic_publish(exchange='', routing_key='file', body=msg)
    if DEBUG == True:
        print("[x] Sent " + msg)


class Event(LoggingEventHandler):
    def on_modified(self, event):
        type_change = event.event_type
        file_path = event.src_path
        dir_check = event.is_directory
        t_message = message_block(type_change, file_path, dir_check)
        t_json = t_message.convert_to_json()
        file_changed_send(t_json)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else "/Users/ekstrah/Desktop/waterBox/dropspace"
    event_handler = Event()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()