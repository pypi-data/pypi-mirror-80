import tensorflow as tf

from craygraph import derive

from ..common import reducers

from .meta import GradientOptimizer, optimizer_from

__all__ = [
  'sgd', 'momentum',
  'rmsprop', 'maxprop',
  'adagrad'
]

class GenericGradientOptimizer(GradientOptimizer):
  def __init__(self, variables, step, scaling, learning_rate=1e-3):
    super(GenericGradientOptimizer, self).__init__(variables)

    self.steps = tuple(
      step(variable)
      for variable in variables
    )
    self.scales = tuple(
      scaling(variable)
      for variable in variables
    )

    self.learning_rate = tf.constant(learning_rate, dtype=tf.float32)

  def apply_gradients(self, gradients):
    steps = tuple(
      step(gradient)
      for step, gradient in zip(self.steps, gradients)
    )
    scales = tuple(
      scale(gradient)
      for scale, gradient in zip(self.scales, gradients)
    )

    for var, delta, scale in zip(self.variables, steps, scales):
      if scale is None:
        var.assign_sub(self.learning_rate * delta)
      else:
        var.assign_sub(self.learning_rate * delta / scale)


SGD = derive('SGD').based_on(GenericGradientOptimizer).with_fixed(
  step=reducers.id_reducer(),
  scaling=reducers.none_reducer()
)

sgd = optimizer_from(SGD)()

class Momentum(GenericGradientOptimizer):
  def __init__(self, variables, learning_rate=1e-3, rho=0.99):
    super(Momentum, self).__init__(
      variables,
      step=reducers.momentum_average(rho),
      scaling=reducers.none_reducer(),
      learning_rate=learning_rate
    )

momentum = optimizer_from(Momentum)()

class RMSProp(GenericGradientOptimizer):
  def __init__(self, variables, learning_rate=1e-3, rho=0.99, eps=1e-7):
    super(RMSProp, self).__init__(
      variables,
      step=reducers.id_reducer(),
      scaling=reducers.momentum_l2(rho=rho, eps=eps),
      learning_rate=learning_rate,
    )

rmsprop = optimizer_from(RMSProp)()

class MaxProp(GenericGradientOptimizer):
  def __init__(self, variables, learning_rate=1e-3, rho=0.99):
    super(MaxProp, self).__init__(
      variables,
      step=reducers.id_reducer(),
      scaling=reducers.moving_linf(rho=rho),
      learning_rate=learning_rate
    )

maxprop = optimizer_from(MaxProp)()

class Adagrad(GenericGradientOptimizer):
  def __init__(self, variables, learning_rate=1e-2):
    super(Adagrad, self).__init__(
      variables,
      step=reducers.id_reducer(),
      scaling=reducers.partial_l2(),
      learning_rate=learning_rate
    )

adagrad = optimizer_from(Adagrad)()