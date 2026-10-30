from django.core.management.base import BaseCommand

from api.models import Blog, Comment, User


class Command(BaseCommand):
    help = "Remplit la base de données avec des utilisateurs, des blogs et des commentaires de démo."

    def handle(self, *args, **kwargs):
        self.stdout.write("Création des données de démo...")

        # 1. Création des utilisateurs démo
        admin_user, created = User.objects.get_or_create(
            username="admin_devsecops",
            defaults={
                "email": "admin@tdev2026.tg",
                "first_name": "Ilem",
                "last_name": "Nelson",
                "is_staff": True,
                "is_superuser": True,
                "is_verified": True,
            },
        )
        if created:
            admin_user.set_password("AdminSecure2026!")
            admin_user.save()
            self.stdout.write(
                self.style.SUCCESS(f"Utilisateur créé : {admin_user.username}")
            )

        normal_user, created = User.objects.get_or_create(
            username="participant_demo",
            defaults={
                "email": "participant@tdev2026.tg",
                "first_name": "Visiteur",
                "last_name": "Djanta",
                "is_verified": True,
            },
        )
        if created:
            normal_user.set_password("Password123!")
            normal_user.save()
            self.stdout.write(
                self.style.SUCCESS(f"Utilisateur créé : {normal_user.username}")
            )

        # 2. Création de blogs de démo
        blog1, created = Blog.objects.get_or_create(
            title="Sécuriser ses pipelines CI/CD en 2026",
            defaults={
                "content": "Le DevSecOps ne se résume pas à installer des outils. C'est une culture de la sécurité intégrée dès la conception du code.",
                "author": admin_user,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Blog créé : {blog1.title}"))

        blog2, created = Blog.objects.get_or_create(
            title="Attention aux failles générées par les IA",
            defaults={
                "content": "Les assistants IA rédigent du code rapidement, mais introduisent parfois des failles subtiles (Injections, IDs cachés, etc.).",
                "author": admin_user,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Blog créé : {blog2.title}"))

        # 3. Création de commentaires de démo
        if not Comment.objects.exists():
            Comment.objects.create(
                blog=blog1,
                author=normal_user,
                content="Super article ! Hâte de voir la démo pratique avec Semgrep et ZAP.",
            )
            Comment.objects.create(
                blog=blog2,
                author=normal_user,
                content="Exactement le genre de problématique qu’on rencontre en entreprise.",
            )
            self.stdout.write(
                self.style.SUCCESS("Commentaires de démo créés avec succès !")
            )

        self.stdout.write(
            self.style.SUCCESS("Base de données initialisée avec brio ! 🚀")
        )
