from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ['username', 'email', 'tipo', 'is_active', 'is_staff']
    search_fields = ['email', 'username']
    ordering = ['date_joined']
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'tipo', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)



# from django.contrib import admin
# from accounts.models import Endereco, Cliente, CustomUser

# admin.site.register(Endereco)
# admin.site.register(Cliente)
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser

# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = ('username', 'email', 'tipo', 'is_active', 'is_staff')
#     fieldsets = (
#         (None, {'fields': ('username', 'email', 'password')}),
#         ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'password1', 'password2', 'tipo', 'is_active', 'is_staff')}
#         ),
#     )
#     ordering = ('email',)

#     def save_model(self, request, obj, form, change):
#         if form.cleaned_data.get("password"):
#             obj.set_password(form.cleaned_data["password"])
#         super().save_model(request, obj, form, change)

# admin.site.register(CustomUser, CustomUserAdmin)

