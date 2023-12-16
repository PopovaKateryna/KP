from django.contrib import admin
from .models import SiteInformation, Company, Tax, UsersWork, Payment

admin.site.register(SiteInformation)
admin.site.register(Company)
admin.site.register(Tax)
admin.site.register(UsersWork)
admin.site.register(Payment)
