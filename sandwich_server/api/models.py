from django.db import models


class Bread(models.Model):
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False)
    name = models.CharField(max_length=1500)
    qty = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bread"
        app_label = "api"

    def __str__(self):
        return self.name


class Topping(models.Model):
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False)
    name = models.CharField(max_length=1500)
    qty = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "topping"
        app_label = "api"

    def __str__(self):
        return self.name


class Cheese(models.Model):
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False)
    name = models.CharField(max_length=1500)
    qty = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cheese"
        app_label = "api"

    def __str__(self):
        return self.name


class Sauce(models.Model):
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False)
    name = models.CharField(max_length=1500)
    qty = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sauce"
        app_label = "api"

    def __str__(self):
        return self.name


class Sandwich(models.Model):
    id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False)
    bread = models.ForeignKey(Bread, on_delete=models.SET_NULL, null=True)
    topping = models.ForeignKey(Topping, on_delete=models.SET_NULL, null=True)
    cheese = models.ForeignKey(Cheese, on_delete=models.SET_NULL, null=True)
    sauce = models.ForeignKey(Sauce, on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sandwich"
        app_label = "api"

    def __str__(self):
        return self.id
