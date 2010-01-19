import types

def Enum(*defs):
  """http://code.activestate.com/recipes/413486/"""
  assert defs, "Empty enums are not supported"

  names = []
  namedict = {}
  idx = 0
  for item in defs:
    if type(item) == types.TupleType:
      name, idx = item
    else:
      name = item
    namedict[idx] = name
    names.append(name)
    idx += 1

  class EnumClass(object):
    __slots__ = names
    def __iter__(self):        return iter(constants)
    def __len__(self):         return len(constants)
    def __getitem__(self, i):  return constants[i]
    def __repr__(self):        return 'Enum' + str(names)
    def __str__(self):         return 'enum ' + str(constants)

  class EnumValue(object):
    __slots__ = ('__value')
    def __init__(self, value): self.__value = value
    Value = property(lambda self: self.__value)
    EnumType = property(lambda self: EnumType)
    def __hash__(self):        return hash(self.__value)
    def __cmp__(self, other):
      # C fans might want to remove the following assertion
      # to make all enums comparable by ordinal value {;))
      assert self.EnumType is other.EnumType, "Only values from the same enum are comparable"
      return cmp(self.__value, other.__value)
    def __invert__(self):      return constants[maximum - self.__value]
    def __nonzero__(self):     return bool(self.__value)
    def __repr__(self):        return str(namedict[self.__value])

  maximum = len(names) - 1
  constants = {}
  i = 0
  for item in defs:
    if type(item) == types.TupleType:
      name, idx = item
    else:
      name, idx = item, i
    assert idx not in constants
    i = idx + 1
    val = EnumValue(idx)
    setattr(EnumClass, name, val)
    constants[idx] = val
  EnumType = EnumClass()
  return EnumType

