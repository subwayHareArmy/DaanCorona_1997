from django.contrib import admin
from main.models import CustomUser, SMSDevice, Recipient, Donor, Donation

admin.site.register(CustomUser)
admin.site.register(SMSDevice)
admin.site.register(Recipient)
admin.site.register(Donor)
admin.site.register(Donation)