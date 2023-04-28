from operator import mod
from unicodedata import name
from django.db import models

# Create your models here.
class iron_purchases(models.Model):
    quantity = models.IntegerField()
    pricing = models.FloatField()
    price = models.IntegerField()
    date = models.DateField()
    notes = models.CharField(null=True,blank=True,max_length=255)
    entry_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f'{self.quantity} * {self.pricing} = {self.price}')

class iron_sales(models.Model):
    quantity = models.IntegerField()
    pricing = models.FloatField()
    price = models.IntegerField()
    date = models.DateField()
    notes = models.CharField(null=True,blank=True,max_length=255)
    entry_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f'{self.quantity} * {self.pricing} = {self.price}')
types = [
    ('income', 'income'),
    ('expenses', 'expenses'),
]
class money_box(models.Model):
    box = models.IntegerField(null=True,blank=True)
    income_id = models.ForeignKey('income',null=True,blank=True,default=1,on_delete=models.SET_DEFAULT)
    expenses_id = models.ForeignKey('expenses',null=True,blank=True,default=1,on_delete=models.SET_DEFAULT)
    type = models.CharField(choices=types,max_length=255)
    date = models.DateField()
    notes = models.CharField(null=True,blank=True,max_length=255)
    entry_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.id)


class income(models.Model):
    price = models.IntegerField()
    date = models.DateField()
    account = models.ForeignKey('accounts',on_delete=models.PROTECT)
    operation_id = models.IntegerField(null=True,blank=True)
    notes = models.CharField(null=True,blank=True,max_length=255)
    entry_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f'{self.price} => ({self.account})')



class expenses(models.Model):
    price = models.IntegerField()
    date = models.DateField()
    account = models.ForeignKey('accounts',on_delete=models.PROTECT)
    operation_id = models.IntegerField(null=True,blank=True)
    bio = models.CharField(null=True,blank=True,max_length=255)
    notes = models.CharField(null=True,blank=True,max_length=255)
    entry_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f'{self.price} => ({self.account})')
        

class pistons(models.Model):
    date = models.DateField()
    piston1 = models.IntegerField()
    piston2 = models.IntegerField()
    piston3 = models.IntegerField()
    notes = models.CharField(null=True,blank=True,max_length=255)
    entry_date = models.DateTimeField(auto_now_add=True)
    


    def __str__(self):
        return str(self.date)

class weight_gain(models.Model):
    price = models.IntegerField()
    date = models.DateField()
    notes = models.CharField(null=True,blank=True,max_length=255)
    entry_date = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return str(f'{self.price} => ({self.date})')

class export(models.Model):
    date = models.DateField()
    output = models.IntegerField()
    output_type2 = models.IntegerField(null=True,blank=True)
    weight = models.IntegerField()
    iron_floors = models.IntegerField()
    notes = models.CharField(null=True,blank=True,max_length=255)
    entry_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(f'{self.output} => ({self.date})')
fuel_type = [
    ('fuel', 'fuel'),
    ('fuel_incom', 'fuel_incom'),
]
class fuel_box(models.Model):
    box = models.IntegerField(null=True,blank=True)
    fuel_incom_id = models.ForeignKey('fuel_incom',null=True,blank=True,default=1,on_delete=models.SET_DEFAULT)
    fuel_id = models.ForeignKey('fuel',null=True,blank=True,default=1,on_delete=models.SET_DEFAULT)
    type = models.CharField(choices=fuel_type,max_length=255)
    date = models.DateField()
    notes = models.CharField(null=True,blank=True,max_length=255)
    entry_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.box)

class fuel_incom(models.Model):
    quantity = models.IntegerField()
    date = models.DateField()
    notes = models.CharField(null=True,blank=True,max_length=255)
    entry_date = models.DateTimeField(auto_now_add=True)
    


    def __str__(self):
        return str(f'{self.quantity} => ({self.date})')

class fuel(models.Model):
    quantity = models.IntegerField()
    date = models.DateField()
    account = models.ForeignKey('accounts',on_delete=models.PROTECT)
    notes = models.CharField(null=True,blank=True,max_length=255)
    entry_date = models.DateTimeField(auto_now_add=True)
    


    def __str__(self):
        return str(f'{self.quantity} => ({self.account})')

class accounts(models.Model):
    name = models.CharField(max_length=255)
    use  = models.ManyToManyField('uses')
    notes = models.CharField(null=True,blank=True,max_length=255)
    entry_date = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.name


class uses(models.Model):
    name = models.CharField(max_length=255)
    notes = models.CharField(null=True,blank=True,max_length=255)
    entry_date = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.name