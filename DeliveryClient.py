import Pyro4
import time

server = Pyro4.Proxy("PYRONAME:delivery.server")

print("Digite seu nome: ")
name = input()

print("Procurando pedido!")
while server.get_len_queue() == 0:
    pass

msg = server.add_delivery(name)
print(msg)
