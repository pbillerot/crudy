""" 
    Modèles 
"""
from django.db import models
from django.db.models.signals import post_delete
from django.shortcuts import get_object_or_404

class WhistPartie(models.Model):
    """ Les parties """
    objects = models.Manager()
    name = models.CharField(max_length=50, blank=False
                            , verbose_name='Nom de la partie'
                            , help_text="Le nom de la partie devra être unique"
                           )
    date = models.DateField(auto_now_add=True, auto_now=False, verbose_name="Date de la partie")
    cartes = models.IntegerField(default=0,
                                 verbose_name='Nombre de cartes max / joueur',
                                 help_text="Nombre de cartes maximum par joueurs qui seront distribuées")
    jeu = models.IntegerField(default=0, verbose_name="n° du jeu en cours")

    def __str__(self):
        return self.name

    class Meta:
        """ meta """
        verbose_name = "Partie"
        verbose_name_plural = "Parties"

class WhistJoueur(models.Model):
    """ Les joueurs """
    objects = models.Manager()
    pseudo = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    # participants = models.ManyToManyField(WhistPartie, through='WhistParticipant')
    # jeux = models.ManyToManyField(WhistPartie, through='WhistJeu')

    def __str__(self):
        return self.pseudo

    class Meta:
        """ meta """
        verbose_name = "Joueur"
        verbose_name_plural = "Joueurs"

class WhistParticipant(models.Model):
    """ Les participants à une partie """
    objects = models.Manager()
    partie = models.ForeignKey(WhistPartie, on_delete=models.CASCADE, verbose_name="Partie")
    joueur = models.ForeignKey(WhistJoueur, on_delete=models.CASCADE, verbose_name="Joueur")
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
            count_participants = WhistParticipant.objects.all()\
                .filter(partie__exact=self.partie).count()
            self.order = (count_participants) * 2
        super().save(*args, **kwargs)

    def compute_order(self):
        """ recalcule de l'ordre """
        participants = WhistParticipant.objects.all()\
        .filter(partie__exact=self.partie).order_by("order")
        order = 0
        for participant in participants:
            participant.order = order
            super(WhistParticipant, participant).save()
            order += 2

class WhistJeu(models.Model):
    """ Les jeux d'une partie """
    objects = models.Manager()
    participant = models.ForeignKey(WhistParticipant, on_delete=models.CASCADE)
    # partie = models.ForeignKey(WhistPartie, on_delete=models.CASCADE)
    # joueur = models.ForeignKey(WhistJoueur, on_delete=models.CASCADE)
    jeu = models.IntegerField(default=0, verbose_name='N° du tour')
    carte = models.IntegerField(default=0, verbose_name='Nbre de cartes')
    pari = models.IntegerField(default=0, verbose_name='Pari')
    real = models.IntegerField(default=0, verbose_name='Réalisé')
    points = models.IntegerField(default=0, verbose_name='Points')
    score = models.IntegerField(default=0, verbose_name='Score')
    donneur = models.IntegerField(default=0)

    def __str__(self):
        # return "{0}_{1}_{2}".format(self.partie, self.joueur, self.jeu)
        return "{0}_{1}".format(self.participant, self.jeu)

    class Meta:
        """ meta """
        verbose_name = "Jeu"
        verbose_name_plural = "Jeux"

    def create_jeux(self, ctx):
        """ Création des jeux de la partie """
        # suppression des jeux 
        WhistJeu.objects.all().filter(participant__partie__id=ctx["folder_id"]).delete()

        partie = get_object_or_404(WhistPartie, id=ctx["folder_id"])
        icarte = 0
        for ijeu in range(0, partie.cartes * 2):
            # calcul du n° du tour et du nombre de carte du tour
            if ijeu < partie.cartes:
                # 1ère moitié de la partie, nbre croissant de cartes
                icarte += 1
            else:
                # 2ème moitié, nbre décroissant de cartes
                if icarte != ijeu:
                    # 2 fois le m nbre de carte à la moitié de la partie
                    icarte -= 1

            # création des lignes de jeux
            ijeu += 1

            # Création d'une ligne par participant
            participants = WhistParticipant.objects.all().filter(partie__id=ctx["folder_id"])
            for participant in participants:
                jeu = WhistJeu(participant=participant, jeu=ijeu, carte=icarte)
                jeu.save()

def post_delete_whist(sender, instance, **kwargs):
    """ traitements suite à la suppression d'un enregistrement """
    if isinstance(instance, (WhistParticipant,)):
        instance.compute_order()

post_delete.connect(post_delete_whist)
