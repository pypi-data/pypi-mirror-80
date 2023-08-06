import tensorflow as tf

__all__ = [
  'var_like'
]

def var_like(tensor, initializer=None):
  if initializer is None:
    initializer = tf.zeros
  elif not callable(initializer):
    ### assuming number
    initializer = lambda shape, dtype: tf.fill(dims=shape, value=initializer, dtype=dtype)
  else:
    pass

  return tf.Variable(
    initial_value=initializer(shape=tensor.shape, dtype=tensor.dtype),
    trainable=False,
    validate_shape=False,
    dtype=tensor.dtype,
    shape=tf.shape(tensor)
  )