
from django.contrib import admin
from .models import Candidat, Choice, Question, Personality, Opinion ,Support
from django.db.models import Count, Avg, F, FloatField
from django.utils.html import format_html
from chartjs.views.lines import BaseLineChartView


# Register Opinion and Personality models as admin classes
@admin.register(Opinion)
class OpinionAdmin(admin.ModelAdmin):
    list_display = ('user', 'personality', 'likes', 'dislikes', 'comment', 'type_personality')
    list_filter = ('likes', 'dislikes', 'type_personality')
    search_fields = ('user__username', 'personality__name', 'comment', 'type_personality')

@admin.register(Personality)
class PersonalityAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_total_likes', 'get_total_dislikes', 'get_percentage_likes', 'get_percentage_dislikes']

    def get_total_likes(self, obj):
        return Opinion.objects.filter(personality=obj, likes=True).count()
    
    get_total_likes.short_description = 'Number of Likes'

    def get_total_dislikes(self, obj):
        return Opinion.objects.filter(personality=obj, dislikes=True).count()
    
    get_total_dislikes.short_description = 'Number of Dislikes'

    def get_percentage_likes(self, obj):
        total_opinions = Opinion.objects.filter(personality=obj).count()
        if total_opinions > 0:
            likes = Opinion.objects.filter(personality=obj, likes=True).count()
            return '{:.2f}%'.format((likes / total_opinions) * 100)
        else:
            return 'N/A'
    
    get_percentage_likes.short_description = 'Percentage of Likes'

    def get_percentage_dislikes(self, obj):
        total_opinions = Opinion.objects.filter(personality=obj).count()
        if total_opinions > 0:
            dislikes = Opinion.objects.filter(personality=obj, dislikes=True).count()
            percentage_dislikes = (dislikes / total_opinions) * 100
            color = 'red' if percentage_dislikes > 50 else 'green'
            return format_html('<span style="color:{};">{:.2f}%</span>'.format(color, percentage_dislikes))
        else:
            return 'N/A'
    
    get_percentage_dislikes.short_description = 'Percentage of Dislikes'

@admin.register(Candidat)
class CandidatAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'genre', 'age_range', 'categorie_socioprofessionnelle', 'ville', 'get_percentage_age_range')
    search_fields = ('username', 'email')

    def get_percentage_age_range(self, obj):
        total_candidates = Candidat.objects.count()
        age_ranges = Candidat.objects.values('age_range').annotate(count=Count('age_range')).order_by('age_range')
        percentages = {entry['age_range']: (entry['count'] / total_candidates) * 100 for entry in age_ranges}
        return ', '.join([f"{age_range}: {percentage:.2f}%" for age_range, percentage in percentages.items()])

    get_percentage_age_range.short_description = 'Percentage of Candidates in Age Range'

# Register other models
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Support)

