# BEGIN_COPYRIGHT
# END_COPYRIGHT
import pydoop.pipes as pp


class Reducer(pp.Reducer):
  
  def __init__(self, ctx):
    super(reducer, self).__init__(ctx)

  def reduce(self, ctx):
    pass
