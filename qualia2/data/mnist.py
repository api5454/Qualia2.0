# -*- coding: utf-8 -*- 
from .. import to_cpu
from ..core import *
from .dataset import *
from .transforms import Compose, ToTensor, Normalize
import matplotlib.pyplot as plt
import gzip

class MNIST(Dataset):
    '''MNIST Dataset\n     
    
    Args:
        train (bool): if True, load training dataset
        transforms (transforms): transforms to apply on the features
        target_transforms (transforms): transforms to apply on the labels

    Shape: 
        - data: [N, 1, 28, 28]
    '''
    def __init__(self, train=True, 
                transforms=Compose([ToTensor(), Normalize([0.5,0.5,0.5],[0.5,0.5,0.5])]), 
                target_transforms=None):
        super().__init__(train, transforms, target_transforms)
        
    def __len__(self):
        if self.train:
            return 60000
        else:
            return 10000
        
    def state_dict(self):
        return {
            'label_map': mnist_labels
        } 
       
    def prepare(self):
        url = 'http://yann.lecun.com/exdb/mnist/' 
        files = { 
            'train_data.gz':'train-images-idx3-ubyte.gz', 
            'train_labels.gz':'train-labels-idx1-ubyte.gz', 
            'test_data.gz':'t10k-images-idx3-ubyte.gz', 
            'test_labels.gz':'t10k-labels-idx1-ubyte.gz' 
        }
        for filename, value in files.items():
            self._download(url+value, filename)
        if self.train:
            data_path = self.root+'/train_data.gz'
            label_path = self.root+'/train_labels.gz'
        else:
            data_path = self.root+'/test_data.gz'
            label_path = self.root+'/test_labels.gz'
        self.data = self._load_data(data_path)
        self.label = MNIST.to_one_hot(self._load_label(label_path), 10)
    
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
                labels = np.asarray(numpy.frombuffer(file.read(), np.uint8, offset=8))
            else:
                labels = np.frombuffer(file.read(), np.uint8, offset=8) 
        return labels

    def show(self, row=10, col=10):
        H, W = 28, 28
        img = np.zeros((H*row, W*col))
        for r in range(row):
            for c in range(col):
                img[r*H:(r+1)*H, c*W:(c+1)*W] = self.data[random.randint(0, len(self.data)-1)].reshape(H,W)
        plt.imshow(to_cpu(img), cmap='gray', interpolation='nearest') 
        plt.axis('off')
        plt.show()   

mnist_labels = {
    0: '0', 
    1: '1', 
    2: '2', 
    3: '3', 
    4: '4', 
    5: '5', 
    6: '6', 
    7: '7', 
    8: '8', 
    9: '9'
}