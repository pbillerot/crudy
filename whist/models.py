""" 
    Modèles 
"""
from django.db import models

class WhistPartie(models.Model):
    """ Les parties """
    name = models.CharField(max_length=50, blank=False
                            , verbose_name='Nom de la partie'
                            , help_text="Le nom de la partie devra être unique"
                            )
    date = models.DateField(auto_now_add=True, auto_now=False, verbose_name="Date de la partie")
    jeu = models.IntegerField(default=0, verbose_name='Nombre de jeux (de tours) de la partie')

    def __str__(self):
        return self.name

    class Meta:
        """ meta """
        verbose_name = "Partie"
        verbose_name_plural = "Parties"

    def save(self, *args, **kwargs):
        """ Création des lignes de jeu pour chaque joueur dans WhistJeu """

        jeux = WhistJeu.objects.filter(partie_id=self.id)
        qjeu = 0
        for jeu in jeux:
            if jeu.jeu > qjeu:
                qjeu = jeu.jeu

        if qjeu < self.jeu:
            # nouveau jeu
            participants = WhistParticipant.objects.filter(partie_id=self.id)
            for participant in participants.iterator():
                for jj in range(qjeu+1, self.jeu + 1):
                    jeu = WhistJeu(partie_id=participant.partie_id, joueur_id=participant.joueur_id, jeu=jj)
                    super(WhistJeu, jeu).save()
        # suppression des jeux créés en trop
        jeux = WhistJeu.objects.filter(partie_id=self.id, jeu__gt=self.jeu)
        if jeux.exists():
            for jeu in jeux.iterator():
                jeu.delete()

        super(WhistPartie, self).save(*args, **kwargs)

class WhistJoueur(models.Model):
    """ Les joueurs """
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
    partie = models.ForeignKey(WhistPartie, on_delete=models.CASCADE, verbose_name="Partie")
    joueur = models.ForeignKey(WhistJoueur, on_delete=models.CASCADE, verbose_name="Joueur")
    score = models.IntegerField(default=0)

    def __str__(self):
        return "{0} participe à la partie {1}".format(self.joueur, self.partie)

    class Meta:
        """ meta """
        verbose_name = "Participant"
        verbose_name_plural = "Participants"

class WhistJeu(models.Model):
    """ Les jeux d'une partie """
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
        super(WhistJeu, self).save(*args, **kwargs)
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
