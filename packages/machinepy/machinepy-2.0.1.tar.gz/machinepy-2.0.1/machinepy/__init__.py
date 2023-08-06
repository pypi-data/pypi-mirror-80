import numpy as _np 
import random as _rd

def _sig (val):
    y = 1/(1 + _np.exp(-(val)))
    return y

def _init_wgts_bias (inputs, outputs):
    weights_array = []
    bias_array = []
    weights = inputs * outputs
    i = 0
    while i < weights:
        weights_array.append(round(_rd.random(),2))
        i+=1
    i = 0
    while i < outputs:
        bias_array.append(round(_rd.random(),2))
        i+=1
    return([weights_array, bias_array])

def _init_wb(user_input):
    i=0
    weights_array = []
    while i < (len(user_input)-1):
        if i == 0:
            input_1 = len(user_input[0]) 
        else:
            input_1 = user_input[i] 
        output_1 = user_input[i+1]
        weights_array.append(_init_wgts_bias(input_1, output_1))
        i+=1
    return weights_array

def _forward_on (input_array, weights_array, outputs):
    arr = []
    arr2 = []
    arr2b = []
    i = 0
    while i < len(weights_array[0]):
        j = 0
        while j < outputs:
            arr.append([weights_array[0][i]])
            j+=1
            i+=1
        arr2.append(arr)
        arr = []
    i = 0
    while i < len(weights_array[1]):
        j = 0
        while j < outputs:
            arr.append([weights_array[1][i]])
            j+=1
            i+=1
        arr2b.append(arr)
        arr = []
    i = 0
    arr2 = _np.array(arr2)
    arr2b = _np.array(arr2b[0])
    while i < len(input_array):
        arr2[i] = (arr2[i] * input_array[i])
        i += 1
    arr3 = 0
    i = 0
    while i < len(input_array):
        arr3 = arr3 + arr2[i]
        i += 1
    arr4 = arr3+arr2b
    
    
    arr5 = []
    i=0
    while i < len(arr4):
        arr5.append(_sig(arr4[i][0]))
        i+=1
    return arr5

def _forwardio(user_input, weights_array):
    output_array = []
    inputs = user_input[0]
    i=1
    while i < len(user_input):
        outputs = user_input[i]
        inputs = _forward_on(inputs, weights_array[i-1],outputs)
        output_array.append(inputs)
        i+=1
    return output_array

def _error_g(inputs,weights,outputs):
    i = 0
    weight_errors = []
    while i < len(weights):
        j = 0
        while j < len(outputs):
            weight_errors.append(weights[i] * outputs[j])
            i+=1
            j+=1
    h = [0] * len(inputs)
    i = 0
    k = 0
    while i < len(weight_errors):
        j = 0
        while j < len(outputs):
            h[k] = h[k] + weight_errors[i]
            i+=1
            j+=1
        k += 1
    i = 0
    while i < len(h):
        h[i] = h[i] * inputs[i]
        i += 1
    return(h)

def _adjust_w(weights_b, weights_c):
    i = 0
    output_weights = weights_b
    while i < len(weights_b):
        j = 0
        while j < len(weights_b[i]):
            k = 0
            while k < len(weights_b[i][j]):
                output_weights[i][j][k] = weights_b[i][j][k] + weights_c[i][j][k]
                k += 1
            j += 1
        i += 1
    return(output_weights)

def _trainio (user_input, weights, target, LR):
    go = _forwardio(user_input,weights)
    output = go[len(go)-1]                  
    error = []                              
    gradients = []                          
    error_gradient = []                     
    weights_bias_change = []

    i = 0                                   
    while i < len(target):
        error.append(target[i] - output[i])
        i += 1

    i = 0                                   
    temp_eg = []
    while i < len(output):
        temp_eg.append(output[i] * (1 - output[i]) * error[i])
        i+=1
    error_gradient.append(temp_eg)

    i = 0
    while i < len(go) - 1:
        j = 0
        temp_ar = []
        while j < len(go[i]):
            temp_ar.append(go[i][j]*(1 - go[i][j]))
            j+=1
        gradients.append(temp_ar)
        i+=1
    
    inputs = go
    inputs.insert(0,user_input[0])
    inputs.pop()
    
    i = len(weights) - 1
    while i > 0:
        error_gradient.insert(0,_error_g(gradients[i-1],weights[i][0],error_gradient[0]))
        i-=1
    
    i = 0
    while i < len(inputs):
        weights_bias_change.append(_wb_change(inputs[i],error_gradient[i],LR))
        i += 1
    
    return(_adjust_w(weights, weights_bias_change))
    

def _wb_change(inputs, error_grad, lr):
    i = 0
    weight_change = []
    bias_change = []
    while i < len(inputs):
        j = 0
        while j < len(error_grad):
            weight_change.append(lr * inputs[i] * error_grad[j])
            j+=1
        i+=1
    i = 0
    while i < len(error_grad):
        bias_change.append(lr*(1)*error_grad[i])
        i+=1

    return([weight_change,bias_change])

def initnet(network_structure):
    inputs = [1] * network_structure[0]
    rest = network_structure
    rest.pop(0)
    rest.insert(0,inputs)
    output = _init_wb(rest)
    return output

def forward(inputs, weights): 
    arr = [inputs]
    i = 0
    while(i<len(weights)):
        arr.append(len(weights[i][1]))
        i+=1
    x = _forwardio(arr,weights)
    weilen = len(weights) - 1
    return x[weilen]

def train(inputs,weights,targets,learning_rate=0.1):
    arr = [inputs]
    i = 0
    while(i<len(weights)):
        arr.append(len(weights[i][1]))
        i+=1
    x = _trainio(arr,weights,targets,learning_rate)
    return x

