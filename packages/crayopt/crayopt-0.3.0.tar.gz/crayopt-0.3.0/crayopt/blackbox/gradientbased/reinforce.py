import tensorflow as tf

from craynn import parameters

from ...common import reducers
from ..meta import optimizer_model_from
from .meta import GradientBasedBlackBoxOptimizer
from .defaults import default_gradient_optimizer

__all__ = [
  'Reinforce', 'reinforce'
]

class Reinforce(GradientBasedBlackBoxOptimizer):
  def __init__(
    self, variables,
    mean=parameters.zeros_init(), sigma=parameters.ones_init(),
    gradient=default_gradient_optimizer,
    bias=reducers.moving_average()
  ):
    super(Reinforce, self).__init__(variables)

    self.means = list()

    for var in variables:
      mean = mean(shape=var.shape, trainable=True)
      mean.assign(var)
      self.means.append(mean)

    self.sigma = sigma(shape=tuple(), trainable=False)

    ndims = sum([tf.reduce_prod(var.shape) for var in variables])
    self.ndims = tf.constant(value=tf.cast(ndims, dtype=tf.float32))

    variables = [
      var
      for param in self.means
      for var in parameters.get_all_variables(param)
    ]
    self.gradient = gradient(variables=variables)
    self.bias = bias(tf.zeros(shape=(), dtype=tf.float32))

  def __enter__(self):
    self.gradient.__enter__()
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    self.gradient.__exit__(exc_type, exc_val, exc_tb)

  def latent(self, batch_size):
    return tuple(
      tf.random.normal(mean=0, stddev=self.sigma(), shape=(batch_size, ) + mean().shape)
      for mean in self.means
    )

  def generate(self, latent):
    return tuple(
      (mean()[None] + Z)
      for mean, Z in zip(self.means, latent)
    )

  def proposal(self, batch_size=None):
    with self.no_gradient():
      latent = self.latent(batch_size=batch_size)
      return self.generate(latent=latent)

  def log_prob(self, proposal):
    log_prob = list()

    for x, mean in zip(proposal, self.means):
      m = mean()
      axes = range(1, len(x.shape))
      lp = tf.reduce_sum((x - m[None]) ** 2, axis=axes)
      log_prob.append(lp)

    return -sum(log_prob) / self.ndims

  def __call__(self, proposal, value):
    log_prob = self.log_prob(proposal)
    bias = self.bias(tf.reduce_mean(value))
    loss = tf.reduce_mean(
      (value - bias) * log_prob
    )

    return self.gradient(loss)

  def no_gradient(self):
    return self.gradient.no_gradient()

reinforce = optimizer_model_from(Reinforce)()