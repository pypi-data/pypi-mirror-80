import tensorflow as tf

from craygraph import derive, CarryingExpression

from ..utils import var_like

__all__ = [
  'id_reducer', 'none_reducer', 'const_reducer',
  'moving_average', 'momentum_average', 'partial_sum',
  'moving_l1', 'momentum_l1', 'partial_l1',
  'moving_l2', 'momentum_l2', 'partial_l2',
  'moving_sqr', 'momentum_sqr', 'partial_sqr',
  'moving_linf'
]

class ReducerModel(object):
  pass

class Reducer(object):
  def __call__(self, value=None):
    raise NotImplementedError()

  def update(self, value):
    raise NotImplementedError()

  def reset(self):
    raise NotImplementedError()


def reducer_from(clazz):
  return CarryingExpression(clazz, carried=('variable', ), base_constructor_class=ReducerModel)

class IDReducer(Reducer):
  """
  State-free reducer - returns the input.
  Functionally equivalent to `lambda : lambda variable: lambda value: value`.
  """
  def __init__(self, variable):
    pass

  def __call__(self, value=None):
    return value

  def update(self, value):
    pass

  def reset(self):
    pass

id_reducer = reducer_from(IDReducer)()

class NoneReducer(Reducer):
  """
  A reducer version of None.
  Functionally equivalent to `lambda : lambda variable: lambda value: None`.
  """
  def __init__(self, variable):
    pass

  def __call__(self, value=None):
    return None

  def update(self, value):
    pass

  def reset(self):
    pass

none_reducer = reducer_from(NoneReducer)()


class ConstReducer(Reducer):
  """
  When you don't feel like reducing...
  """
  def __init__(self, variable, const=0):
    self.const = const

  def __call__(self, value=None):
    return self.const

  def update(self, value):
    pass

  def reset(self):
    pass

const_reducer = reducer_from(ConstReducer)()


class Accumulator(Reducer):
  def __init__(self, variable, f, observe, initial_value=None, eps=None):
    if initial_value is None:
      initializer = tf.zeros
    elif not callable(initial_value):
      ### assuming number
      initializer = lambda shape, dtype: tf.fill(dims=shape, value=initial_value, dtype=dtype)
    else:
      initializer = initial_value

    self.acc = var_like(variable, initializer=initializer)
    self.dtype = variable.dtype

    self.initializer = initializer

    self.eps = None if eps is None else tf.constant(eps, dtype=self.dtype)

    self.f = f
    self.observe = (lambda x: x) if observe is None else observe

  @tf.function(autograph=False)
  def __call__(self, value=None):
    if value is not None:
      v = self.f(value)
      self.update(v)

    if self.eps is None:
      return self.observe(self.acc)
    else:
      return self.observe(self.acc + self.eps)

  def update(self, value):
    raise NotImplementedError()

  def reset(self):
    self.acc.assign(
      self.initializer(shape=self.acc.shape, dtype=self.acc.dtype)
    )


class SumAccumulator(Accumulator):
  def update(self, value):
    self.acc.assign_add(value)

class Momentum(Accumulator):
  def __init__(self, variable, f, observe=None, rho=0.99, initial_value=None, eps=None):
    super(Momentum, self).__init__(variable, f, observe, initial_value=initial_value, eps=eps)

    self.rho = tf.constant(rho, dtype=self.dtype, shape=())
    self.crho = tf.constant(1 - rho, dtype=self.dtype, shape=())

  def update(self, value):
    self.acc.assign(
      self.rho * self.acc + value
    )

class Moving(Accumulator):
  def __init__(self, variable, f, observe=None, rho=0.99, initial_value=None, eps=None):
    super(Moving, self).__init__(variable, f, observe, initial_value=initial_value, eps=eps)

    self.rho = tf.constant(rho, dtype=self.dtype, shape=())
    self.crho = tf.constant(1 - rho, dtype=self.dtype, shape=())

  def update(self, value):
    self.acc.assign(
      self.rho * self.acc + self.crho * value
    )

### non-norm accumulators

PartialSum = derive('PartialSum').based_on(SumAccumulator).with_fixed(f=lambda x: x, observe=None)
MomentumAverage = derive('MomentumAverage').based_on(Momentum).with_fixed(f=lambda x: x, observe=None)
MovingAverage = derive('MovingAverage').based_on(Moving).with_fixed(f=lambda x: x, observe=None)

partial_sum = reducer_from(PartialSum)()
momentum_average = reducer_from(MomentumAverage)()
moving_average = reducer_from(MovingAverage)()

PartialL1 = derive('PartialL1').based_on(SumAccumulator).with_fixed(f=tf.abs, observe=None)
MomentumL1 = derive('MomentumL1').based_on(Momentum).with_fixed(f=tf.abs, observe=None)
MovingL1 = derive('MovingL1').based_on(Moving).with_fixed(f=tf.abs, observe=None)

partial_l1 = reducer_from(PartialL1)()
momentum_l1 = reducer_from(MomentumL1)()
moving_l1 = reducer_from(MovingL1)()

PartialL2 = derive('PartialL2').based_on(SumAccumulator).with_fixed(f=tf.square, observe=tf.sqrt)
MomentumL2 = derive('MomentumL2').based_on(Momentum).with_fixed(f=tf.square, observe=tf.sqrt)
MovingL2 = derive('MovingL2').based_on(Moving).with_fixed(f=tf.square, observe=tf.sqrt)

partial_l2 = reducer_from(PartialL2)()
momentum_l2 = reducer_from(MomentumL2)()
moving_l2 = reducer_from(MovingL2)()

PartialSqr = derive('PartialSqr').based_on(SumAccumulator).with_fixed(f=tf.square, observe=None)
MomentumSqr = derive('MomentumSqr').based_on(Momentum).with_fixed(f=tf.square, observe=None)
MovingSqr = derive('MovingSqr').based_on(Moving).with_fixed(f=tf.square, observe=None)

partial_sqr = reducer_from(PartialSqr)()
momentum_sqr = reducer_from(MomentumSqr)()
moving_sqr = reducer_from(MovingSqr)()

class MovingLinf(Accumulator):
  def __init__(self, variable, rho=0.99, initial_value=None, eps=None):
    super(MovingLinf, self).__init__(variable, f=tf.abs, observe=None, initial_value=initial_value, eps=eps)

    self.rho = tf.constant(rho, dtype=self.dtype, shape=())

  def update(self, value):
    self.acc.assign(
      tf.maximum(self.rho * self.acc, value)
    )

moving_linf = reducer_from(MovingLinf)()

