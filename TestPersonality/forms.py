from django import forms
from .models import Choice,Candidat,Question,Percandidat,Opinion,PersonalityOpinion,Personality,Support


AGE_RANGES = (
    ('20-30', '20-30'),
    ('30-40', '30-40'),
    ('40-50', '40-50'),
    ('>50', '>50'),
)
CATEGORIE_CHOICES = (
    ('etudiant', 'Étudiant'),
    ('employe', 'Employé'),
    ('cadre', 'Cadre'),
    ('travailleur_independant', 'Travailleur indépendant'),
    ('sans_emploi', 'Sans emploi'),
    ('autre', 'Autre'),
)
class CandidateForm(forms.ModelForm):
    age_range = forms.ChoiceField(choices=AGE_RANGES, widget=forms.RadioSelect)
    categorie_socioprofessionnelle = forms.ChoiceField(choices=CATEGORIE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Candidat
        fields = ['username', 'email', 'genre', 'age_range', 'categorie_socioprofessionnelle', 'autre_categorie', 'ville']
# class OpinionForm(forms.ModelForm):
#     class Meta:
#         model = Percandidat
#         fields = ['candidat', 'personalite', 'pyn', 'commantaire', 'personalite_sa', 'psayn', 'commantaire_sa', 'personalite_sb', 'psbyn', 'commantaire_sb']

# class PersonalityOpinionForm(forms.ModelForm):
#     class Meta:
#         model = Opinion
#         fields = ['likes', 'dislikes', 'comment', 'type_personality'] 
# class OpinionForm(forms.ModelForm):
#     class Meta:
#         model = Opinion
#         fields = ['personality', 'likes', 'comment', 'type_personality']

#        #-----------azga------------- 
class QuestionnaireForm(forms.Form):
    def __init__(self, *args, **kwargs):
        candidat_username = kwargs.pop('candidat_username', None)
        questions = kwargs.pop('questions', None)
        super(QuestionnaireForm, self).__init__(*args, **kwargs)

        if candidat_username:
             self.fields['candidat_username'] = forms.CharField(
                 widget=forms.HiddenInput(),
                 initial=candidat_username
             )

        if questions:
            for question in questions:
                self.fields[f'question_{question.id}'] = forms.ModelChoiceField(
                    queryset=Choice.objects.filter(question=question),
                    widget=forms.RadioSelect,
                    required=True,
                    
                    label=question.text
                )
class EtudiantsForm(forms.ModelForm):
    class Meta:
        model = Support
        fields = ['name', 'password']

class PersonalityForm(forms.ModelForm):
    class Meta:
        model = Personality
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'exampleFormControlInput1', 
                'placeholder': 'Enter name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'id': 'exampleFormControlTextarea1', 
                'rows': 3, 
                'placeholder': 'Enter description'
            }),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control', 
                'id': 'exampleFormControlTextarea1', 
                'rows': 3, 
                'placeholder': 'Enter question'
            }),
        }

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'personalities', 'question']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'personalities': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'question': forms.Select(attrs={'class': 'form-control'}),
        }
