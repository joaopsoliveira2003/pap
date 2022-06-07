from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

Group.objects.get_or_create(name='admin')
Group.objects.get_or_create(name='user')

class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True)
    image = models.ImageField(null=True)

    class Meta:
        ordering = ['user']
        verbose_name = "Perfil"
        verbose_name_plural = "Perfils"

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user=instance)
        if User.objects.count() == 1:
            instance.groups.add(Group.objects.get(name='admin'))
        else:
            instance.groups.add(Group.objects.get(name='user'))

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class ticketmodel(models.Model):
    subject = models.TextField()
    gravity = models.TextField()
    message = models.TextField()
    status = models.TextField(default='open')
    response = models.TextField(null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, related_name='user')
    technician = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, related_name='technician')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"

    def __str__(self):
        return self.message


class contactmodel(models.Model):
    name = models.TextField()
    email = models.EmailField()
    subject = models.TextField()
    message = models.TextField()
    status = models.TextField(default='unread')
    response = models.TextField(null=True)
    technician = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"

    def __str__(self):
        return self.name

class filemodel(models.Model):
    name = models.TextField()
    description = models.TextField()
    file = models.FileField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
        verbose_name = "Ficheiro"
        verbose_name_plural = "Ficheiros"

    def __str__(self):
        return self.name