from django.contrib import admin
from App.models import Guest, Table, Reservation

# Register your models here.
admin.site.register(Guest)
admin.site.register(Table)
admin.site.register(Reservation)