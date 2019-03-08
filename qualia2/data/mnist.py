# -*- coding: utf-8 -*- 
from .. import to_cpu
from ..core import *
from ..config import gpu
from ..autograd import Tensor
from .dataloader import DataLoader
import matplotlib.pyplot as plt
import os
import gzip

class MNIST(DataLoader):
    '''MNIST Dataset\n     
    Args:
        normalize (bool): If true, the intensity value of a specific pixel in a specific image will be rescaled from [0, 255] to [0, 1]. Default: True 
        flatten (bool): If true, data will have a shape of [N, 28*28]. Default: False 

    Shape: 
        - data: [N, 1, 28, 28] if flatten [N, 28*28]
    '''
    def __init__(self, normalize=True, flatten=False):
        super().__init__() 
        path = os.path.dirname(os.path.abspath(__file__)) 

        print('[*] preparing data...')
        if not os.path.exists(path + '/download/mnist/'): 
            print('    this might take few minutes.') 
            os.makedirs(path + '/download/mnist/') 
            self.download(path+'/download/mnist/')
        self.train_data = self._load_data(path + '/download/mnist/train_data.gz')
        self.train_label = MNIST.to_one_hot(self._load_label(path + '/download/mnist/train_labels.gz'), 10)
        self.test_data = self._load_data(path + '/download/mnist/test_data.gz')
        self.test_label = MNIST.to_one_hot(self._load_label(path + '/download/mnist/test_labels.gz'), 10)
        print('[*] done.')

        if normalize: 
            self.train_data = np.divide(self.train_data, 255.0)
            self.test_data = np.divide(self.test_data, 255.0)
        if flatten:
            self.train_data = self.train_data.reshape(-1, 28*28) 
            self.test_data = self.test_data.reshape(-1, 28*28) 

    def download(self, path): 
        import urllib.request 
        url = 'http://yann.lecun.com/exdb/mnist/' 
        files = { 
            'train_data.gz':'train-images-idx3-ubyte.gz', 
            'train_labels.gz':'train-labels-idx1-ubyte.gz', 
            'test_data.gz':'t10k-images-idx3-ubyte.gz', 
            'test_labels.gz':'t10k-labels-idx1-ubyte.gz' 
        } 
        for key, value in files.items(): 
            if not os.path.exists(path+key): 
                urllib.request.urlretrieve(url+value, path+key) 
    
    def _load_data(self, filename):
        with gzip.open(filename, 'rb') as file: 
            if gpu:
                import numpy
                data = np.asarray(numpy.frombuffer(file.read(), np.uint8, offset=16))
            else:
                data = np.frombuffer(file.read(), np.uint8, offset=16) 
        return data.reshape(-1,1,28,28) 

    def _load_label(self, filename):
        with gzip.open(filename, 'rb') as file: 
            if gpu:
                import numpy
                labels = np.asarray(numpy.frombuffer(file.read(), np.uint8, offset=8) )
            else:
                labels = np.frombuffer(file.read(), np.uint8, offset=8) 
        return labels
        
        