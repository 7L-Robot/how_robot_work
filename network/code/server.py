# coding=utf-8 

import pickle
from multiprocessing.connection import Client
from multiprocessing.connection import Listener
import numpy as np

class Base():
    def __init__(self, host, port):
        assert 'need to define'
        self.client = None

    def send_data(self, data_list):
        for data in data_list:
            data_type = str(type(data))
            num_type = 'None'

            if 'numpy' in data_type:
                num_type = data.dtype.name
                data = data.tobytes()
            elif 'str' in data_type:
                data = data.encode()
            else:
                data_type = 'numpy'
                data = np.array(data)
                num_type = data.dtype.name
                data = data.tobytes()

            self.client.send_bytes( data_type.encode() )
            self.client.send_bytes( num_type.encode() )
            self.client.send_bytes( data )

        self.client.send_bytes( 'over'.encode() )

    def recv_data(self):
        ret = []
        while True:
            data_type = self.client.recv_bytes()            
            if isinstance(data_type, bytes):
                data_type = data_type.decode()

            if data_type == "over":
                break
            
            # get the number type for numpy arr data
            num_type = self.client.recv_bytes()            
            if isinstance(num_type, bytes):
                num_type = num_type.decode()

            data = self.client.recv_bytes()

            if 'numpy' in data_type:
                data = np.frombuffer(data, num_type)
            elif  'str' in data_type:
                data = data
            else:
                data = data

            ret.append(data)
            
        return ret


    def send_and_recv_data(self, data_list):

        self.send_data(data_list)
        ret = self.recv_data()
        return ret


    def close(self, data):
        assert 'Need to define'


class SocketClient(Base):
    def __init__(self, host, port):
        self.client = Client((host, port))

    def close(self, data):
        self.client.send( pickle.dumps( data, protocol=2  ) )
        self.client.close()


class SocketServer(Base):
    def __init__(self, host, port):
        # host = "172.31.224.159" # 获取本地主机名
        self.server = Listener((host, port))
        
        conn = self.server.accept()
        self.client = conn

    def close(self):
        self.client.close()
        self.server.close()
        print('Server close')


# for server
'''
if __name__ == "__main__":

    server = SocketServer('0.0.0.0', 15000)

    data = server.recv_data()
    
    print(data)

    server.send_data( [np.array([1,2,3]), 'Apple', (-1,2), []] )
    server.close()

'''

# for client

if __name__ == "__main__":

    # 这里是服务器端的ip
    client = SocketClient('172.31.227.87', 15000)
    # client = SocketClient('172.27.178.26', 15000)
    data = client.send_and_recv_data(  [np.eye(3), []] )
    print(data)