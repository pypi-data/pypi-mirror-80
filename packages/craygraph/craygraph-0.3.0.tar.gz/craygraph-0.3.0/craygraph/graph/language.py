from ..meta import NodeModel

from .achain import achain as _achain
from .selector import SelectStatement, NothingStatement

__all__ = [
  'achain',
  'repeat',
  'for_each',
  'with_inputs',
  'select',
  'seek',
  'nothing'
]

class achain(NodeModel):
  def __init__(self, *definition):
    self.definition = definition

  def __call__(self, *incoming):
    return _achain(incoming, self.definition)

def repeat(n):
  def repeated(*definition):
    return achain(definition * n)

  return repeated

class for_each(NodeModel):
  def __init__(self, *definition):
    self.definition = definition

  def __call__(self, *incoming):
    return [
      _achain(node, self.definition)
      for node in incoming
    ]

nothing = NothingStatement()

select = SelectStatement(
  achain=achain,
  search_subgraph=False,
  replace=False
)

seek = SelectStatement(
  achain=achain,
  search_subgraph=True,
  replace=False
)

with_inputs = SelectStatement(
  achain=achain,
  search_subgraph=False,
  replace=True
)