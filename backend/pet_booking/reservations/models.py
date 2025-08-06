from django.db import models
from users.models import Users

class Reservation_grooming(models.Model):
    reservation_id = models.CharField(max_length=20, unique=True)
    store_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=20)
    user_phone = models.CharField(max_length=15)
    grooming_services_name = models.IntegerField()
    pet_name = models.CharField(max_length=10)
    pet_breed = models.CharField(max_length=10)
    pick_up_service = models.BooleanField()
    reservation_time = models.DateTimeField()
    customer_note = models.TextField(blank=True, default='')
    store_note = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reservation_grooming'

    def __str__(self):
        return self.reservation_id


class Grooming_schedules(models.Model):
    reservation_grooming_id = models.ForeignKey(
        Reservation_grooming,
        on_delete = models.CASCADE,
        db_column = 'reservation_grooming_id'
    )

    date = models.DateField()
    unavailable_time = models.TimeField()

    class Meta:
        db_table = 'grooming_schedules'

    def __str__(self):
        return f'booking record for {self.reservation_grooming_id}'


class Reservation_boarding(models.Model):
    reservation_id = models.CharField(max_length=20, unique=True)
    store_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=20)
    user_phone = models.CharField(max_length=15)
    pet_name = models.CharField(max_length=10)
    room_type = models.CharField(max_length=20)
    checkin_date = models.DateTimeField()
    checkout_date = models.DateTimeField()
    customer_note = models.TextField(blank=True, default='')
    store_note = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reservation_boarding'

    def __str__(self):
        return self.reservation_id

class Boarding_schedules(models.Model):
    reservation_boarding_id = models.ForeignKey(
        Reservation_boarding,
        on_delete = models.CASCADE,
        db_column = 'reservation_boarding_id'
    )

    room_type = models.CharField(max_length=20)
    unavailable_time = models.DateTimeField(auto_now_add=True)


class Orders(models.Model):
    reservation_grooming = models.ForeignKey(
        Reservation_grooming,
        on_delete = models.CASCADE,
        db_column = 'reservation_grooming_id',
        null = True,
        blank = True
    )

    reservation_boarding = models.ForeignKey(
        Reservation_boarding,
        on_delete = models.CASCADE,
        db_column = 'reservation_boarding_id',
        null = True,
        blank = True
    )

    user_id = models.ForeignKey(
        Users,
        on_delete = models.CASCADE,
        db_column = 'user_id'
    )

    total_price = models.IntegerField()

    class Meta:
        db_table = 'orders'

    def __str__(self):
        service_type = "grooming" if self.reservation_grooming else "boarding"
        return f'Order {self.id} - {service_type} (${self.total_price})'