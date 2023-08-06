## pytorch模型加载与模型复杂度计算


### load pretrain
load_pretrained_weights会自动去除modules,自动过滤不匹配的层

```python
from checkpoint.checkpoint_tools import load_pretrained_weights
from torchvision.models import resnet50


model = resnet50(num_classes=2)
pretrain_path = "/home/xxxx/.torch/models/resnet50-19c8e357.pth"
load_pretrained_weights(model, pretrain_path, verbose=True)

"""
Successfully loaded pretrained weights from 
"/home/xxxx/.torch/models/resnet50-19c8e357.pth"
********************************************************************************
The following layers are discarded due to unmatched keys or layer size
['fc.weight', 'fc.bias', 'bn1.num_batches_tracked',
 'layer1.0.bn1.num_batches_tracked', 
 'layer1.0.bn2.num_batches_tracked',
 'layer1.0.bn3.num_batches_tracked',
 'layer1.0.downsample.1.num_batches_tracked',
 'layer1.1.bn1.num_batches_tracked',
 'layer1.1.bn2.num_batches_tracked',
 'layer1.1.bn3.num_batches_tracked',
 'layer1.2.bn1.num_batches_tracked',
...
********************************************************************************
The following layers are success
['conv1.weight', 'bn1.running_mean',
 'bn1.running_var', 'bn1.weight', 'bn1.bias',
 'layer1.0.conv1.weight', 'layer1.0.bn1.running_mean',
 'layer1.0.bn1.running_var', 'layer1.0.bn1.weight',
 'layer1.0.bn1.bias', 'layer1.0.conv2.weight',
 'layer1.0.bn2.running_mean', 'layer1.0.bn2.running_var',
 'layer1.0.bn2.weight', 'layer1.0.bn2.bias',
 'layer1.0.conv3.weight', 'layer1.0.bn3.running_mean',
...
"""


```


### compute model complexity
compute_model_complexity计算模型的FLOPs和参数数量


```python

from checkpoint.checkpoint_tools import compute_model_complexity
from torchvision.models import resnet50


flops, params = compute_model_complexity(resnet50(num_classes=2), (1, 3, 224, 224), verbose=True)
print(f"resnet50 flops:{flops / 1e9:.2f} GFLOPs")
print(f"resnet50 params:{params / 1e6:.2f} M")

"""
  -------------------------------------------------------
  Model complexity with input size (1, 3, 224, 224)
  -------------------------------------------------------
  Conv2d (params=23,454,912, flops=4,087,136,256)
  BatchNorm2d (params=53,120, flops=44,455,936)
  ReLU (params=0, flops=9,608,704)
  MaxPool2d (params=0, flops=1,605,632)
  AdaptiveAvgPool2d (params=0, flops=100,352)
  Linear (params=4,098, flops=4,098)
  -------------------------------------------------------
  Total (params=23,512,130, flops=4,142,910,978)
  -------------------------------------------------------
resnet50 flops:4.14 GFLOPs
resnet50 params:23.51 M
"""
```
