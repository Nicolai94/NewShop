from .models import Product
from django.db.models import Min,Max


def get_filters(request):
    minMaxPrice = Product.objects.aggregate(Min('price'), Max('price'))

    data = {
        'minMaxPrice': minMaxPrice,
    }
    return data