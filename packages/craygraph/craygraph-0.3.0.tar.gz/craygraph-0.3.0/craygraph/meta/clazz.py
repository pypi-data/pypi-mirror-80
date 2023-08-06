from inspect import signature, Signature, Parameter
from .meta import NodeModel

__all__ = [
  'derive', 'model_from',

  'carry', 'bind',
  'CarryingExpression',
]

def get_var_arguments(sign : Signature):
  var_arguments = [
    name for name, param in sign.parameters.items()
    if param.kind == Parameter.VAR_POSITIONAL
  ]

  if len(var_arguments) == 0:
    return None
  else:
    return var_arguments[0]

def bind(sign : Signature, kwargs):
  positionals = list()
  keywords = dict()

  positional = True

  for k, p in sign.parameters.items():
    if k not in kwargs:
      positional = False
      continue

    v = kwargs.pop(k)

    if positional and (p.kind == Parameter.POSITIONAL_ONLY or p.kind == Parameter.POSITIONAL_OR_KEYWORD):
      positionals.append(v)

    elif p.kind == Parameter.VAR_POSITIONAL:
      positionals.extend(v)

    elif p.kind == Parameter.VAR_KEYWORD:
      keywords.update(v)
      positional = False

    else:
      keywords[k] = v
      positional = False

  for k, v in kwargs.items():
    keywords[k] = v

  return positionals, keywords

class From(object):
  def __init__(self, what, base_class):
    self.what = what
    self.base_class = base_class
    self._defaults = dict()

  def with_defaults(self, **kwargs):
    self._defaults.update(kwargs)

  def with_fixed(self, **kwargs):
    return _derive_from(self.what, self.base_class, kwargs, self._defaults)

class Deriver(object):
  def __init__(self, what):
    self.what = what

  def based_on(self, base_class):
    return From(self.what, base_class)

derive = Deriver

def _derive_from(name, base_class, fixed, defaults):
  common = set(fixed.keys()) & set(defaults.keys())
  if len(common) > 0:
    raise ValueError('can not fix value and set default value of the same parameter [%s]' % (', '.join(common)))

  original_signature = signature(base_class.__init__)
  new_parameters = list()
  for pname, param in original_signature.parameters.items():
    if pname in fixed:
      continue

    if pname in defaults:
      param = param.replace(default=defaults[pname])

    new_parameters.append(param)

  new_signature = Signature(
    new_parameters,
    return_annotation=original_signature.return_annotation
  )

  def new_init(self, *args, **kwargs):
    arguments = new_signature.bind(self, *args, **kwargs)
    arguments.apply_defaults()

    updated_kwargs = arguments.arguments.copy()
    updated_kwargs.update(fixed)

    args, kwargs = bind(original_signature, updated_kwargs)

    base_class.__init__(*args, **kwargs)


  new_init.__signature__ = new_signature

  return type(name, (base_class, ), {
    '__init__' : new_init
  })

def promote_parameters(parameters):
  """
  Promotes keyword-only arguments to keyword-or-positional arguments if possible.
  """
  var_positional = False
  normalized_parameters = list()

  for p in parameters:
    if var_positional:
      normalized_parameters.append(p)

    elif p.kind == Parameter.VAR_POSITIONAL or p.kind == Parameter.VAR_KEYWORD:
      var_positional = True
      normalized_parameters.append(p)

    elif p.kind == Parameter.KEYWORD_ONLY:
      normalized_parameters.append(
        p.replace(kind=Parameter.POSITIONAL_OR_KEYWORD)
      )

    else:
      normalized_parameters.append(p)

  return normalized_parameters

