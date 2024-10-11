from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Meta:
        db_table = 'mundoalado_user'  # Nombre de tabla personalizado

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='mundoalado_user_groups',  # Cambiar related_name
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='mundoalado_user_permissions',  # Cambiar related_name
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

class Bird(models.Model):
    ESTADOS_CONSERVACION = [
        ('LC', 'Preocupación menor'),
        ('NT', 'Casi amenazado'),
        ('VU', 'Vulnerable'),
        ('EN', 'En peligro'),
        ('CR', 'En peligro crítico'),
        ('EW', 'Extinto en estado silvestre'),
        ('EX', 'Extinto'),
    ]

    nombre_comun = models.CharField(max_length=255)
    nombre_cientifico = models.CharField(max_length=255, unique=True)
    familia = models.CharField(max_length=100)
    habitat = models.TextField()
    distribucion_geografica = models.TextField()
    tamaño = models.FloatField(help_text="Tamaño promedio en centímetros")
    peso = models.FloatField(help_text="Peso promedio en gramos")
    coloracion = models.TextField()
    dieta = models.CharField(max_length=255)
    comportamiento = models.TextField()
    estado_conservacion = models.CharField(max_length=2, choices=ESTADOS_CONSERVACION, default='LC')
    imagen = models.ImageField(upload_to='pajaros/', blank=True, null=True)
    sonido = models.URLField(blank=True, null=True)
    fecha_descubrimiento = models.DateField(blank=True, null=True)
    autoridad = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre_comun
