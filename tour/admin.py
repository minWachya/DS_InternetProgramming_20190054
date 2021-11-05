from django.contrib import admin
from .models import PackageTour, Category, Tag

# Register your models here.


# PackageTour 등록
admin.site.register(PackageTour)

# Category 등록
# slug 필드는 자동 등록
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Category, CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Tag, TagAdmin)