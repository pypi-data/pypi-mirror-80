from Products.CMFCore import permissions as CMFCorePermissions

# manage the trash can
ManageTrash = "ims.trashcan: Manage trash can"

CMFCorePermissions.setDefaultRoles(ManageTrash, ('Manager',))
