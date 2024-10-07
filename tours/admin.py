from django import forms
from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from ckeditor.widgets import CKEditorWidget

from main.models import BestChoice, RestIdea
from .models import *
from common.models import *
from django.contrib.auth.models import Group, User

admin.site.unregister(User)
admin.site.unregister(Group)


class TourCommentsAdminForm(forms.ModelForm):
    comment = forms.CharField(
        label='Комментарий',
        widget=CKEditorWidget(config_name='default')
    )

    class Meta:
        model = TourComments
        fields = '__all__'


class TourAdminForm(forms.ModelForm):
    description = forms.CharField(
        label='Описание',
        widget=CKEditorWidget(config_name='default')
    )

    class Meta:
        model = Tour
        fields = '__all__'


@admin.register(TourComments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'tour', 'rate', 'date', 'is_approved']
    list_filter = ['is_approved', 'date', 'rate']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        for comment in queryset:
            if comment.tour:
                comment.tour.update_rating()

    approve_comments.short_description = "Одобрить выбранные отзывы"


class TourImageInline(TabularInline):
    max_num = 15
    extra = 1
    model = TourImage


@admin.register(Tour)
class TourAdmin(ModelAdmin):
    form = TourAdminForm
    inlines = [TourImageInline]
    list_display = ['title', 'start_tour', 'end_tour', 'get_final_rating', 'rating_count', 'is_best_choice', 'is_rest_idea']
    readonly_fields = ['average_rating', 'rating_count']
    list_editable = ['is_best_choice', 'is_rest_idea']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.update_rating()
        self._update_special_lists(obj)

    def get_final_rating(self, obj):
        return obj.get_final_rating()

    get_final_rating.short_description = 'Рейтинг'

    def _update_special_lists(self, tour):
        rest_idea, _ = RestIdea.objects.get_or_create(id=1)
        if tour.is_rest_idea:
            rest_idea.tours.add(tour)
        else:
            rest_idea.tours.remove(tour)

        best_choice, _ = BestChoice.objects.get_or_create(id=1)
        if tour.is_best_choice:
            best_choice.tours.add(tour)
        else:
            best_choice.tours.remove(tour)


@admin.register(TourInquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'email', 'created_at', 'tour']
    list_filter = ['created_at', 'tour']
    search_fields = ['name', 'phone_number', 'email']
    readonly_fields = ['created_at']


@admin.register(IconsAfterName)
class IconsAfterNameAdmin(admin.ModelAdmin):
    list_display = ['icon_city_country', 'icon_date']
