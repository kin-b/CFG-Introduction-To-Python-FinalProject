#checking the recieved recipes against a nutrition database to check for health warnings - the code is not refined
#not included in the final project or refined because while it works, the data provided by the database is useless
#eg an ingredient like 'yoghurt' comes back with no health warnings despite being a milk based product - same for most ingredients

import requests


ingredient = input("What ingredient are you looking for? ")


def search_for_recipes(i):
    url = 'https://api.edamam.com/api/recipes/v2?type=public&q={}&app_id=bf4faac8&app_key=f4bdbe647d5552ddd866335984c798f9'.format(i)
    response = requests.get(url)
    results = response.json()
    return results


def check_ingredient(i2):
    url = 'https://api.edamam.com/api/nutrition-data?app_id=cc691f12&app_key=3b805f9d01a82a7a740dd845ba678aae&nutrition-type=cooking&ingr={}'.format(i2)
    response2 = requests.get(url)
    results2 = response2.json()
    cautions = results2['cautions']
    return cautions


def ingeredients_with_warnings(ingrs):
    checked_ingrs = []
    for ingr in ingrs:
        checked_ingr = []
        warnings = {}
        check = check_ingredient(ingr)
        checked_ingr.append(ingr)
        warnings.update(({"dietary warning": "{}".format(check)}))
        checked_ingr.append(warnings)
        checked_ingrs.append(checked_ingr)
    return checked_ingrs


recipes = search_for_recipes(ingredient)['hits']

for recipe in recipes:
    print('\n' + recipe['recipe']['label'].upper())
    recipe_ingredients = []
    for ingredient in recipe:
        ingredients2 = recipe['recipe']['ingredients']
        recipe_ingredients_nxt_lvl = []
        for ingredient_next_level in ingredients2:
            recipe_ingredients_nxt_lvl.append(ingredient_next_level.get('food'))
        ingr_warnings = ingeredients_with_warnings(recipe_ingredients_nxt_lvl)
        recipe_ingredients.append(ingr_warnings)
    print(recipe_ingredients)
