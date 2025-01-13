from spyne import Application, rpc, ServiceBase, Integer, Float, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import json
import os

DATA_PATH = "data/users.json"


def load_users():
    if not os.path.exists(DATA_PATH):
        return {}
    with open(DATA_PATH, "r") as file:
        return json.load(file)

def save_users(users):
    with open(DATA_PATH, "w") as file:
        json.dump(users, file, indent=2)


class CombinedService(ServiceBase):
  
    @rpc(Integer, Integer, _returns=Integer)
    def add(ctx, x, y):
        return x + y

    @rpc(Integer, Integer, _returns=Integer)
    def subtract(ctx, x, y):
        return x - y

    @rpc(Integer, Integer, _returns=Integer)
    def multiply(ctx, x, y):
        return x * y

    @rpc(Float, Float, _returns=Float)
    def divide(ctx, x, y):
        if y == 0:
            raise ValueError("No se puede dividir por cero.")
        return x / y

   
    @rpc(Unicode, Integer, _returns=Integer)
    def add_user(ctx, name, age):
        users = load_users()
        new_id = str(len(users) + 1)
        users[new_id] = {"name": name, "age": age}
        save_users(users)
        return int(new_id)

    @rpc(Integer, _returns=Unicode)
    def get_user(ctx, user_id):
        users = load_users()
        if str(user_id) in users:
            user = users[str(user_id)]
            return f"Nombre: {user['name']}, Edad: {user['age']}"
        return "Usuario no encontrado"

    @rpc(Integer, _returns=Unicode)
    def delete_user(ctx, user_id):
        users = load_users()
        if str(user_id) in users:
            del users[str(user_id)]
            save_users(users)
            return "Usuario eliminado"
        return "Usuario no encontrado"

application = Application(
    [CombinedService],
    tns="combined.soap.example",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(),
)

if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    wsgi_app = WsgiApplication(application)
    server = make_server("127.0.0.1", 8000, wsgi_app)
    print("SOAP server running on http://127.0.0.1:8000")
    server.serve_forever()
