import tensorflow as tf

__all__ = [
  'rosenbrock',
  'rosenbrock_log1p'
]

def rosenbrock(x):
  if len(x.shape) == 1:
    return (1 - x[0]) ** 2 + 100 * (x[1] - x[0] ** 2) ** 2
  else:
    return (1 - x[:, 0]) ** 2 + 100 * (x[:, 1] - x[:, 0] ** 2) ** 2

def rosenbrock_log1p(x):
  if len(x.shape) == 1:
    return tf.math.log1p(
      (1 - x[0]) ** 2 + 100 * (x[1] - x[0] ** 2) ** 2
    )
  else:
    return tf.math.log1p(
      (1 - x[:, 0]) ** 2 + 100 * (x[:, 1] - x[:, 0] ** 2) ** 2
    )