Introduction
============


ims.trashcan provides a way to maintain a backup of recently deleted content without having to resort to 
backups or rolling back commits that could include several entangled commits occurring after the item was
deleted.


How it Works
============

The goal of this package is to store actual python objects without them being an actual
object in the database. A trashed item should not be able to be traversed to or have any of its methods
or attributes accessed, but exist only as binary data until restored. To do this they are stored as
python pickles. Pickles are serialized python objects that can be deserialized and in fact this is how
the ZODB operates. To store data as pickles, we actually create a ZODB Blob using the ZODB export
process. A trashed item has the following attributes:

 - data: a Blob instance of the ZODB export
 - path: the traversal path from which it was deleted
 - id: a unique id in the trash can, consisting of the original item's id + a timestamp
 - title: title of the original item
 - _created: a DateTime instance of when the trash item was created
 
Trashed items are restored using an inverse process, where ZODB import deserializes the Blob pickle.


Configuration and Cleanup
============

In the ZMI in a site's portal_trash_can you can configure the number of days to keep content (default 7)
before removing from the site (you will still need to pack your database after this point for them to be
fully removed from it). This will be respected by this tool's `__call__` method which you can access
programmatically:

```python
>>> import plone.api
>>> can = plone.api.portal.get('portal_trash_can')
>>> can()
```

or via HTTP request `http://localhost:8080/Plone/portal_trash_can`

It is recommended that you set up a cron job to execute this periodically.


# Trashable Items

By default, any object that provides the plone.dexterity.interfaces.IDexterityItem interface will be
trashable. Not that this does not include IDexterityContainer. It is possible to register other subscribers
to trigger entering the trashcan using ZCML. This example shows how to register an imagined interface
"foo.bar.interfaces.IMyInterface" in the event that it is deleted (IObjectRemovedEvent).

```xml
  <subscriber
     for="foo.bar.interfaces.IMyInterface
          zope.lifecycleevent.interfaces.IObjectRemovedEvent"
     handler="ims.trashcan.events.trashEventHandler" />
```

Note that this
is completely unnecessary for items that are Dexterity non-container objects and in fact would result in
duplicates

## Deleted containers

By default, IDexterityContainer is not a registered trashable interface. This is because the IObjectRemovedEvent
will trigger twice for any contained objects if we try to trash it. This not only doubles the amount of
data entering the trash can, it also doubles the overhead time needed to delete the item. Generally, 
containers only have metadata and what we care about are the pages and files contained in it.
It is strongly recommended that you do not register a container as trashable unless you understand this
caveat and deem it absolutely necessary and worth the added cost.

# Restoring Items

To restore an item, first find it via the site's ZMI: ${site_url}/portal_trash_can/manage_workspace. This
lists all non-expired deleted items by "id + timestamp". Accessing a trashed item contains metadata
including original title and deletion date/time. There are no options when restoring content, it will
simply restore it to the original location. If that original location no longer exists, it will
restore it to the portal root

## Restoring an Entire Folder

Barring custom delete subscribers for that content type, a folderish object will generally not itself
be included in the trash can. Consider the following folder structure given these ids.

```
portal/
└── folderA/
    ├── page1
    └── page2
```
If folderA is deleted, the trash can will contain two entries: page1 and page2. By default, since
folderA no longer exists, these would be restored to the portal root. You can however first create
a root folder folderA and then restore these pages, which will restore them to their original location.

### Exceptions

In some cases it will not be possible to restore content without additional work:
- The deleted page has been replaced by a new page with an identical id. You will have to rename the id
of the new page before being able to restore
- A deleted folder has been replaced by a non-container with the identical id. In the above example, this
would correlate to /portal/folderA being replaced by e.g. a Page with that path. You will not be able to restore
/portal/folderA/page1 because the current /portal/folderA cannot contain items. You will need to rename
the new folderA and create an actual folder in its place
- The python class is no longer included in the Zope client. In this case the pickle cannot be
deserialized until it is included in Zope. You will need to restore the client and/or roll back changes
to make that class available.