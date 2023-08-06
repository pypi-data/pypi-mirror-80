from ..meta import BlackBoxOptimizer

__all__ = [
  'GradientBasedBlackBoxOptimizer'
]

class GradientBasedBlackBoxOptimizer(BlackBoxOptimizer):
  def __init__(self, variables):
    super(GradientBasedBlackBoxOptimizer, self).__init__(variables=variables)

  def __enter__(self):
    raise NotImplementedError()

  def __exit__(self, exc_type, exc_val, exc_tb):
    raise NotImplementedError()

  def latent(self, batch_size):
    raise NotImplementedError()

  def generate(self, latent):
    raise NotImplementedError()

  def proposal(self, batch_size):
    return self.generate(self.latent(batch_size))

  def __call__(self, proposal, value):
    raise NotImplementedError()