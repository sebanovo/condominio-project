from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    username = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, null=False, blank=False)
    photo = models.TextField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.username} - {self.email}"


class Casa(models.Model):
    nro = models.CharField(max_length=10)
    categoria = models.CharField(max_length=50)
    capacidad = models.IntegerField()
    usuarios = models.ManyToManyField(Usuario, related_name="casas")

    def __str__(self):
        return f"{self.nro} - {self.categoria} - {self.capacidad}"


class Vehiculo(models.Model):
    placa = models.CharField(max_length=10)
    tipo = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.placa} - {self.tipo} - {self.color}"


class AreaComun(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    horario = models.CharField(max_length=100)
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} - {self.horario} - {self.horario}"


class Reserva(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
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
        choices=[("qr", "QR"), ("tarjeta", "Tarjeta"), ("efectivo", "Efectivo")],
    )

    def __str__(self):
        return f"{self.fecha} - {self.estado_pago}"


class Multa(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descripcion = models.TextField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
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
        choices=[("qr", "QR"), ("tarjeta", "Tarjeta"), ("efectivo", "Efectivo")],
    )

    def __str__(self):
        return f"{self.id_usuario} - {self.descripcion} - {self.monto} - {self.estado_pago}"


class Extranjero(models.Model):
    ci = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.ci} - {self.nombre}"


class IngresoSalida(models.Model):
    id_usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, null=True, blank=True
    )
    fecha = models.DateTimeField()
    tipo = models.CharField(
        max_length=10, choices=[("ingreso", "Ingreso"), ("salida", "Salida")]
    )
    modo = models.CharField(
        max_length=20,
        choices=[
            ("pie", "A pie"),
            ("auto", "Auto"),
            ("bici", "Bici"),
            ("moto", "Moto"),
            ("otro", "Otro"),
        ],
    )
    extranjero = models.ForeignKey(
        Extranjero, on_delete=models.CASCADE, null=True, blank=True
    )
    es_extranjero = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.fecha} - {self.tipo} - {self.modo}"
