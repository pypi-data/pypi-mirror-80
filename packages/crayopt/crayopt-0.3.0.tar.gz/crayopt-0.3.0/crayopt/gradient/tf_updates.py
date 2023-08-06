import tensorflow as tf
from craygraph import derive

from .meta import GradientOptimizer

__all__ = [
  'SGD', 'sgd',
  'Momentum', 'momentum',
  'RMSProp', 'rmsprop',
  'Adadelta', 'adadelta',
  'Adam', 'adam',
  'Adamax', 'adamax',
  'Nadam', 'nadam',
  'AMSGrad', 'amsgrad',
  'Nesterov', 'nesterov'
]

class TensorflowOptimizerWrapper(GradientOptimizer):
  def __init__(self, variables, tf_opt, opt_kwargs=None):
    if opt_kwargs is None:
      opt_kwargs = dict()

    self.tf_optimizer = tf_opt(**opt_kwargs)
    
    super(TensorflowOptimizerWrapper, self).__init__(variables)

  def apply_gradients(self, gradients):
    self.tf_optimizer.apply_gradients(zip(gradients, self.variables))


SGD = derive('SGD').based_on(TensorflowOptimizerWrapper).with_fixed(tf_opt=tf.keras.optimizers.SGD)

def sgd(learning_rate=1e-3):
  def optimizer(variables):
    return SGD(variables, opt_kwargs=dict(learning_rate=learning_rate))

  return optimizer

Momentum = derive('Momentum').based_on(TensorflowOptimizerWrapper).with_fixed(tf_opt=tf.keras.optimizers.SGD)

def momentum(learning_rate=1.0e-3, rho=0.9):
  def optimizer(variables):
    return Momentum(variables, opt_kwargs=dict(learning_rate=learning_rate, momentum=rho))

  return optimizer


RMSProp = derive('RMSProp').based_on(TensorflowOptimizerWrapper).with_fixed(tf_opt=tf.keras.optimizers.RMSprop)

def rmsprop(learning_rate=1.0e-3, rho=0.9, eps=1e-7):
  def optimizer(variables):
    return RMSProp(variables, opt_kwargs=dict(learning_rate=learning_rate, rho=rho, epsilon=eps))
  return optimizer

Adadelta =  derive('Adadelta').based_on(TensorflowOptimizerWrapper).with_fixed(tf_opt=tf.keras.optimizers.Adadelta)

def adadelta(learning_rate=1.0, rho=0.9, eps=1e-7):
  def optimizer(variables):
    return Adadelta(variables, opt_kwargs=dict(learning_rate=learning_rate, rho=rho, epsilon=eps))
  return optimizer

Adam = derive('Adam').based_on(TensorflowOptimizerWrapper).with_fixed(tf_opt=tf.keras.optimizers.Adam)

def adam(learning_rate=1.0e-3, beta1=0.9, beta2=0.999, eps=1e-7):
  def optimizer(variables):
    return Adam(variables, opt_kwargs=dict(
      learning_rate=learning_rate, beta_1=beta1, beta_2=beta2, epsilon=eps
    ))
  return optimizer


Adamax = derive('Adamax').based_on(TensorflowOptimizerWrapper).with_fixed(tf_opt=tf.keras.optimizers.Adamax)

def adamax(learning_rate=1.0e-3, beta1=0.9, beta2=0.999, eps=1e-7):
  def optimizer(variables):
    return Adamax(variables, opt_kwargs=dict(
      learning_rate=learning_rate, beta_1=beta1, beta_2=beta2, epsilon=eps
    ))
  return optimizer


Nadam = derive('Nadam').based_on(TensorflowOptimizerWrapper).with_fixed(tf_opt=tf.keras.optimizers.Nadam)

def nadam(learning_rate=1.0e-3, beta1=0.9, beta2=0.999, eps=1e-7):
  def optimizer(variables):
    return Nadam(variables, opt_kwargs=dict(
      learning_rate=learning_rate, beta_1=beta1, beta_2=beta2, epsilon=eps
    ))
  return optimizer


AMSGrad = derive('AMSGrad').based_on(TensorflowOptimizerWrapper).with_fixed(tf_opt=tf.keras.optimizers.Adam)

def amsgrad(learning_rate=1.0e-3, beta1=0.9, beta2=0.999, eps=1e-7):
  def optimizer(variables):
    return Adam(variables, opt_kwargs=dict(
      learning_rate=learning_rate, beta_1=beta1, beta_2=beta2, amsgrad=True, epsilon=eps
    ))
  return optimizer


Nesterov = derive('Nesterov').based_on(TensorflowOptimizerWrapper).with_fixed(tf_opt=tf.keras.optimizers.SGD)

def nesterov(learning_rate=1.0e-3, rho=0.9, eps=1e-7):
  def optimizer(variables):
    return Nesterov(variables, opt_kwargs=dict(
      learning_rate=learning_rate, momentum=rho, nesterov=True, eps=eps
    ))
  return optimizer