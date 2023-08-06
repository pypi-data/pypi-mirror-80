import tensorflow as tf

from ..common import reducers
from .meta import GradientOptimizer

__all__ = [
  'adadelta'
]

class Adadelta(GradientOptimizer):
  def __init__(self, variables, learning_rate=1e-3, rho=0.99, eps=1e-7):
    super(Adadelta, self).__init__(variables)

    self.learning_rate = tf.constant(learning_rate, dtype=tf.float32)

    self.deltas_acc = [
      reducers.moving_average(rho=rho, initial_value=tf.ones)(variable)
      for variable in variables
    ]
    self.second_momentum = [
      reducers.moving_sqr(rho=rho, initial_value=tf.zeros)(variable)
      for variable in variables
    ]

    self.eps = tf.constant(eps, dtype=tf.float32)

  def apply_gradients(self, gradients):
    scaling = [
      momentum(gradient)
      for momentum, gradient in zip(self.second_momentum, gradients)
    ]

    deltas = [
      tf.sqrt(delta() / (scale + self.eps)) * grad
      for delta, scale, grad in zip(self.deltas_acc, scaling, gradients)
    ]

    for acc, delta in zip(self.deltas_acc, deltas):
      acc(delta)

    for var, delta in zip(self.variables, deltas):
      var.assign_sub(self.learning_rate * delta)

def adadelta(learning_rate=1e-1, rho=0.99, eps=1e-7):
  def optimizer(variables):
    return Adadelta(variables, learning_rate=learning_rate, rho=rho, eps=eps)

  return optimizer