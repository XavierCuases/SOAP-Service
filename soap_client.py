from zeep import Client


wsdl = "http://127.0.0.1:8000/?wsdl"
client = Client(wsdl)

print("Probando operaciones matemáticas:")
print(f"5 + 3 = {client.service.add(5, 3)}")
print(f"10 - 4 = {client.service.subtract(10, 4)}")
print(f"4 * 7 = {client.service.multiply(4, 7)}")
print(f"20 / 4 = {client.service.divide(20, 4)}")

print("\nProbando gestión de usuarios:")

user_id = client.service.add_user("Carlos", 35)
print(f"Usuario agregado con ID: {user_id}")


print(client.service.get_user(user_id))

#
print(client.service.delete_user(user_id))


print(client.service.get_user(user_id))
