__all__ = [
  'BlackBoxOptimizer',
  'BlackBoxOptimizerModel',
  'optimizer_model_from'
]

class BlackBoxOptimizer(object):
  def __init__(self, variables):
    self.variables = variables
    
    super(BlackBoxOptimizer, self).__init__()

  def __enter__(self):
    raise NotImplementedError()

  def __exit__(self, exc_type, exc_val, exc_tb):
    raise NotImplementedError()

  def proposal(self, batch_size):
    raise NotImplementedError()

  def __call__(self, proposal, value):
    raise NotImplementedError()

class BlackBoxOptimizerModel(object):
  pass

def optimizer_model_from(clazz):
  from craygraph import CarryingExpression

  return CarryingExpression(
    clazz, carried=('variables',),
    base_constructor_class=BlackBoxOptimizerModel
  )