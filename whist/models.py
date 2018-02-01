""" 
    Modèles 
"""
from django.db import models
from django.db.models.signals import post_delete

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
    carte = models.IntegerField(default=0, verbose_name="Nombre de carte du jeu")
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

    def __str__(self):
        return "{0} participe à la partie {1}".format(self.joueur, self.partie)

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
        self.compute_order()

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
    partie = models.ForeignKey(WhistPartie, on_delete=models.CASCADE)
    joueur = models.ForeignKey(WhistJoueur, on_delete=models.CASCADE)
    jeu = models.IntegerField(default=0, verbose_name='Jeu')
    pari = models.IntegerField(default=0, verbose_name='Pari')
    real = models.IntegerField(default=0, verbose_name='Réalisé')
    points = models.IntegerField(default=0, verbose_name='Points')
    score = models.IntegerField(default=0, verbose_name='Score')

    def __str__(self):
        return "{0}_{1}_{2}".format(self.partie, self.joueur, self.jeu)

    class Meta:
        """ meta """
        verbose_name = "Jeu"
        verbose_name_plural = "Jeux"

    def save(self, *args, **kwargs):
        """ Calcul des points en fonction du pari et du réalisé """
        super().save(*args, **kwargs)
        jeux = WhistJeu.objects.filter(partie=self.partie, jeu=self.jeu)
        for jeu in jeux.iterator():
            # print("{} {} {}".format(jeu.joueur, jeu.pari, jeu.real))
            if jeu.pari != jeu.real:
                jeu.points = -10
            else:
                jeu.points = 10 + jeu.pari * 2
            super(WhistJeu, jeu).save()
        # calcul des points et score
        participants = WhistParticipant.objects.filter(partie=self.partie)
        for participant in participants:
            jeux = WhistJeu.objects.filter(partie=self.partie, joueur=participant.joueur, jeu__lte=self.jeu).order_by('jeu')
            for jeu in jeux.iterator():
                # print("{} {} {}".format(jeu.joueur, jeu.pari, jeu.real))
                if jeu.pari != jeu.real:
                    jeu.points = -10
                else:
                    jeu.points = 10 + jeu.pari * 2
                participant.score += jeu.points
            # mise à jour du score du participant
            participant.save()
            for jeu in jeux.iterator():
                # print("{} {} {}".format(jeu.joueur, jeu.pari, jeu.real))
                # on reporte le score sur les jeux de la partie
                if jeu.pari != jeu.real:
                    jeu.points = -10
                else:
                    jeu.points = 10 + jeu.pari * 2
                jeu.score = participant.score
                super(WhistJeu, jeu).save()

            super(WhistJeu, jeu).save()

def post_delete_whist(sender, instance, **kwargs):
    """ traitements suite à la suppression d'un enregistrement """
    if isinstance(instance, (WhistParticipant,)):
        instance.compute_order()

post_delete.connect(post_delete_whist)
