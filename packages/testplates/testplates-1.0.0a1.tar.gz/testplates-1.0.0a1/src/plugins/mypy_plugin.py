from typing import Callable, Optional, Final
from mypy.plugin import Plugin, ClassDefContext

ClassDefContextHook = Optional[Callable[[ClassDefContext], None]]

TESTPLATES_STRUCTURE_DECORATOR: Final[str] = "testplates.structure.struct"


class TestplatesPlugin(Plugin):
    def get_class_decorator_hook(self, fullname: str) -> ClassDefContextHook:
        if fullname == TESTPLATES_STRUCTURE_DECORATOR:
            return testplates_structure_class_decorator_hook

        return None


def testplates_structure_class_decorator_hook(context: ClassDefContext) -> None:
    info = context.cls.info
    structure_instance = context.reason.node.type.ret_type.item

    info.is_final = True
    info.mro.insert(1, structure_instance.type)
    info.bases.insert(-1, structure_instance)


def plugin(version: str):
    if not version.startswith("0.790"):
        pass

    return TestplatesPlugin
