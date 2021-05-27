import hazelcast
from fastapi import FastAPI
from pydantic import BaseModel
import sys
import uvicorn


class Message(BaseModel):
    id: str
    msg: str


app = FastAPI()


client = hazelcast.HazelcastClient(
    cluster_name="dev",
    cluster_members=[
        f"127.0.0.1:{sys.argv[2]}"
    ]
)

my_map = client.get_map("lab6")


@app.post("/lab", status_code=200)
def handle_message(message: Message):
    my_map.put(message.id, message.msg)
    print(message)


@app.get("/lab")
def return_messages():
    print([(uid, msg) for (uid, msg) in my_map.entry_set().result()])
    return str([(uid, msg) for (uid, msg) in my_map.entry_set().result()])


if __name__ == "__main__":
    print(sys.argv[1], sys.argv[2])
    uvicorn.run("logging_service:app", port=sys.argv[1])

