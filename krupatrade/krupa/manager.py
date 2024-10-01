from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,email,password = None, **extra_feilds):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_feilds)
        user.set_password(password)
        user.save(using = self.db)
        return user
    
    def create_super_user(self,email,password = None, **extra_feilds):
        extra_feilds.setdefault('is_staff',True)
        extra_feilds.setdefault('is_superuser',True)
        extra_feilds.setdefault('is_active',True)

        return self.create_user(email,password,**extra_feilds)
    