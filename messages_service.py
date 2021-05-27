from fastapi import FastAPI
import pika
import threading


def run_in_thread(fn):
    def run(*args, **kwargs):
        t = threading.Thread(target=fn, args=args, kwargs=kwargs)
        t.start()
        return t
    return run


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    data.append(body)
    print(data)


@run_in_thread
def consume_loop(messages_list):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()
    channel.queue_declare(queue='lab6')
    for method_frame, properties, body in channel.consume('lab6'):
        print(str(body))
        messages_list.append(str(body))


data = []
consume_loop(data)
app = FastAPI()


@app.get("/lab")
def root():
    print(data)
    return str(data)
