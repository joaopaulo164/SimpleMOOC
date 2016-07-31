from django.contrib import admin
from .models import (Course, Enrollment, Announcement, Comment, Lesson, Material)

# Register your models here.


class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'start_date', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


# Para cadastrar o material dentro de uma aula (Inline - Tudo numa linha)
class MaterialTabularInlineAdmin(admin.TabularInline):
    model = Material


# Para cadastrar o material dentro de uma aula (Inline - Dividido em blocos)
class MaterialStackedInlineAdmin(admin.StackedInline):
    model = Material


class LessonAdmin(admin.ModelAdmin):
    list_display = ['name', 'number', 'course', 'release_date']
    search_fields = ['name', 'description']
    list_filter = ['created_at']

    inlines = [
        MaterialStackedInlineAdmin # Uso do material inline
    ]

    # Inline com TabularInline
    # inlines = [
    #     MaterialTabularInlineAdmin # Uso do material inline
    # ]


admin.site.register(Course, CourseAdmin)
admin.site.register([Enrollment, Announcement, Comment, Material])
admin.site.register(Lesson, LessonAdmin)