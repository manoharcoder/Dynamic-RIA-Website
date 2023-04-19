from django.contrib import admin
from riaapp.models import *
# Register your models here.

admin.site.register(Register)
admin.site.register(Cources)
admin.site.register(Payments)
admin.site.register(Documents)
admin.site.register(Certificate)
# admin.site.register(Contact)
admin.site.register(Trainer)
admin.site.register(Attendance)



class ContactAdmin(admin.ModelAdmin):
    list_display=('name',
                  'email',
                  'phoneNumber',
                  'description',)
    search_fields=('name','email','phoneNumber')
    list_filter=['name','email']
admin.site.register(Contact,ContactAdmin)

