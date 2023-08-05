# Same as IQN

class InvalidNQN(ValueError):
    def __init__(self, name):
        super(InvalidNQN, self).__init__('Invalid NQN {}'.format(name))


class NVMeName(object):
    def __init__(self, name):
        super(NVMeName, self).__init__()
        self._name = name._name if isinstance(name, NVMeName) else name.lower() # pylint: disable=protected-access

    def __repr__(self):
        return self._name

    def __hash__(self):
        return hash(self._name)

    def __eq__(self, other):
        if not isinstance(other, NVMeName):
            try:
                other = NVMeName(other)
            except Exception:  # pylint: disable=broad-except
                return False
        return self._name == other._name  # pylint: disable=protected-access

    def __ne__(self, other):
        return not (self == other)  # pylint: disable=superfluous-parens


class NQN(NVMeName):
    def __init__(self, name):
        super(NQN, self).__init__(name)
        fields = self._name.split(':')
        base, self._extra = fields[0], tuple(fields[1:])
        base_fields = base.split('.')
        if len(base_fields) < 2:
            raise InvalidNQN(name)
        self._type = base_fields[0]
        self._date = base_fields[1]
        self._naming_authority = '.'.join(base_fields[2:])
        if self._type != 'nqn':
            raise InvalidNQN(name)

    def get_date(self):
        return self._date

    def get_naming_authority(self):
        return self._naming_authority

    def get_extra(self):
        return ':'.join(self._extra)

    def get_extra_fields(self):
        return self._extra


def make_nvme_name(nvme_name):
    try:
        return NQN(nvme_name)
    except InvalidNQN:
        return NVMeName(nvme_name)
