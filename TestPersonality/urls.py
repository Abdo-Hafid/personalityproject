from django.urls import path
from .views import test,register_candidate,questionnaire,MaxOverallPersonalityView,SubmitOpinionView,likes_by_age,ajouter_page,likes_by_age_chart,ajouter_quest,ajouter_choice,register_student,error_page
#from .views import end,PersonalityStatsView,DashboardStatisticsView,SubmitOpinionView,SaveOpinionsView,MerciView,RegisterOpinionView,test,questionnaire,register_candidate,display_responses,result,hello,ResponseListView,MaxOverallPersonalityView,StatisticsView
app_name = 'TestPersonality'
urlpatterns = [
    # path('25personalities/', hello, name='register_candidate'),
     path('questionnaire/<int:candidat_id>/', questionnaire, name='questionnaire'),
     path('register', register_candidate, name='register_candidate'),
    # path('result/<int:candidat_id>/', result, name='result'),
    # path('resultes/', ResponseListView.as_view(), name='resultes'),
    # path('display-responses/', display_responses, name='display_responses'),
     path('max_overall_personality/<int:candidat_id>/', MaxOverallPersonalityView.as_view(), name='max_overall_personality'),
     path('submit_opinion/', SubmitOpinionView.as_view(), name='submit_opinion'),
    # path('register_opinion/', RegisterOpinionView.as_view(), name='register_opinion'),   
    # path('statistics/', PersonalityStatsView.as_view(), name='statistics'),
     path('error/', error_page, name='error'),
     path('', test, name='test'),
     path('ajouter_page/', ajouter_page, name='ajouter_page'),
     path('ajouter/<int:id>/', ajouter_page, name='edit_personality'),
     path('ajouter_quest/', ajouter_quest, name='ajouter_quest'),
     path('ajouterqest/<int:id>/', ajouter_quest, name='edit_question'),
     path('ajouterchoice/', ajouter_choice, name='ajouter_choice'),
     path('ajouterchoice/<int:id>/', ajouter_choice, name='edit_choice'),
     path('regester_std/', register_student, name='register_student'),
    # path('end/', end, name='end'),
    # path('merci/<int:candidat_id>/', MerciView.as_view(), name='merci'),
    # path('save_opinions/', SaveOpinionsView.as_view(), name='save_opinions'),
     path('likes-by-age/', likes_by_age, name='likes_by_age'),
     path('likes-by-age-chart/', likes_by_age_chart, name='likes_by_age_chart'),


    
]