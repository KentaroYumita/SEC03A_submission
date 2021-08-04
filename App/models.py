from django.db import models

# Create your models here.
class Guest(models.Model):
    name = models.CharField(max_length=20)
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Table(models.Model):
    max_sheet = models.IntegerField()
    def __str__(self):
        return f"This table accept up to {self.max_sheet}"

class Reservation(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    number = models.IntegerField()
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    timeslot = models.DateTimeField()

    def __str__(self):
        people="people" if self.number>1 else "person"
        return f"{self.guest.name}({self.number} {people}) reserved at {self.timeslot}"