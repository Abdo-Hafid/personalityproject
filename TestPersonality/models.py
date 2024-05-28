from django.db import models

# Create your models here.

    
class Support(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100 , null = False)
    support = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Personality(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=4000 , null = True)

    def __str__(self):
        return self.name
    def get_principal_personality_likes(self):
        return self.opinion_set.filter(type_personality='Personnalité principale', likes=True).count()

    get_principal_personality_likes.short_description = 'Number of Likes for Principal Personality'

class Question(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text

class Choice(models.Model):
    text = models.CharField(max_length=100)
    personalities = models.ManyToManyField(Personality)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
    
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
    ('30-40', '40-40'),
    ('40-50', '40-50'),
    ('>50', '>50'),
)
class Candidat(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=200, blank=True, null=True)
    genre = models.CharField(max_length=20, choices=(('male', 'Male'), ('female', 'Female')), null=True)
    age_range = models.CharField(max_length=10, choices=AGE_RANGES, null=True)
    categorie_socioprofessionnelle = models.CharField(
        max_length=50,
        choices=(
            ('etudiant', 'Étudiant'),
            ('employe', 'Employé'),
            ('cadre', 'Cadre'),
            ('travailleur_independant', 'Travailleur indépendant'),
            ('sans_emploi', 'Sans emploi'),
            ('autre', 'Autre'),
        ),
        null=True,
    )
    autre_categorie = models.CharField(max_length=100,blank=True, null=True)
    ville = models.CharField(max_length=50, choices=MOROCCAN_CITIES, null=True)

    def __str__(self):
        return self.username
    

class Response(models.Model):
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        personalities_str = ", ".join([personality.name for personality in self.choice.personalities.all()])
        return f"{self.candidate.username}'s response to {self.choice.question.text} with personalities: {personalities_str}"
    
class Percandidat(models.Model):
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE)
    personalite = models.ForeignKey(Personality, on_delete=models.CASCADE, null=True, related_name='percandidat_personalite_pyn')
    pyn = models.BooleanField(default=False)
    commantaire = models.CharField(max_length=400, null=True)
    personalite_sa = models.ForeignKey(Personality, on_delete=models.CASCADE, null=True, related_name='percandidat_personalite_personalite_sa')
    psayn = models.BooleanField(default=False)
    commantaire_sa = models.CharField(max_length=400, null=True)
    personalite_sb = models.ForeignKey(Personality, on_delete=models.CASCADE, null=True, related_name='percandidat_personalite_personalite_sb')
    psbyn = models.BooleanField(default=False)
    commantaire_sb = models.CharField(max_length=400, null=True)

class Opinion(models.Model):
    user = models.ForeignKey(Candidat, on_delete=models.CASCADE)
    personality = models.ForeignKey(Personality, on_delete=models.CASCADE)
    likes = models.BooleanField(default=False)
    dislikes = models.BooleanField(default=False)  
    comment = models.TextField(blank=True, null=True) 
    type_personality = models.CharField(max_length=50,null=True)
    def __str__(self):
        return f"{self.user.username}'s opinion on {self.personality.name}" 


class PersonalityOpinion(models.Model):
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE)
    personality_name = models.CharField(max_length=100)
    liked = models.BooleanField()
    comment = models.TextField()
    type_personality = models.CharField(max_length=50,null=True)
    def __str__(self):
        return f"{self.candidat}'s opinion on {self.personality_name}"



        
    

