import plone.api


def trashEventHandler(ob, event):
    """ Item is deleted - trash it!"""
    try:
        can = plone.api.portal.get_tool('portal_trash_can')
    except plone.api.exc.InvalidParameterError:
        pass  # not installed
    except plone.api.exc.CannotGetPortalError:
        pass  # portal is being deleted
    else:
        can.trash(ob)


def trashAdded(ob, event):
    """ nothing for now """
    pass


def trashRemoved(ob, event):
    """ nothing for now """
    pass
