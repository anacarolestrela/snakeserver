import Pyro4


server = Pyro4.Proxy("PYRONAME:delivery.server")

print("Digite seu nome: ")
name = input()

print("Digite o produto que deseja: ")
product = input()

print("Digite a quantidade desse produto: ")
quantity = input()


position, id = server.add_buyer(name, product, quantity)
print("Pedido adicionado, esperando entregador! Posição na fila: ", position)
while position != 0:
    msg, position = server.check_buyer(id)

print(msg)



