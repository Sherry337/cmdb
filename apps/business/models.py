from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class Products(models.Model):
    product_name = models.CharField("产品名",db_column='product_name',db_index = True,max_length=255,help_text="产品名")
    description  = models.CharField("描述",db_column='description',null=True,max_length=255,help_text="描述")
    user         = models.ManyToManyField(User, verbose_name="产品负责人", related_name="user", help_text="产品负责人")


    def __str__(self):
        return self.product_name

    class Meta:
        db_table = 'zto_products'
        # permissions = (
        #     ("view_products", "can view products"),
        # )
        ordering = ["id"]