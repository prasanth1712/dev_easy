from django.contrib import admin
from app.models.objectmodel import wmobject,wmobject_details,lookups,wmobject_attachments,attach_lookup,wmobject_rel_notes
# Register your models here.
admin.site.register(wmobject)
admin.site.register(wmobject_details)
admin.site.register(lookups)
admin.site.register(wmobject_attachments)
admin.site.register(attach_lookup)
admin.site.register(wmobject_rel_notes)