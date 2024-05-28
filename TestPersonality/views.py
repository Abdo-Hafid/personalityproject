from itertools import count
from django.views import View
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import Question, Choice ,Candidat,Response,Personality,Percandidat,Opinion,PersonalityOpinion,Support
#from .forms import QuestionnaireForm,CandidateForm,OpinionForm,PersonalityOpinionForm
from django.db.models import Count,Case, When, IntegerField, Sum,F
from django.views.generic.list import ListView
from .models import Response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic import TemplateView
from .forms import CandidateForm,QuestionnaireForm,PersonalityForm,QuestionForm,ChoiceForm,EtudiantsForm
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.contrib import admin




# Create your views here.
import logging

logger = logging.getLogger(__name__)
MOROCCAN_CITIES = (
    ('Agadir', 'Agadir'),
    ('Al Hoceima', 'Al Hoceima'),
    ('Asilah', 'Asilah'),
    ('Azemmour', 'Azemmour'),
    ('Azrou', 'Azrou'),
    ('Beni Mellal', 'Beni Mellal'),
    ('Berkane', 'Berkane'),
    ('Berrechid', 'Berrechid'),
    ('Boujdour', 'Boujdour'),
    ('Casablanca', 'Casablanca'),
    ('Chefchaouen', 'Chefchaouen'),
    ('Dakhla', 'Dakhla'),
    ('El Jadida', 'El Jadida'),
    ('Errachidia', 'Errachidia'),
    ('Essaouira', 'Essaouira'),
    ('Fes', 'Fes'),
    ('Fnideq', 'Fnideq'),
    ('Guelmim', 'Guelmim'),
    ('Ifrane', 'Ifrane'),
    ('Khenifra', 'Khenifra'),
    ('Khmissat', 'Khmissat'),
    ('Khouribga', 'Khouribga'),
    ('Laayoune', 'Laayoune'),
    ('Larache', 'Larache'),
    ('Marrakech', 'Marrakech'),
    ('Martil', 'Martil'),
    ('Meknes', 'Meknes'),
    ('Mohammedia', 'Mohammedia'),
    ('Nador', 'Nador'),
    ('Ouarzazate', 'Ouarzazate'),
    ('Oued Zem', 'Oued Zem'),
    ('Oujda', 'Oujda'),
    ('Rabat', 'Rabat'),
    ('Safi', 'Safi'),
    ('Salé', 'Salé'),
    ('Sefrou', 'Sefrou'),
    ('Settat', 'Settat'),
    ('Sidi Kacem', 'Sidi Kacem'),
    ('Sidi Slimane', 'Sidi Slimane'),
    ('Sidi Yahya El Gharb', 'Sidi Yahya El Gharb'),
    ('Skhirat', 'Skhirat'),
    ('Tanger', 'Tanger'),
    ('Tan-Tan', 'Tan-Tan'),
    ('Taza', 'Taza'),
    ('Temara', 'Temara'),
    ('Tetouan', 'Tetouan'),
    ('Tiflet', 'Tiflet'),
    ('Tiznit', 'Tiznit'),
    ('Youssoufia', 'Youssoufia'),
)
AGE_RANGES = (
    ('20-30', '20-30'),
    ('30-40', '30-40'),
    ('40-50', '40-50'),
    ('>50', '>50'),
)

CategorieSocioProfessionnelleChoices = (
        ('etudiant', 'Étudiant'),
        ('employe', 'Employé'),
        ('cadre', 'Cadre'),
        ('travailleur_independant', 'Travailleur indépendant'),
        ('sans_emploi', 'Sans emploi'),
        ('autre', 'Autre'),
    )
