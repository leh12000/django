


from category.models import Category

def category_list(request):
    categories=Category.objects.all().order_by('name')

    return dict(categories=categories)

