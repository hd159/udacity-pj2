from flask_cors import cross_origin
from . import routes

from models import Category

def mappingCategories(categories):
    res = {}
    for category in categories:
       res[category.id] =  category.type

    return res

@routes.route('/categories')
@cross_origin()
def all_categories():
    categories  = Category.query.all()
    categories = mappingCategories(categories)
    return {'categories': categories}

