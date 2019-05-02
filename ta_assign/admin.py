from django.contrib import admin

# Register your models here.
from .models import (User)
from .models import (Course)
from .models import (Lecture)
from .models import (Lab)
from .models import (InstructorCourse)
from .models import (TACourse)
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Lab)
admin.site.register(InstructorCourse)
admin.site.register(TACourse)

