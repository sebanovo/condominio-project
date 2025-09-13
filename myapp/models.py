from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Casa(models.Model):
    nro = models.CharField(max_length=10, unique=True)
    categoria = models.CharField(
        max_length=50,
        choices=[
            ("standard", "Standard"),
            ("premium", "Premium"),
            ("vip", "VIP"),
        ],
    )
    capacidad = models.IntegerField(
        validators=[MinValueValidator(1)]  # minimo 1 persona
    )


class Perfil(models.Model):
    telefono = models.IntegerField(unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    casa = models.ForeignKey(
        Casa,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="residentes",
    )
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)


class Vehiculo(models.Model):
    placa = models.CharField(max_length=10)
    tipo = models.CharField(
        max_length=50,
        choices=[
            ("auto", "Automóvil"),
            ("moto", "Motocicleta"),
            ("bici", "Bicicleta"),
            ("camion", "Camión"),
        ],
    )
    color = models.CharField(max_length=50)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)


class AreaComun(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    horario = models.CharField(max_length=100)
    costo = models.DecimalField(max_digits=10, decimal_places=2)


class Reserva(models.Model):
    ESTADO_PAGO_CHOICES = [
        ("Pendiente"),
        ("Pagado"),
        ("Cancelado"),
    ]
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_area = models.ForeignKey(AreaComun, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    estado_pago = models.CharField(
        max_length=20,
        choices=[
            ("pendiente", "Pendiente"),
            ("pagado", "Pagado"),
            ("cancelado", "Cancelado"),
        ],
    )
    metodo_pago = models.CharField(
        max_length=20,
        choices=[
            ("qr", "QR"),
            ("tarjeta", "Tarjeta"),
            ("efectivo", "Efectivo"),
            ("transferencia", "Transferencia"),
        ],
    )


class Multa(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descripcion = models.TextField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    estado_pago = models.CharField(
        max_length=20,
        choices=[
            ("pendiente", "Pendiente"),
            ("pagada", "Pagada"),
            ("perdonada", "Perdonada"),
        ],
    )
    metodo_pago = models.CharField(
        max_length=20,
        choices=[
            ("efectivo", "Efectivo"),
            ("transferencia", "Transferencia"),
            ("descuento", "Descuento en cuota"),
        ],
    )


class IngresoSalida(models.Model):
    id_usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    fecha = models.DateTimeField()
    tipo = models.CharField(
        max_length=10,
        choices=[
            ("entrada", "Entrada"),
            ("salida", "Salida"),
        ],
    )
    modo = models.CharField(
        max_length=20,
        choices=[
            ("pie", "A pie"),
            ("auto", "Auto"),
            ("moto", "Moto"),
            ("bici", "Bicicleta"),
            ("otro", "Otro"),
        ],
    )
    es_extranjero = models.BooleanField(default=False)


class Extranjero(models.Model):
    ci = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
