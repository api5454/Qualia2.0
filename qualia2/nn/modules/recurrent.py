# -*- coding: utf-8 -*-
import math 
from .module import Module
from ...core import * 
from ...functions import rnncell, rnn, lstmcell, grucell, gru
from ...autograd import Tensor 

class RNN(Module):
    '''Applies a multi-layer Elman RNN with tanh
    Args:
        input_size (int): The number of expected features in the input
        hidden_size (int): The number of features in the hidden state
        num_layers (int): Number of recurrent layers.
        bias (bool):adds a learnable bias to the output. Default: True 
    Shape:
            - Input: [seq_len, N, input_size]
            - Hidden: [num_layers, N, hidden_size]
            - Output: [seq_len, N, hidden_size]
            - Hidden: [num_layers, N, hidden_size]
    '''
    def __init__(self, input_size, hidden_size, num_layers, bias=True):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_params += (input_size*hidden_size + (2*num_layers-1)*hidden_size*hidden_size)
        self.weight_x = [Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(input_size, hidden_size)))]
        self.weight_h = []
        for i in range(num_layers):
            if i == 0:
                self.weight_h.append(Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(hidden_size, hidden_size))))
            else:
                self.weight_x.append(Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(hidden_size, hidden_size))))
                self.weight_h.append(Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(hidden_size, hidden_size))))
        if bias:
            self.num_params += 2*num_layers*hidden_size
            self.bias_x = []
            self.bias_h = []
            for _ in range(num_layers):
                self.bias_x.append(Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(hidden_size))))
                self.bias_h.append(Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(hidden_size))))
        else:
            self.bias_x = None
            self.bias_h = None  
    
    def __repr__(self):
        return '{}({}, {}, {}, bias={}) at 0x{:0{}X}'.format(self.__class__.__name__, self.input_size, self.hidden_size, self.num_layers, str(self.bias_x is not None), id(self), 16)

    def forward(self, x, h0):
        result, hn = rnn(x, h0, self.weight_x, self.weight_h, self.bias_x, self.bias_h, self.num_layers)
        if self.input_shape is None:
            self.input_shape = tuple([x.shape, h0.shape])
        if self.output_shape is None:
            self.output_shape = tuple([result.shape, hn.shape])
        return result, hn

class RNNCell(Module):
    '''An Elman RNN cell with tanh\n
    Args:
        input_size (int): The number of expected features in the input
        hidden_size (int): The number of features in the hidden state
        bias (bool):adds a learnable bias to the output. Default: True 
    
    Shape:
        - Input: [N, input_size]
        - Hidden: [N, hidden_size]
        - Output: [N, hidden_size]
    '''
    def __init__(self, input_size, hidden_size, bias=True):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_params += (input_size*hidden_size + hidden_size*hidden_size)
        self.weight_x = Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(input_size, hidden_size)))
        self.weight_h = Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(hidden_size, hidden_size)))
        if bias:
            self.bias_x = Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(hidden_size)))
            self.bias_h = Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(hidden_size)))
            self.num_params += 2*hidden_size
        else:
            self.bias_x = None
            self.bias_h = None

    def __repr__(self):
        return '{}({}, {}, bias={}) at 0x{:0{}X}'.format(self.__class__.__name__, self.input_size, self.hidden_size, str(self.bias_x is not None), id(self), 16)
 
    def forward(self, x, h):
        result = rnncell(x, h, self.weight_x, self.weight_h, self.bias_x, self.bias_h)
        if self.input_shape is None:
            self.input_shape = tuple([x.shape, h.shape])
        if self.output_shape is None:
            self.output_shape = result.shape
        return result
    
class LSTM(Module):
    '''Long Short Term Memoty \n
    Args:
        input_size (int): The number of expected features in the input
        hidden_size (int): The number of features in the hidden state
        num_layers (int): Number of recurrent layers.
        bias (bool):adds a learnable bias to the output. Default: True 

    Shape:
        - Input: [seq_len, N, input_size]
        - Hidden_h: [num_layers, N, hidden_size]
        - Hidden_c: [num_layers, N, hidden_size]
        - Output: [seq_len, N, hidden_size]
        - Hidden_h: [num_layers, N, hidden_size]
        - Hidden_c: [num_layers, N, hidden_size]
    '''
    def __init__(self, input_size, hidden_size, num_layers, bias=True):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_params += (4*input_size*hidden_size + (2*num_layers-1)*4*hidden_size*hidden_size)
        self.weight_x = [Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(input_size, 4*hidden_size)))]
        self.weight_h = []
        for i in range(num_layers):
            if i == 0:
                self.weight_h.append(Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(hidden_size, 4*hidden_size))))
            else:
                self.weight_x.append(Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(hidden_size, 4*hidden_size))))
                self.weight_h.append(Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(hidden_size, 4*hidden_size))))
        if bias:
            self.num_params += 2*num_layers*4*hidden_size
            self.bias_x = []
            self.bias_h = []
            for _ in range(num_layers):
                self.bias_x.append(Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(4*hidden_size))))
                self.bias_h.append(Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(4*hidden_size))))
        else:
            self.bias_x = None
            self.bias_h = None  
    
    def __repr__(self):
        return '{}({}, {}, {}, bias={}) at 0x{:0{}X}'.format(self.__class__.__name__, self.input_size, self.hidden_size, self.num_layers, str(self.bias_x is not None), id(self), 16)

    def forward(self, x, h0, c0):
        result, hn, cn = lstm(x, h0, c0, self.weight_x, self.weight_h, self.bias_x, self.bias_h, self.num_layers)
        if self.input_shape is None:
            self.input_shape = [x.shape, h0.shape, c0.shape]
        if self.output_shape is None:
            self.output_shape = [result.shape, hn.shape, cn.shape]
        return result, hn, cn
    