def register_candidate(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            logger.info(f'Username: {username}')  # Use logger instead of print
            if username == "R.EL2024@2025":
                return redirect('TestPersonality:statistics')
            else:
                existing_candidate = Candidat.objects.filter(username=username).first()
                if existing_candidate:
                    messages.error(request, 'Candidate with this username already exists.')
                else:
                    candidat = form.save()
                    
                    questionnaire_url = reverse('TestPersonality:questionnaire', kwargs={'candidat_id': candidat.id})
                    return redirect(questionnaire_url)
    else:
        form = CandidateForm()

    context = {
        'form': form,
        'AGE_RANGES': AGE_RANGES,
        'MOROCCAN_CITIES':MOROCCAN_CITIES,
        'CategorieSocioProfessionnelleChoices': CategorieSocioProfessionnelleChoices,
    }

    return render(request, 'register_candidate.html', context)


def hello(request):
 return render(request, 'hello.html')
def test(request):
 return render(request, 'index.html')

# def display_responses(request):
#     candidats_with_personality_count = Candidat.objects.annotate(personality_count=Count('response__choice__personalities')).all()
#     responses = Response.objects.select_related('choice__question').all()
#     return render(request, 'display_responses.html', {'responses': responses, 'candidats_with_personality_count': candidats_with_personality_count})




# #-----------azga-------------
def questionnaire(request, candidat_id):
    try:
        candidat = Candidat.objects.get(id=candidat_id)
    except Candidat.DoesNotExist:
        messages.error(request, 'Candidate not found.')
        return redirect('some_error_page')

    if request.method == 'POST':
        questions = Question.objects.all()
        questionnaire_form = QuestionnaireForm(request.POST, questions=questions)

        if questionnaire_form.is_valid():
            # Clear existing responses for the candidate
            Response.objects.filter(candidat=candidat).delete()

            # Save responses for each question
            for question in questions:
                choice_obj = questionnaire_form.cleaned_data.get(f'question_{question.id}')
                if choice_obj:
                    Response.objects.create(candidat=candidat, choice=choice_obj)
                else:
                    print(f"Choice for question {question.id} is missing in the form data.")

            return redirect('TestPersonality:max_overall_personality', candidat_id=candidat_id)
        else:
            print("Data problem in form validation:", questionnaire_form.errors) 
    else:
        questions = Question.objects.all()
        questionnaire_form = QuestionnaireForm(candidat_username=candidat.username, questions=questions)

    return render(request, 'questionnaire.html', {'questionnaire_form': questionnaire_form, 'questions': questions, 'candidat': candidat})
# #-----------azga-------------

# def result(request, candidat_id):
#     candidate = Candidat.objects.get(pk=candidat_id)
#     print("Candidat ID:", candidat_id)
#     personalities_with_candidate_count = Personality.objects.filter(choice__response__candidat=candidate).annotate(candidate_count=Count('choice__response__candidat', distinct=True)).all()
#     print("Personalities with Candidate Count:", personalities_with_candidate_count)
#     return render(request, 'result.html', {'candidate': candidate, 'personalities_with_candidate_count': personalities_with_candidate_count})


# class ResponseListView(ListView):
#     model = Response
#     template_name = 'result.html'

    
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         users = set(Response.objects.values_list('candidat__username', flat=True))

#         response_data = []

#         for user in users:
#             user_responses = Response.objects.filter(candidat__username=user)

#             # Get all personalities and their overall counts for the user
#             all_personalities_count = Personality.objects.filter(
#                 choice__response__in=user_responses
#             ).values('name').annotate(total_count=Count('name'))

#             # Find the personality with the highest overall count for the user
#             if all_personalities_count:
#                 max_overall_personality = max(all_personalities_count, key=lambda x: x['total_count'])['name']
#             else:
#                 max_overall_personality = None

#             # Check if there's only one personality with a count of 1 across all responses
#             is_multiple_personalities = len(all_personalities_count) > 1 and all(
#                 personality['total_count'] == 1 for personality in all_personalities_count
#             )

#             for response in user_responses:
#                 personalities_count = response.choice.personalities.values('name').annotate(count=Count('name'))

#                 # Check if personalities_count is not empty before finding the maximum count
#                 if personalities_count:
#                     max_count = max(personalities_count, key=lambda x: x['count'])['count']
#                 else:
#                     max_count = 0

#                 # Include all personalities if each has a count of 1
#                 all_personalities = [personality['name'] for personality in personalities_count if personality['count'] == 1]

#                 response_data.append({
#                     'user': user,
#                     'question': response.choice.question.text,
#                     'max_personality': f"{max_count} {max(personalities_count, key=lambda x: x['count'])['name']}" if max_count > 1 else None,
#                     'all_personalities': all_personalities if len(all_personalities) == len(personalities_count) else None,
#                     'max_overall_personality': "You have multiple personalities." if is_multiple_personalities else f"{max_overall_personality} (Overall)" if max_overall_personality else None,
#                 })

#         context['response_data'] = response_data
#         return context




class MaxOverallPersonalityView(View):
    template_name = 'yourpersonality.html'

    def get(self, request, candidat_id):
        user_responses = Response.objects.filter(candidat__id=candidat_id)
        candidat = get_object_or_404(Candidat, id=candidat_id)

        # Filter and get the principal personality
        principal_personality_data = Personality.objects.filter(
            choice__response__in=user_responses
        ).values('name', 'description').annotate(total_count=Count('name')).order_by(F('total_count').desc()).first()

        principal_personality = {
            'name': principal_personality_data['name'],
            'description': principal_personality_data['description']
        } if principal_personality_data else None

        # Filter and get the secondary personalities
        secondary_personalities_data = Personality.objects.filter(
            choice__response__in=user_responses
        ).values('name', 'description').annotate(total_count=Count('name')).order_by(F('total_count').desc())[1:3]

        secondary_personalities = []
        for personality_data in secondary_personalities_data:
            personality = {
                'name': personality_data['name'],
                'description': personality_data['description']
            }
            secondary_personalities.append(personality)

        context = {
            'candidat': candidat,
            'principal_personality': principal_personality,
            'secondary_personalities': secondary_personalities,
            'candidat_id': candidat_id,
        }

        return render(request, self.template_name, context)
    def post(self, request, candidat_id):
        # Handle form submission for opinions
        return SubmitOpinionView.as_view()(request)
class SubmitOpinionView(View):
    def post(self, request):
        candidat_id = request.POST.get('candidat_id')
        candidat = get_object_or_404(Candidat, id=candidat_id)

        # Extract data from the form for the principal personality
        principal_personality_name = request.POST.get('principal_personality_name')
        likes_principal = request.POST.get('likes_principal') == 'True'
        dislikes_principal = request.POST.get('dislikes_principal') == 'True'
        comment_principal = request.POST.get('comments_principal')
        type_personality_principal = 'Personnalité principale'

        # Create or update the opinion for the principal personality
        principal_personality_instance = Personality.objects.get(name=principal_personality_name)
        try:
            existing_opinion = Opinion.objects.get(user=candidat, personality=principal_personality_instance)
            existing_opinion.likes = likes_principal
            existing_opinion.dislikes = dislikes_principal
            existing_opinion.comment = comment_principal
            existing_opinion.type_personality = type_personality_principal
            existing_opinion.save()  # Save the existing opinion instance
        except Opinion.DoesNotExist:
            Opinion.objects.create(
                user=candidat,
                personality=principal_personality_instance,
                likes=likes_principal,
                dislikes=dislikes_principal,
                comment=comment_principal,
                type_personality=type_personality_principal
            )

        # Handle opinions for secondary personalities similarly as above
        secondary_personality_names = request.POST.getlist('secondary_personality_name[]')
        for secondary_personality_name in secondary_personality_names:
            likes_secondary = request.POST.get(f'likes_{secondary_personality_name}') == 'True'
            dislikes_secondary = request.POST.get(f'dislikes_{secondary_personality_name}') == 'True'
            comment_secondary = request.POST.get(f'comments_{secondary_personality_name}')
            type_personality_secondary = 'Personnalité secondaire'

            secondary_personality_instance = Personality.objects.get(name=secondary_personality_name)
            try:
                existing_opinion = Opinion.objects.get(user=candidat, personality=secondary_personality_instance)
                existing_opinion.likes = likes_secondary
                existing_opinion.dislikes = dislikes_secondary
                existing_opinion.comment = comment_secondary
                existing_opinion.type_personality = type_personality_secondary
                existing_opinion.save()  # Save the existing opinion instance
            except Opinion.DoesNotExist:
                Opinion.objects.create(
                    user=candidat,
                    personality=secondary_personality_instance,
                    likes=likes_secondary,
                    dislikes=dislikes_secondary,
                    comment=comment_secondary,
                    type_personality=type_personality_secondary
                )

        return redirect('TestPersonality:test')
def register_student(request):
    if request.method == 'POST':
        form = EtudiantsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            if Support.objects.filter(name=name).exists():
                student = Support.objects.get(name=name)
                if student.support:
                    return redirect('TestPersonality:ajouter_page')
                else:
                    return redirect('TestPersonality:error')
            else:
                student = form.save(commit=False)
                student.support = False  
                student.save()
                return redirect('TestPersonality:error')  
    else:
        form = EtudiantsForm()

    return render(request, 'register_student.html', {'form': form})
# class SaveOpinionsView(View):
#     def post(self, request):
#         form = PersonalityOpinionForm(request.POST)
#         if form.is_valid():
#             candidat_id = form.cleaned_data['candidat_id']

#             for index, personality in enumerate(Personality.objects.all(), start=1):
#                 liked = form.cleaned_data[f'personality_{index}_liked']
#                 comment = form.cleaned_data[f'comment_{personality.name.lower()}']

#                 if liked:
#                     PersonalityOpinion.objects.create(
#                         candidat_id=candidat_id,
#                         personality_name=personality.name,
#                         liked=True,
#                         comment=comment
#                     )
#                 else : 
#                     PersonalityOpinion.objects.create(
#                         candidat_id=candidat_id,
#                         personality_name=personality.name,
#                         liked=False,
#                         comment=comment
#                     )

#             return JsonResponse({'success': True})
#         else:
#             return JsonResponse({'error': 'Form is not valid'})
    
# class RegisterOpinionView(View):
#     template_name = 'yourpersonality.html'

#     def get(self, request):
#         form = PersonalityOpinionForm()
#         return render(request, self.template_name, {'form': form})

#     def post(self, request):
#         form = PersonalityOpinionForm(request.POST)
#         if form.is_valid():
#             candidat_id = request.POST.get('candidat_id')  # Use POST data to get candidat_id
#             if candidat_id:
#                 # Get the Candidat instance
#                 candidat = get_object_or_404(Candidat, id=candidat_id)
#                 # Loop through submitted data for each personality
#                 for personality, type_personality in zip(request.POST.getlist('personalities[]'), request.POST.getlist('type_personality[]')):
#                     # Create PersonalityOpinion instance
#                     opinion = form.save(commit=False)
#                     opinion.user = candidat
#                     opinion.personality = personality
#                     opinion.type_personality = type_personality
#                     opinion.save()
#                 return redirect('votre_profile_app:end')  # Redirect to a success page
#             else:
#                 return redirect('error_url')  # Redirect to an error page if candidat_id is not available
#         else:
#             return render(request, self.template_name, {'form': form})
   

# class StatisticsView(View):
#     template_name = 'statistics.html'

#     def get(self, request):
#         # Calculate the most common personality overall
#         most_common_personality = Personality.objects.annotate(num_responses=Count('choice__response')).order_by('-num_responses').first()

#         # Calculate the distribution of personalities among users
#         personality_distribution = Candidat.objects.annotate(num_personality=Count('response__choice__personalities')).values('username', 'num_personality')
        
#         total_responses = Response.objects.count()
#         personality_percentage = Personality.objects.annotate(percentage=Count('choice__response') * 100.0 / total_responses).values('name', 'percentage')
#         total_responses_per_type = Candidat.objects.annotate(
#             total_responses=Count('response')
#         ).values('etudiant', 'enactivite', 'chomage', 'total_responses')

#         print( "that i" ,total_responses_per_type)
#         total_responses_count = total_responses_per_type[0]['total_responses']
#         etudiant_percentage = F('etudiant') * 100.0 / total_responses_count
#         enactivite_percentage = F('enactivite') * 100.0 / total_responses_count
#         chomage_percentage = F('chomage') * 100.0 / total_responses_count
    

#         context = {
#             'most_common_personality': most_common_personality,
#             'personality_distribution': personality_distribution,
#             'personality_percentage': personality_percentage,
#             'etudiant_percentage': etudiant_percentage,
#             'enactivite_percentage': enactivite_percentage,
#             'chomage_percentage': chomage_percentage,
#         }

#         return render(request, self.template_name, context)
# class MerciView(View):
#     def post(self, request, candidat_id):
#         candidat = get_object_or_404(Candidat, id=candidat_id)
#         personalities = request.POST.getlist('personalities')
#         likes = request.POST.getlist('likes')
#         comments = request.POST.getlist('comments')

#         for personality, like, comment in zip(personalities, likes, comments):
#             Opinion.objects.create(
#                 user=candidat,
#                 personality=Personality.objects.get(name=personality),
#                 likes=like == 'yes',
#                 comment=comment
#             )

#         return redirect('max_overall_personality', candidat_id=candidat_id)
# class DashboardStatisticsView(TemplateView):
#     template_name = 'statistics.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
        
#         opinions = Opinion.objects.all()
#         total_opinions_count = opinions.count()

#         # Calculate percentage of candidates who like each personality
#         personalities = Personality.objects.all()
#         personality_likes_percentages = {}

#         for personality in personalities:
#             personality_likes_count = opinions.filter(personality=personality, likes=True).count()
#             personality_likes_percentage = (personality_likes_count / total_opinions_count) * 100
#             personality_likes_percentages[personality.name] = personality_likes_percentage

#         context['personality_likes_percentages'] = personality_likes_percentages

#         # Calculate likes percentage for principal personality
#         principal_personality = context.get('principal_personality')  # Get principal personality from context
#         if principal_personality:
#             principal_personality_likes_percentage = personality_likes_percentages.get(principal_personality, 0)
#         else:
#             principal_personality_likes_percentage = 0
#         context['principal_personality_likes_percentage'] = principal_personality_likes_percentage

#         # Calculate likes percentage for secondary personalities
#         secondary_personalities = context.get('secondary_personalities')  # Get secondary personalities from context
#         secondary_personality1_likes_percentage = personality_likes_percentages.get(secondary_personalities[0], 0) if secondary_personalities else 0
#         secondary_personality2_likes_percentage = personality_likes_percentages.get(secondary_personalities[1], 0) if secondary_personalities else 0
#         context['secondary_personality1_likes_percentage'] = secondary_personality1_likes_percentage
#         context['secondary_personality2_likes_percentage'] = secondary_personality2_likes_percentage

#         return context
    
# class PersonalityStatsView(View):
#     def get(self, request):
#         # Nombre total de candidats
#         total_candidates = Candidat.objects.count()
#         etudiant_candidates = Candidat.objects.filter(etudiant=True).count()
#         enactivite_candidates = Candidat.objects.filter(enactivite=True).count()
#         chomage_candidates = Candidat.objects.filter(chomage=True).count()
#         opinions = Opinion.objects.all()
#         # Récupérer les opinions likées
#         liked_opinions = Opinion.objects.filter(likes=True)

#         # Compter les types de personnalité likés
#         liked_personality_types = liked_opinions.values('type_personality').annotate(total_likes=Count('type_personality'))

#         # Calculer le pourcentage pour chaque type de personnalité liké
#         personality_stats = []
#         for personality_type in liked_personality_types:
#             count_likes = personality_type['total_likes']
#             percentage = (count_likes / total_candidates) * 100
#             personality_stats.append({
#                 'type_personality': personality_type['type_personality'],
#                 'total_likes': count_likes,
#                 'percentage': round(percentage, 2)
#             })

#         context = {
#             'personality_stats': personality_stats,
#             'total_candidates':total_candidates,
#             'etudiant_candidates':etudiant_candidates,
#             'enactivite_candidates':enactivite_candidates,
#             'chomage_candidates':chomage_candidates,
#             'opinions': opinions,
#         }

#         return render(request, 'statistics.html', context)
# def end(request):
#     return render(request, 'end.html')
def likes_by_age(request):
    age_ranges = Candidat.objects.values_list('age_range', flat=True).distinct()
    personalities = Personality.objects.annotate(like_count=Count('opinion')).order_by('-like_count')
    age_likes = {}

    for age_range in age_ranges:
        age_likes[age_range] = {personality.name: Opinion.objects.filter(user__age_range=age_range, personality=personality, likes=True).count() for personality in personalities}

    context = {'age_likes': age_likes}
    return render(request, 'static.html', context)

def likes_by_age_chart(request):
    age_ranges = list(Candidat.objects.values_list('age_range', flat=True).distinct())
    personalities = Personality.objects.all()

    chart_labels = age_ranges
    chart_data = []
    personalities_data = []

    for personality in personalities:
        likes_per_age = [
            Opinion.objects.filter(user__age_range=age_range, personality=personality, likes=True).count()
            for age_range in age_ranges
        ]

        total_likes = Opinion.objects.filter(personality=personality, likes=True).count()
        total_dislikes = Opinion.objects.filter(personality=personality, dislikes=True).count()
        total_opinions = total_likes + total_dislikes

        # Calculate percentage likes and dislikes
        if total_opinions > 0:
            percentage_likes = '{:.2f}%'.format((total_likes / total_opinions) * 100)
            percentage_dislikes = '{:.2f}%'.format((total_dislikes / total_opinions) * 100)
        else:
            percentage_likes = 'N/A'
            percentage_dislikes = 'N/A'

        chart_data.append({
            'label': personality.name,
            'data': likes_per_age,
            'backgroundColor': f'rgba({(hash(personality.name) % 256)}, {(hash(personality.name) // 256 % 256)}, {(hash(personality.name) // 256 // 256 % 256)}, 0.2)',
            'borderColor': f'rgba({(hash(personality.name) % 256)}, {(hash(personality.name) // 256 % 256)}, {(hash(personality.name) // 256 // 256 % 256)}, 1)',
            'borderWidth': 1
        })
        personalities_data.append({
            'name': personality.name,
            'total_likes': total_likes,
            'total_dislikes': total_dislikes,
            'percentage_likes': percentage_likes,
            'percentage_dislikes': percentage_dislikes
        })
    opinions = Opinion.objects.all()
    opinions_data = [{
        'user': opinion.user.username,
        'personality': opinion.personality.name,
        'likes': opinion.likes,
        'dislikes': opinion.dislikes,
        'comment': opinion.comment,
        'type_personality': opinion.type_personality
    } for opinion in opinions]

    context = {
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'personalities_data': personalities_data,
        'opinions_data': opinions_data,
        
    }

    return render(request, 'static.html', context)
def ajouter_page(request, id=None):
    if id:
        personality = get_object_or_404(Personality, id=id)
        if request.method == 'POST':
            form = PersonalityForm(request.POST, instance=personality)
            if form.is_valid():
                form.save()
                return redirect('TestPersonality:ajouter_page')
        else:
            form = PersonalityForm(instance=personality)
    else:
        if request.method == 'POST':
            form = PersonalityForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('TestPersonality:ajouter_page')
        else:
            form = PersonalityForm()

    personalities = Personality.objects.all()
    return render(request, 'ajouter.html', {'form': form, 'personalities': personalities, 'edit_id': id})

def ajouter_quest(request, id=None):
    if id:
        question = get_object_or_404(Question, id=id)
        if request.method == 'POST':
            form = QuestionForm(request.POST, instance=question)
            if form.is_valid():
                form.save()
                return redirect('TestPersonality:ajouter_quest')
        else:
            form = QuestionForm(instance=question)
    else:
        if request.method == 'POST':
            form = QuestionForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('TestPersonality:ajouter_quest')
        else:
            form = QuestionForm()

    questiones = Question.objects.all()
    return render(request, 'ajouterqest.html', {'form': form, 'questiones': questiones, 'edit_id': id})
def ajouter_choice(request, id=None):
    if id:
        choice = get_object_or_404(Choice, id=id)
        if request.method == 'POST':
            form = ChoiceForm(request.POST, instance=choice)
            if form.is_valid():
                form.save()
                return redirect('TestPersonality:ajouter_choice')
        else:
            form = ChoiceForm(instance=choice)
    else:
        if request.method == 'POST':
            form = ChoiceForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('TestPersonality:ajouter_choice')
        else:
            form = ChoiceForm()

    choices = Choice.objects.all()
    return render(request, 'ajouterchoice.html', {'form': form, 'choices': choices, 'edit_id': id})

def error_page(request):
    return render(request, 'error.html')