def carry(
  original,
  fixed, defaults,
  carried, duplicated=(),
  base_constructor_class=NodeModel,
  inject_model=None
):
  original_signature = signature(original)

  assert all(c in carried for c in duplicated), \
    'duplicated arguments must be a subset of carried arguments'

  assert all(c in original_signature.parameters for c in carried), \
    'Carrying parameter must be present in the original signature'

  assert inject_model is None or inject_model in original_signature.parameters, \
    'There is no arguments for model injection!'

  assert all(c not in fixed for c in carried), \
    'Cannot fix carried parameters'

  kw_defaults = dict()
  arg_defaults = dict()

  for k, v in defaults.items():
    if k in original_signature.parameters:
      arg_defaults[k] = v
    else:
      kw_defaults[k] = v

  kw_parameters = tuple(
    p
    for p in original_signature.parameters
    if original_signature.parameters[p].kind == Parameter.VAR_KEYWORD
  )

  assert len(kw_defaults) == 0 or len(kw_parameters) > 0, 'some default values are not present in the signature'

  kw_parameter = None if len(kw_parameters) == 0 else kw_parameters[0]

  constructor_parameters = list()

  for p in original_signature.parameters:
    param = original_signature.parameters[p]

    if p in carried and p not in duplicated:
      continue

    elif p in fixed:
      continue

    elif p == inject_model:
      continue

    elif param.kind == Parameter.VAR_KEYWORD:
      ### putting kw defaults before the **kwargs argument
      for k, v in kw_defaults.items():
        constructor_parameters.append(
          Parameter(k, kind=Parameter.KEYWORD_ONLY, default=v)
        )

      constructor_parameters.append(param)

    else:
      constructor_parameters.append(
        param.replace(default=defaults[p]) if p in defaults else param
      )

  constructor_parameters = promote_parameters(constructor_parameters)

  if original_signature.return_annotation == Parameter.empty:
    constructor_return_annotation = Parameter.empty
  else:
    constructor_return_annotation = '(%s) -> %s' % (
      ', '.join(carried),
      original_signature.return_annotation
    )

  actual_constructor_signature = Signature(
    parameters=constructor_parameters
  )
  apparent_constructor_signature = Signature(
    parameters=[Parameter('self', Parameter.POSITIONAL_ONLY)] + constructor_parameters,
    return_annotation=constructor_return_annotation
  )

  model_parameters = list()
  for p in original_signature.parameters:
    if p in carried:
      param = original_signature.parameters[p]
      model_parameters.append(
        param.replace(default=defaults[p]) if p in defaults else param
      )

  model_parameters = promote_parameters(model_parameters)

  actual_model_signature = Signature(
    parameters=model_parameters
  )
  apparent_model_signature = Signature(
    parameters=[Parameter('self', Parameter.POSITIONAL_ONLY)] + model_parameters,
    return_annotation=original_signature.return_annotation
  )

  def __init__(self, *args, **kwargs):
    arguments = actual_constructor_signature.bind(*args, **kwargs)
    arguments.apply_defaults()

    self.constructor_arguments = arguments.arguments.copy()
    self.constructor_arguments.update(fixed)

    ### putting new defaults back to **kwargs
    for kw_key in kw_defaults:
      self.constructor_arguments[kw_parameter][kw_key] = self.constructor_arguments.pop(kw_key, kw_defaults[kw_key])

  def __call__(self, *args, **kwargs):
    arguments = actual_model_signature.bind(*args, **kwargs)

    if inject_model is not None and inject_model in arguments.arguments:
      raise Exception('model injection argument is already specified!')

    arguments.apply_defaults()
    model_arguments = arguments.arguments.copy()

    if inject_model is not None:
      model_arguments[inject_model] = self

    for p in self.constructor_arguments:
      if p in duplicated and p in model_arguments:
        model_arguments[p] = duplicated[p](
          self.constructor_arguments[p],
          model_arguments[p],
        )
      else:
        model_arguments[p] = self.constructor_arguments[p]

    args, kwargs = bind(original_signature, model_arguments)
    return original(*args, **kwargs)

  def __str__(self, ):
    name = getattr(original, '__name__', '')
    return '%s[%s] -> (%s) -> %s' % (
      name,
      ', '.join('%s=%s' % (k, v) for k, v in fixed.items()),
      actual_constructor_signature,
      actual_model_signature
    )

  __init__.__signature__ = apparent_constructor_signature
  __call__.__signature__ = apparent_model_signature

  original_name = getattr(original, '__name__', 'node')
  if len(original_name) == 0:
    clazz_name = 'NodeModel'
  else:
    clazz_name = '%s%sModel' % (original_name[0].upper(), original_name[1:])

  model_clazz = type(
    clazz_name,
    (base_constructor_class,),
    dict(
      __init__=__init__,
      __str__=__str__,
      __call__=__call__,
    )
  )

  return model_clazz

class CarryingExpression(object):
  """
  Allows nice syntax for `carry` method:
  carry(<function>, ['param1', 'param2']).with_fixed(param1=value1).with_defaults(param3=value3)()
  """
  def __init__(
    self, original,
    fixed=None, defaults=None,
    carried=None, duplicated=None,
    base_constructor_class=NodeModel
  ):
    self.original = original

    self.fixed = dict() if fixed is None else fixed
    self.defaults = dict() if defaults is None else defaults
    self.carried = tuple() if carried is None else carried
    self.duplicated = dict() if duplicated is None else duplicated

    self.base_constructor_class = base_constructor_class

  def __call__(self, inject_model=None):
    return carry(
      self.original,
      self.fixed, self.defaults, self.carried,
      base_constructor_class=self.base_constructor_class,
      duplicated=self.duplicated,
      inject_model=inject_model
    )

  def with_defaults(self, **kwargs):
    self.defaults.update(kwargs)
    return self

  def with_fixed(self, **kwargs):
    self.fixed.update(kwargs)
    return self

def model_from(clazz, carried=('incoming', ), duplicated=None, base_constructor_class=NodeModel):
  return CarryingExpression(
    clazz,
    carried=carried,
    duplicated=duplicated,
    base_constructor_class=base_constructor_class
  )