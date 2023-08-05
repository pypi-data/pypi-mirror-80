from Products.CMFCore import utils

from . import can


def initialize(context):
    utils.ToolInit(
        'ims.trashcan tool',
        tools=(can.PloneTrashCan,),
        icon='tool.png', ).initialize(context)
