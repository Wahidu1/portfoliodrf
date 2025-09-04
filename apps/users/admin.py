from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.users.models import BlogPost, ContactMessage, MyAchievement, MyExperience, MyUser, MySkill, MyWork, Settings, Technology, SettingFiles
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
@admin.register(MyUser)
class UserAdmin(BaseUserAdmin):
    # Fields to display in the list view
    list_display = ('email', 'name', 'is_superuser', 'is_staff')

    # Fields to filter by in the admin list view
    list_filter = ('is_superuser', 'is_staff', 'is_active')

    # The field used for ordering the list
    ordering = ('email',)  # email instead of username

    # Fields for detail view in admin
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Fields for adding a new user in admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )

    # Make email the unique identifier instead of username
    search_fields = ('email', 'name')

@admin.register(MySkill)
class MySkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'order', 'display_icon')  # remove 'user' if not present
    list_editable = ('percentage', 'order')
    list_filter = ('percentage', 'order')
    search_fields = ('name',)
    ordering = ('order', 'name')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'icon', 'percentage')
        }),
        ('Display Settings', {
            'fields': ('order',),
            'classes': ('collapse',)
        }),
    )

    def display_icon(self, obj):
        """Show icon preview in admin list view."""
        if obj.icon:
            return format_html('<img src="{}" width="50" height="50" />', obj.icon.url)
        return "No icon"
    display_icon.short_description = 'Icon Preview'

    def save_model(self, request, obj, form, change):
        """Ensure percentage does not exceed 100."""
        if obj.percentage > 100:
            obj.percentage = 100
        super().save_model(request, obj, form, change)


# ----------------------------
# Technology Admin
# ----------------------------
@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name", "icon")
    search_fields = ("name",)
    ordering = ("name",)

# ----------------------------
# MyWork Admin
# ----------------------------
class MyWorkTechnologyInline(admin.TabularInline):
    model = MyWork.technologies.through
    extra = 1

@admin.register(MyWork)
class MyWorkAdmin(admin.ModelAdmin):
    list_display = ("title", "subtext", "order", "thumbnail")
    list_filter = ("technologies",)
    search_fields = ("title", "subtext", "description")
    ordering = ("order",)
    inlines = [MyWorkTechnologyInline]
    exclude = ("technologies",)  # exclude M2M from main form to use inline

    # show small image thumbnail
    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover;" />', obj.image.url)
        return "-"
    thumbnail.short_description = "Image"

@admin.register(MyAchievement)
class MyAchievementAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "order", "thumbnail")
    search_fields = ("title", "description")
    ordering = ("order",)

    # Show small thumbnail for the achievement image
    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit:cover;" />',
                obj.image.url
            )
        return "-"
    thumbnail.short_description = "Image"
@admin.register(MyExperience)
class MyExperienceAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "start_date", "end_date", "order", "duration")
    search_fields = ("title", "company", "description")
    ordering = ("order",)
    list_filter = ("company",)

    # Optional: show duration in admin list
    def duration(self, obj):
        end = obj.end_date or "Present"
        return f"{obj.start_date} - {end}"
    duration.short_description = "Duration"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "short_message", "created_at")
    search_fields = ("name", "email", "message")
    ordering = ("-created_at",)
    readonly_fields = ("name", "email", "message", "created_at", "updated_at")

    # Show first 50 characters of message
    def short_message(self, obj):
        if len(obj.message) > 50:
            return f"{obj.message[:50]}..."
        return obj.message
    short_message.short_description = "Message Preview"


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "published_at", "thumbnail")
    list_filter = ("status", "published_at")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}  # Auto-fill slug from title
    ordering = ("-published_at",)
    readonly_fields = ("published_at",)

    # Show small thumbnail in list view
    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit:cover;" />',
                obj.image.url
            )
        return "-"
    thumbnail.short_description = "Image"


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ("key", "short_value")
    search_fields = ("key", "value")
    ordering = ("key",)
    readonly_fields = ()  # Make fields editable; remove if you want read-only

    # Show a shortened preview of the value to keep the list clean
    def short_value(self, obj):
        if len(obj.value) > 50:
            return f"{obj.value[:50]}..."
        return obj.value
    short_value.short_description = "Value"

@admin.register(SettingFiles)
class SettingFilesAdmin(admin.ModelAdmin):
    list_display = ("name", "file")
    search_fields = ("name",)
    ordering = ("name",)
