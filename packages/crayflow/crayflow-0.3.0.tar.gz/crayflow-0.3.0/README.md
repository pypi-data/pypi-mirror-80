# crayflow

```python
import crayflow as flow

data_train, labels_train, data_test, labels_test = flow.dataflow(
  flow.instances.download_mnist('MNIST/'),
  flow.instances.read_mnist() @ flow.pickled('MNIST/mnist.pickled')
)('/data/directory/')
```

