import os
import re

CWD = os.path.dirname(os.path.abspath(__file__))
INPUT = [l.rstrip() for l in open(f"{CWD}/input.txt", "r").readlines()]


def get_allergens(input):
    foods = []
    possible_allergens = {}
    for line in input:
        match = re.match(r"^(.*) \(contains (.*)\)$", line)
        ingredients = set(match[1].split(" "))
        foods.append(set(match[1].split(" ")))
        for allergen in match[2].split(", "):
            if allergen in possible_allergens:
                possible_allergens[allergen] = (
                    possible_allergens[allergen] & ingredients
                )
            else:
                possible_allergens[allergen] = ingredients
    allergens = {}
    while len(allergens) < len(possible_allergens):
        for allergen, ingredients in possible_allergens.items():
            if len(ingredients) == 1:
                ingredient = list(ingredients)[0]
                allergens[allergen] = ingredient
                for allergen in possible_allergens.keys():
                    if ingredient in possible_allergens[allergen]:
                        possible_allergens[allergen] -= {ingredient}
                break
    return allergens, foods


def print_part1_ans(input):
    allergens, foods = get_allergens(input)
    allergen_names = set(allergens.values())
    safe_ingredients_count = 0
    for food in foods:
        safe_ingredients_count += len(food - allergen_names)
    print(safe_ingredients_count)


def print_part2_ans(input):
    allergens, _ = get_allergens(input)
    allergen_list = list(allergens.keys())
    allergen_list.sort()
    ingredients = []
    for allergen in allergen_list:
        ingredients.append(allergens[allergen])
    print(",".join(ingredients))


print_part1_ans(INPUT)
print_part2_ans(INPUT)
