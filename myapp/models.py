from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Tablas para la base de datos de condominio


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

    def __str__(self):
        return f"{self.nro}"


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

    def __str__(self):
        return f"{self.user.username} - {self.casa.nro if self.casa else 'Sin casa'}"


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
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.placa} - {self.tipo} - {self.color}"


class AreaComun(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    horario_apertura = models.TimeField(default="08:00:00")
    horario_cierre = models.TimeField(default="22:00:00")
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} - {self.horario_apertura}/{self.horario_cierre} - {self.costo}bs/hora"


class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    area_comun = models.ForeignKey(AreaComun, on_delete=models.CASCADE)
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

    def __str__(self):
        return f"{self.usuario.username} - {self.area_comun.nombre} - {self.fecha}"


class Multa(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
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

    def __str__(self):
        return f"{self.usuario.username} - {self.monto} - {self.estado_pago}"


class Extranjero(models.Model):
    ci = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.ci} - {self.nombre}"


class IngresoSalida(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    extranjero = models.ForeignKey(
        Extranjero, on_delete=models.CASCADE, null=True, blank=True
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

    def __str__(self):
        return f"{self.usuario.username if not self.es_extranjero else self.extranjero.nombre} - {self.fecha} - {self.tipo} - {self.modo} - {'es extranjero' if self.es_extranjero else 'no es extranjero'}"
