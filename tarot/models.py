""" 
    Modèles 
"""
from django.db import models
from django.db.models.signals import post_delete
from django.shortcuts import get_object_or_404

class TarotPartie(models.Model):
    """ Les parties """
    objects = models.Manager()
    owner = models.CharField(max_length=50, default="inconnu"
                            , verbose_name='Compte'
                            , help_text="Le compte propriétaire"
                           )
    name = models.CharField(max_length=50, blank=False
                            , verbose_name='Nom de la partie'
                            , help_text="Le nom de la partie sera unique"
                           )
    date = models.DateField(auto_now_add=True, auto_now=False, verbose_name="Date de la partie")
    jeu = models.IntegerField(default=0, verbose_name="n° du jeu en cours")

    def __str__(self):
        return self.name

    class Meta:
        """ meta """
        verbose_name = "Partie"
        verbose_name_plural = "Parties"

class TarotJoueur(models.Model):
    """ Les joueurs """
    objects = models.Manager()
    owner = models.CharField(max_length=50, default="inconnu"
                            , verbose_name='Compte'
                            , help_text="Le compte propriétaire"
                           )
    pseudo = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    # participants = models.ManyToManyField(TarotPartie, through='TarotParticipant')
    # jeux = models.ManyToManyField(TarotPartie, through='TarotJeu')

    def __str__(self):
        return self.pseudo

    class Meta:
        """ meta """
        verbose_name = "Joueur"
        verbose_name_plural = "Joueurs"

class TarotParticipant(models.Model):
    """ Les participants à une partie """
    objects = models.Manager()
    partie = models.ForeignKey(TarotPartie, on_delete=models.CASCADE, verbose_name="Partie")
    joueur = models.ForeignKey(TarotJoueur, on_delete=models.CASCADE, verbose_name="Joueur")
    score = models.IntegerField(default=0)
    order = models.IntegerField(default=99)
    donneur = models.IntegerField(default=0)

    def __str__(self):
        return "{0} participe {1}".format(self.joueur, self.partie)

    class Meta:
        """ meta """
        verbose_name = "Participant"
        verbose_name_plural = "Participants"

    def save(self, *args, **kwargs):
        """ Calcul de l'ordre """
        if self.pk is None:
            count_participants = TarotParticipant.objects.all()\
                .filter(partie__exact=self.partie).count()
            self.order = (count_participants) * 2
        super().save(*args, **kwargs)

    def compute_order(self):
        """ recalcule de l'ordre """
        participants = TarotParticipant.objects.all()\
        .filter(partie__exact=self.partie).order_by("order")
        order = 0
        for participant in participants:
            participant.order = order
            super(TarotParticipant, participant).save()
            order += 2

class TarotJeu(models.Model):
    """ Les jeux d'une partie """
    objects = models.Manager()
    participant = models.ForeignKey(TarotParticipant, on_delete=models.CASCADE)
    jeu = models.IntegerField(default=0, verbose_name='N° du tour')
    pari = models.TextField(default="", verbose_name='Contrat')
    real = models.IntegerField(default=0, verbose_name='Réalisé')
    points = models.IntegerField(default=0, verbose_name='Points')
    score = models.IntegerField(default=0, verbose_name='Score')
    medal = models.IntegerField(default=0, verbose_name='Médaille') # Gold Silver Bronze Chocolate
    donneur = models.BooleanField(default=0, verbose_name='Donneur')
    partenaire = models.BooleanField(default=0, verbose_name='Partenaire appelé')
    bouts = models.IntegerField(default=0, verbose_name="Nombre de Bouts")
    primes = models.IntegerField(default=0, verbose_name="Primes")
    ptbout = models.BooleanField(default=False, verbose_name="Petit au bout (10 points)")
    misere1 = models.BooleanField(default=False, verbose_name="Misère d'atout (10 points)")
    misere2 = models.BooleanField(default=False, verbose_name="Misère de tête (10 points)")
    poignee1 = models.BooleanField(default=False, verbose_name='Poignée (20 points)')
    poignee2 = models.BooleanField(default=False, verbose_name='Double Poignée (30 points)')
    poignee3 = models.BooleanField(default=False, verbose_name='Triple Poignée (40 points)')
    grchelem = models.BooleanField(default=False, verbose_name='Grand Chelem annoncé (400 points)')
    gchelem = models.BooleanField(default=False, verbose_name='Grand Chelem non annoncé (200 points)')
    ptchelem = models.BooleanField(default=False, verbose_name='Petit Chelem annoncé (200 points)')
    pchelem = models.BooleanField(default=False, verbose_name='Petit Chelem non annoncé (100 points)')
    gpchelem = models.BooleanField(default=False, verbose_name='Grand Chelem annoncé non réalisé (-200 points)')
    ppchelem = models.BooleanField(default=False, verbose_name='Petit Chelem annoncé non réalisé (-100 points)')

    def __str__(self):
        # return "{0}_{1}_{2}".format(self.partie, self.joueur, self.jeu)
        return "{0}_{1}".format(self.participant, self.jeu)

    class Meta:
        """ meta """
        verbose_name = "Jeu"
        verbose_name_plural = "Jeux"

    def create_jeux(self, crudy):
        """ Création du 1er jeu de la partie """
        # suppression des jeux 
        TarotJeu.objects.all().filter(participant__partie__id=crudy.folder_id).delete()

        partie = get_object_or_404(TarotPartie, id=crudy.folder_id)
        partie.jeu = 1
        partie.save()

        # Création d'une ligne par participant
        participants = TarotParticipant.objects.all().filter(partie__id=crudy.folder_id)
        for participant in participants:
            jeu = TarotJeu(participant=participant, jeu=1, donneur=participant.donneur)
            jeu.save()

def post_delete_tarot(sender, instance, **kwargs):
    """ traitements suite à la suppression d'un enregistrement """
    if isinstance(instance, (TarotParticipant,)):
        instance.compute_order()

post_delete.connect(post_delete_tarot)
