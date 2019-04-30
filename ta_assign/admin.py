from django.contrib import admin

# Register your models here.
from .models import (User)
from .models import (Course)
from .models import (TACourse)
admin.site.register(User)
admin.site.register(Course)
admin.site.register(TACourse)
