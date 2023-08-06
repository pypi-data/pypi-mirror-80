from ...gradient import tf_updates

default_gradient_optimizer = tf_updates.adam(learning_rate=1e-3, beta1=0.9, beta2=0.999)

__all__ = [
  'default_gradient_optimizer'
]