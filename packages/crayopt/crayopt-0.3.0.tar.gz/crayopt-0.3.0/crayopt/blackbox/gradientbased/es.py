import numpy as np
import tensorflow as tf

from craynn import parameters

from ...common import reducers
from ..meta import optimizer_model_from
from .meta import GradientBasedBlackBoxOptimizer
from .defaults import default_gradient_optimizer

__all__ = [
  'EvolutionaryStrategies', 'es'
]

class EvolutionaryStrategies(GradientBasedBlackBoxOptimizer):
  def __init__(
    self, variables,
    mean=parameters.zeros_init(),
    log_sigma=parameters.zeros_init(),
    shared_variance=False,
    gradient=default_gradient_optimizer,
    bias=reducers.moving_average()
  ):
    super(EvolutionaryStrategies, self).__init__(variables)

    self.means = list()

    variables = [
      var if isinstance(var, (tf.Tensor, tf.Variable)) else tf.convert_to_tensor(var, dtype=tf.float32)
      for var in variables
    ]

    for var in variables:
      mean = mean(shape=var.shape, trainable=True)
      mean.assign(var)
      self.means.append(mean)

    self.shared_variance = shared_variance

    if shared_variance:
      self.log_sigmas = [
        log_sigma(shape=tuple(), trainable=True)
      ]
    else:
      self.log_sigmas = [
        log_sigma(shape=var.shape, trainable=True)
        for var in variables
      ]

    ndims = sum([tf.reduce_prod(var.shape) for var in variables])
    self.ndims = tf.constant(value=tf.cast(ndims, dtype=tf.float32))

    self.gradient = gradient([
      var
      for parameter in (self.means + self.log_sigmas)
      for var in getattr(parameter, 'variables', tuple)()
    ])

    self.bias = bias(tf.zeros(shape=(), dtype=tf.float32))

  def __enter__(self):
    self.gradient.__enter__()
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    self.gradient.__exit__(exc_type, exc_val, exc_tb)

  def latent(self, batch_size):
    return tuple(
      tf.random.normal(shape=(batch_size, ) + mean.shape(), dtype=tf.float32)
      for mean in self.means
    )

  def generate(self, latent):
    if self.shared_variance:
      log_sigma, = self.log_sigmas
      log_s = log_sigma()
      s = tf.exp(log_s)

      return tuple(
        mean()[None] + Z * s
        for mean, Z in zip(self.means, latent)
      )

    else:
      return tuple(
        mean()[None] + Z * tf.exp(log_sigma())[None]
        for mean, log_sigma, Z in zip(self.means, self.log_sigmas, latent)
      )

  def proposal(self, batch_size=None):
    with self.no_gradient():
      latent = self.latent(batch_size=batch_size)
      return self.generate(latent=latent)

  def log_prob(self, proposal):
    log_prob = list()

    if self.shared_variance:
      log_sigma, = self.log_sigmas
      log_s = log_sigma()
      s = tf.exp(log_s)

      for x, mean in zip(proposal, self.means):
        m = mean()
        axes = range(1, len(x.shape))

        lp = tf.reduce_sum(((x - m[None]) / s) ** 2, axis=axes)
        log_prob.append(lp)

      return -sum(log_prob) / self.ndims - log_s

    else:
      for x, mean, log_sigma in zip(proposal, self.means, self.log_sigmas):
        log_s = log_sigma()
        s = tf.exp(log_s)
        m = mean()
        axes = range(1, len(x.shape))

        lp = tf.reduce_sum(((x - m[None]) / s) ** 2, axis=axes) + tf.reduce_sum(log_s)
        log_prob.append(lp)

      return -sum(log_prob) / self.ndims

  def __call__(self, proposal, value):
    log_prob = self.log_prob(proposal)
    bias = self.bias(tf.reduce_mean(value))
    loss = tf.reduce_mean((value - bias) * log_prob)

    return self.gradient(loss)

  def no_gradient(self):
    return self.gradient.no_gradient()

es = optimizer_model_from(EvolutionaryStrategies)()