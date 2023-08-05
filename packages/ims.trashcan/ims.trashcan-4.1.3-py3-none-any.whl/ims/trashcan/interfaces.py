from zope.interface.interface import Interface
from zope.schema import Bytes, TextLine


class ITrashedItem(Interface):
    """ deleted item with trash wrapper """
    id = TextLine(
        title="ID",
        description="ID",
    )

    Title = TextLine(
        title="Title",
        description="Original title",
    )

    data = Bytes(
        title="Data",
        description="The fake zexp file",
    )

    path = TextLine(
        title="Path",
        description="The path to its restore point",
    )


class ITrashCan(Interface):
    """ marker """
