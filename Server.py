import Pyro4

class BuyerClient:
    def __init__(self, id, name, product, quantity):
        self.id = id
        self.name = name
        self.product = product
        self.quantity = quantity
        self.delivery = ''
        self.position = 0

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Server:
    def __init__(self):
        self.id = 1
        self.buyer_queue = []

    def add_buyer(self, name, product, quantity):
        buyer = BuyerClient(self.id, name, product, quantity)
        self.buyer_queue.append(buyer)
        buyer.position = len(self.buyer_queue)
        self.id += 1
        return len(self.buyer_queue), buyer.position
    
    def get_len_queue(self):
        return len(self.buyer_queue)
    
    def add_delivery(self, name):
        if(self.buyer_queue):
            buyer = self.buyer_queue[0]
            string = "Pedido econtrado! Entrega de " + str(buyer.quantity) + " " + buyer.product + " para " + buyer.name + "!"
            buyer.delivery = name
            buyer.position = 0
            return string
    
    def check_buyer(self, id):
        msg = ''
        for buyer in self.buyer_queue:
            if buyer.id == id:
                if(buyer.position == 0):
                    self.buyer_queue.pop(0)
                    msg = "Entregador encontrado! Espere por " + buyer.delivery
                return msg, buyer.position


    
if __name__=="__main__":
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(Server)
    ns.register("delivery.server", uri)

    print("Servidor pronto.")
    daemon.requestLoop()

