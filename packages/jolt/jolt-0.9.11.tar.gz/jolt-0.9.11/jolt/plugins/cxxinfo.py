from jolt import filesystem as fs
from jolt import utils
from jolt.cache import ArtifactStringAttribute
from jolt.cache import ArtifactAttributeSet
from jolt.cache import ArtifactAttributeSetProvider


class CppInfoVariable(ArtifactStringAttribute):
    def __init__(self, name):
        super(CppInfoVariable, self).__init__(name)

    def apply(self, task, artifact):
        pass

    def unapply(self, task, artifact):
        pass


class CppInfoListVariable(CppInfoVariable):
    def __init__(self, name):
        super(CppInfoListVariable, self).__init__(name)

    def set_value(self, value):
        values = utils.as_list(value)
        super(CppInfoListVariable, self).set_value(":".join(values))

    def append(self, value):
        value = ":".join(utils.as_list(value))
        if self.get_value():
            self.set_value(self.get_value() + ":" + value)
        else:
            self.set_value(value)

    def items(self):
        value = self.get_value()
        return value.split(":") if value is not None else []


class CppInfoDictVariable(CppInfoListVariable):
    def __init__(self, name):
        super(CppInfoDictVariable, self).__init__(name)

    def __setitem__(self, key, value=None):
        item = "{0}={1}".format(key, value) if value is not None else key
        self.append(item)


class CppInfo(ArtifactAttributeSet):
    def __init__(self):
        super(CppInfo, self).__init__()

    def create(self, name):
        if name == "asflags":
            return CppInfoListVariable("asflags")
        if name == "cflags":
            return CppInfoListVariable("cflags")
        if name == "cxxflags":
            return CppInfoListVariable("cxxflags")
        if name == "incpaths":
            return CppInfoListVariable("incpaths")
        if name == "ldflags":
            return CppInfoListVariable("ldflags")
        if name == "libpaths":
            return CppInfoListVariable("libpaths")
        if name == "libraries":
            return CppInfoListVariable("libraries")
        if name == "macros":
            return CppInfoDictVariable("macros")
        assert False, "no such cxxinfo attribute: {0}".format(name)


@ArtifactAttributeSetProvider.Register
class CppInfoProvider(ArtifactAttributeSetProvider):
    def create(self, artifact):
        setattr(artifact, "cxxinfo", CppInfo())

    def parse(self, artifact, content):
        if "cxxinfo" not in content:
            return
        for key, value in content["cxxinfo"].items():
            setattr(artifact.cxxinfo, key, value)

    def format(self, artifact, content):
        if "cxxinfo" not in content:
            content["cxxinfo"] = {}
        for key, value in artifact.cxxinfo.items():
            content["cxxinfo"][key] = str(value)

    def apply(self, task, artifact):
        pass

    def unapply(self, task, artifact):
        pass
