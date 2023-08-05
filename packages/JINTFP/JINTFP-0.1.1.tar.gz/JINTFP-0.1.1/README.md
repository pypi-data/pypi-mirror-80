# JINTFP
Just in Need, Time Functional Pipeline.

This package is designed to aid implementation of Function Pipeline design into arbitrary program.\
With simple three classes, convert your functions into Node and draw Pipeline to effectively chain those primitives. \
For more detail and tutorial, please refer to short technical report on the topic : \
https://github.com/grasshopperTrainer/JINTFP/blob/master/res/Introduction-to-JINT-Function-Pipeline.pdf

## Installation
Use `pip` to install the package.  
`pip install JINTFP`

## Usage
```python
import JINTFP as fp


class Adder(fp.NodeBody):
    in0 = fp.Input(def_val=0)
    in1 = fp.Input(def_val=0)
    out0 = fp.Output()

    def __init__(self, a, b):
        super().__init__(a, b)

    def calculate(self, a, b):
        print(f'adding {a}, {b}')
        return a + b


node0 = Adder(1, 2)
node1 = Adder(20, 50)
node1.in0 = node0.out0

print(node0.out0)
print(node1.out0)
```    

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.    
<https://github.com/grasshopperTrainer/JINTFP>    

## Alternative contact
For any questions :    
<grasshoppertrainer@gmail.com>    
    
## Licence
MIT
