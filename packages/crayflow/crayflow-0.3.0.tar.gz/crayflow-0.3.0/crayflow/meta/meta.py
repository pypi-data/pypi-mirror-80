from collections import namedtuple

from craygraph import Node, NodeModel, get_incoming, dynamic_propagate
from craygraph import apply_with_kwargs

__all__ = [
  'Cache', 'NoCache',
  'ComputationalStage',
  'GenericComputationalStage',
  'dataflow', 'stage'
]

class Flow(object):
  def __call__(self, *args, root=None, **kwargs):
    raise NotImplementedError()

  def outputs(self):
    raise NotImplementedError()


class Cache(object):
  def __rmatmul__(self, other):
    return GenericCachedComputationModel(f=other, cache=self)

  def __rlshift__(self, other):
    return GenericCachedComputationModel(f=other, cache=self)

  def __rrshift__(self, other):
    return GenericCachedComputationModel(f=other, cache=self)

  def load(self, root=None):
    raise NotImplementedError()

  def save(self, obj, root=None):
    raise NotImplementedError()

class NoCache(Cache):
  def __init__(self):
    pass

  def load(self, root=None):
    raise FileNotFoundError

  def save(self, obj, root=None):
    pass

no_cache = NoCache()

class ComputationalStage(Node):
  def __init__(self, *incoming, name=None):
    super(ComputationalStage, self).__init__(*incoming, name=name)

  def load(self, root=None):
    raise FileNotFoundError()

  def get_output_for(self, *args, root=None):
    raise NotImplementedError()


def flatten(*args):
  result = list()
  for arg in args:
    if isinstance(arg, (tuple, )):
      result.extend(arg)
    else:
      result.append(arg)

  return result


class GenericComputationalStage(ComputationalStage):
  def __init__(self, f, *incoming, cache: Cache=NoCache(), name=None):
    self.f = f
    self.cache = cache

    super(GenericComputationalStage, self).__init__(*incoming, name=name)

  def load(self, root=None, **modes):
    return apply_with_kwargs(self.cache.load, root=root, **modes)

  def get_output_for(self, *inputs, root=None, **modes):
    result = apply_with_kwargs(
      self.f,
      *flatten(inputs),
      **modes
    )
    apply_with_kwargs(self.cache.save, result, root=root, **modes)
    return result

  def __matmul__(self, cache):
    return GenericComputationalStage(
      self.f, *self.incoming(), cache=cache, name=self.name
    )

class GenericCachedComputationModel(NodeModel):
  def __init__(self, f, cache: Cache=NoCache(), name=None):
    self.f = f
    self.cache = cache
    self.name = name

  def __call__(self, *incoming):
    return GenericComputationalStage(self.f, *incoming, cache=self.cache, name=self.name)

  def __matmul__(self, cache):
    return GenericCachedComputationModel(
      self.f, cache=cache, name=self.name
    )

def stage(cache=NoCache(), name=None):
  def s(f):
    return GenericCachedComputationModel(f, cache=cache, name=name)
  return s


Maybe = namedtuple('Maybe', ['value', 'success'])

class DataFlow(object):
  def __init__(self, outputs):
    self._outputs = outputs

  def outputs(self):
    if isinstance(self._outputs, (tuple, list)):
      return self._outputs
    else:
      return (self._outputs, )

  def __call__(self, root=None, warn=True, **kwargs):
    from .utils import get_data_root
    root = get_data_root(root)

    def _get_incoming(node : ComputationalStage):
      try:
        result = apply_with_kwargs(node.load, root=root, warn=warn, **kwargs)
        return tuple(), Maybe(result, True)
      except (KeyError, FileNotFoundError, NotImplementedError):
        return get_incoming(node), Maybe(None, False)

    def get_output(node : ComputationalStage, args, result : Maybe):
      if result.success:
        return result.value
      else:
        return apply_with_kwargs(node.get_output_for, *flatten(*args), root=root, warn=warn, **kwargs)

    if isinstance(self._outputs, (list, tuple)):
      result = dynamic_propagate(get_output, self._outputs, incoming=_get_incoming)
      return flatten(*(result[output] for output in self._outputs))
    else:
      result = dynamic_propagate(get_output, (self._outputs, ), incoming=_get_incoming)
      return result[self._outputs]

def dataflow(*definition):
  from .lang import achain
  return DataFlow(achain(*definition)())