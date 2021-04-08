from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm
from .models import CustomUser,Challan


class ChallanAdmin(admin.ModelAdmin):
	model=Challan
	list_display=['id','name','email','fine','place','license_number','vechile_type','created_by']
	

admin.site.register(Challan,ChallanAdmin)


class CustomUserAdmin(UserAdmin):
	model=CustomUser
	add_form=CustomUserCreationForm

	fieldsets=(
		*UserAdmin.fieldsets,(
			"User Info",{
				'fields':("date_of_birth",'address',"profile","active")
			     }
		)
	)

admin.site.register(CustomUser,CustomUserAdmin)