class LSTMCell(Module):
    '''A Long Short Term Memoty cell \n
    Args:
        input_size (int): The number of expected features in the input
        hidden_size (int): The number of features in the hidden state
        bias (bool):adds a learnable bias to the output. Default: True 

    Shape:
        - Input: [N, input_size]
        - Hidden_h: [N, hidden_size]
        - Hidden_c: [N, hidden_size]
        - Output_h: [N, hidden_size]
        - Output_c: [N, hidden_size]
    '''
    def __init__(self, input_size, hidden_size, bias=True):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_params += (4*input_size*hidden_size + 4*hidden_size*hidden_size)
        self.weight_x = Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(input_size, 4*hidden_size)))
        self.weight_h = Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(hidden_size, 4*hidden_size)))
        if bias:
            self.bias_x = Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(4*hidden_size)))
            self.bias_h = Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(4*hidden_size)))
            self.num_params += 2*4*hidden_size
        else:
            self.bias_x = None
            self.bias_h = None
    
    def __repr__(self):
        return '{}({}, {}, bias={}) at 0x{:0{}X}'.format(self.__class__.__name__, self.input_size, self.hidden_size, str(self.bias_x is not None), id(self), 16)

    def forward(self, x, h, c):
        h_next, c_next = lstmcell(x, h, c, self.weight_x, self.weight_h, self.bias_x, self.bias_h)
        if self.input_shape is None:
            self.input_shape = [x.shape, h.shape, c.shape]
        if self.output_shape is None:
            self.output_shape = [h_next.shape, c_next.shape]
        return h_next, c_next

class GRU(Module):
    '''Applies a multi-layer gated recurrent unit (GRU) RNN to an input sequence.
    Args:
        input_size (int): The number of expected features in the input
        hidden_size (int): The number of features in the hidden state
        num_layers (int): Number of recurrent layers.
        bias (bool):adds a learnable bias to the output. Default: True 
    Shape:
            - Input: [seq_len, N, input_size]
            - Hidden: [num_layers, N, hidden_size]
            - Output: [seq_len, N, hidden_size]
            - Hidden: [num_layers, N, hidden_size]
    '''
    def __init__(self, input_size, hidden_size, num_layers, bias=True):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_params += (3*input_size*hidden_size + (2*num_layers-1)*3*hidden_size*hidden_size)
        self.weight_x = [Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(input_size, 3*hidden_size)))]
        self.weight_h = []
        for i in range(num_layers):
            if i == 0:
                self.weight_h.append(Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(hidden_size, 3*hidden_size))))
            else:
                self.weight_x.append(Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(hidden_size, 3*hidden_size))))
                self.weight_h.append(Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(hidden_size, 3*hidden_size))))
        if bias:
            self.num_params += 2*num_layers*3*hidden_size
            self.bias_x = []
            self.bias_h = []
            for _ in range(num_layers):
                self.bias_x.append(Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(3*hidden_size))))
                self.bias_h.append(Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(3*hidden_size))))
        else:
            self.bias_x = None
            self.bias_h = None  
    
    def __repr__(self):
        return '{}({}, {}, {}, bias={}) at 0x{:0{}X}'.format(self.__class__.__name__, self.input_size, self.hidden_size, self.num_layers, str(self.bias_x is not None), id(self), 16)

    def forward(self, x, h0):
        result, hn = gru(x, h0, self.weight_x, self.weight_h, self.bias_x, self.bias_h, self.num_layers)
        if self.input_shape is None:
            self.input_shape = tuple([x.shape, h0.shape])
        if self.output_shape is None:
            self.output_shape = tuple([result.shape, hn.shape])
        return result, hn    
    
class GRUCell(Module):
    '''A gated recurrent unit\n
    Args:
        input_size (int): The number of expected features in the input
        hidden_size (int): The number of features in the hidden state
        bias (bool):adds a learnable bias to the output. Default: True 
    
    Shape:
        - Input: [N, input_size]
        - Hidden: [N, hidden_size]
        - Output: [N, hidden_size]
    '''
    def __init__(self, input_size, hidden_size, bias=True):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_params += (3*input_size*hidden_size + 3*hidden_size*hidden_size)
        self.weight_x = Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(input_size, 3*hidden_size)))
        self.weight_h = Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(hidden_size, 3*hidden_size)))
        if bias:
            self.bias_x = Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(3*hidden_size)))
            self.bias_h = Tensor(np.random.uniform(-math.sqrt(1/hidden_size),math.sqrt(1/hidden_size),(3*hidden_size)))
            self.num_params += 2*3*hidden_size
        else:
            self.bias_x = None
            self.bias_h = None
    
    def __repr__(self):
        return '{}({}, {}, bias={}) at 0x{:0{}X}'.format(self.__class__.__name__, self.input_size, self.hidden_size, str(self.bias_x is not None), id(self), 16)

    def forward(self, x, h):
        result = grucell(x, h, self.weight_x, self.weight_h, self.bias_x, self.bias_h)
        if self.input_shape is None:
            self.input_shape = tuple([x.shape, h.shape])
        if self.output_shape is None:
            self.output_shape = result.shape
        return result
