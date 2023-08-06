import tensorflow as tf

__all__ = [
  'GradientOptimizer',
  'OptimizerModel',
  'optimizer_from'
]

class EmptyContext(object):
  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    pass

class GradientOptimizer(object):
  def __init__(self, variables):
    self.variables = variables
    self.tape = None
    self._context = False

  def __enter__(self):
    if self._context:
      raise RuntimeError('Re-entering optimizer context.')

    tape = tf.GradientTape(persistent=False, watch_accessed_variables=False)
    self.tape = tape.__enter__()
    self.tape.watch(self.variables)

    self._context = True

    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    if self.tape is None or not self._context:
      raise RuntimeError('Exiting non-existent context.')

    self._context = False

    self.tape.__exit__(exc_type, exc_val, exc_tb)
    self.tape = None

  def apply_gradients(self, gradients):
    raise NotImplementedError()

  def __call__(self, value):
    if self.tape is None or not self._context:
      raise RuntimeError(
        'optimizer is called outside optimizer context, please, use `with optimizer:` statement'
      )

    with self.tape.stop_recording():
      gradients = self.tape.gradient(value, self.variables)
      self.apply_gradients(gradients)

    return value

  def no_gradient(self):
    if self.tape is None or not self._context:
      return EmptyContext()
    else:
      return self.tape.stop_recording()

class OptimizerModel(object):
  pass

def optimizer_from(clazz):
  from craygraph import CarryingExpression

  return CarryingExpression(
    clazz, carried=('variables', ),
    base_constructor_class=OptimizerModel
  )