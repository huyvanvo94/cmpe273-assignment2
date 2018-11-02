servers = ['http://localhost:5000','http://localhost:5001','http://localhost:5002','http://localhost:5003']


def append(server):
    servers.append(server)

def get(idx):
    return servers[idx]