#Project goal: requesting data from an api, displaying it, sorting it, saving it to file
#the program gets recipes from edamam.com for the ingredient, meal type and diet chosen by the user
#then sorts them and displays them


import requests
import json
from pprint import pprint


def meal_type(mt):
    if mt == "b" or mt == "B":
        m_t2 = 'breakfast'
    elif mt == "l" or mt == "L":
        m_t2 = 'lunch'
    elif mt == "d" or mt == "D":
        m_t2 = 'dinner'
    elif mt == "t" or mt == "T":
        m_t2 = 'teatime'
    elif mt == "s" or mt == "S":
        m_t2 = 'snack'
    else:
        m_t2 = ''
    return m_t2


def diet_type(dt):
    if dt == "1":
        d_t2 = 'DASH'
    elif dt == "2":
        d_t2 = "immuno-supportive"
    elif dt == "3":
        d_t2 = "keto-friendly"
    elif dt == "4":
        d_t2 = "kosher"
    elif dt == "5":
        d_t2 = "Mediterranean"
    elif dt == "6":
        d_t2 = "paleo"
    elif dt == "7":
        d_t2 = "sugar-conscious"
    elif dt == "8":
        d_t2 = "vegan"
    elif dt == "9":
        d_t2 = "vegetarian"
    else:
        d_t2 = ''
    return d_t2


def displaying_choice(d):
    if d == "C" or d == "c":
        dc = 'calories'
    elif d == "t" or d == "T":
        dc = 'preptime'
    elif d == "s" or d == "S":
        dc = 'servings'
    else:
        dc = ''
    return dc


def search_for_recipes(i, i2, i3):
    if i2 == '' and i3 == '':
        url = 'https://api.edamam.com/api/recipes/v2?type=public&q={}&app_id=bf4faac8&app_key=f4bdbe647d5552ddd866335984c798f9'.format(i)
    elif i2 != '' and i3 == '':
        url = 'https://api.edamam.com/api/recipes/v2?type=public&q={}&app_id=bf4faac8&app_key=f4bdbe647d5552ddd866335984c798f9&mealType={}'.format(i, i2)
    elif i2 == '' and i3 != '':
        url = 'https://api.edamam.com/api/recipes/v2?type=public&q={}&app_id=bf4faac8&app_key=f4bdbe647d5552ddd866335984c798f9&health={}'.format(i, i3)
    else:
        url = 'https://api.edamam.com/api/recipes/v2?type=public&q={}&app_id=bf4faac8&app_key=f4bdbe647d5552ddd866335984c798f9&health={}&mealType={}'.format(i, i3, i2)
    response = requests.get(url)
    results = response.json()
    return results


def sorting_by_servings(s):
    return s['recipe']['yield']


def sorting_by_calories(s):
    return s['recipe']['calories']


def sorting_by_totaltime(s):
    return s['recipe']['totalTime']


def sorting_the_results(results2, choice):
    if choice == 'calories':
        results2.sort(key=sorting_by_calories)
    elif choice == 'preptime':
        results2.sort(key=sorting_by_totaltime)
    elif choice == 'servings':
        results2.sort(key=sorting_by_servings)
    else:
        results2 = results2
    return results2


def save_to_file(my_recipes):
    with open('my_recipes.txt', 'w+') as text_file:
        text_file.write(my_recipes)


ingredient = input("What ingredient do you fancy cooking with today? ")
meal = input("What meal are you making?\n(b-breakfast/l-lunch/d-dinner/t-teatime/s-snack/a-any) ")
diet = input("Do you follow a specific diet? Choose a number:\n1-DASH\n2-Immuno-Supportive\n3-Keto-Friendly\n4-Kosher\n5-Mediterranean\n6-Paleo\n7-Sugar-Conscious\n8-Vegan\n9-Vegetarian\n0-I'm Omnivorous\n")
results_display = input("How do you want your results sorted?\n(c-calories/s-servings/t-preparation time) ")

mealType = meal_type(meal)
dietType = diet_type(diet)
user_choice = displaying_choice(results_display)
recipes = search_for_recipes(ingredient, mealType, dietType)#['hits']
recipes = recipes['hits']
recipes = sorting_the_results(recipes, user_choice)
recipes_to_str = json.dumps(recipes, indent=4)
save_to_file(recipes_to_str)

for recipe in recipes:
    print('\n' + recipe['recipe']['label'].upper())
    print("by: " + str(recipe['recipe']['source']) + " - " + str(recipe['recipe']['url']))
    print(recipe['recipe']['mealType'])
    print(diet_type(diet))
    print('servings: ' + str(recipe['recipe']['yield']))
    print('preparation time: ' + str(recipe['recipe']['totalTime']))
    print('ingredients list:')
    pprint(recipe['recipe']['ingredientLines'])
    print('calories: ' + str(recipe['recipe']['calories']))
