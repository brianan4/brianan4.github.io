import json

class Recipe():
    def __init__(self, recipe_file):
        with open(recipe_file, 'r') as f:
            recipe_json = json.load(f)
        
        self.file = recipe_file
        self.json = recipe_json
        self.json_string = json.dumps(recipe_json)
        self.name = ""
        self.ingredients = dict()
        self.recipe = []
        self.steps = 0
        self.step = 0
        self.instructions = []

        self._load_json(recipe_json)

    def start(self):
        self.step = 1

    def next(self):
        if self.step < self.steps:
            self.step += 1
            return 0
        else:
            self.end()
            return 1
        
    def back(self):
        if self.step > 1:
            self.step -= 1
            return 0
        else:
            self.end()
            return 1

    def end(self):
        self.step = 0
        return 1

    def current_step(self):
        return self.step

    def instruction(self, step=None):
        instruction = (0, "")

        if step == None:
            step = self.step - 1

        if 0 <= step < self.steps:
            instruction = (self.recipe[step], self.instructions[step])
        
        return instruction
        
        
    def adjust(self, adjustment_json):
        self._load_json(adjustment_json)

    def _load_json(self, recipe_json):
        self.json = recipe_json
        self.name = recipe_json["name"]
        self.ingredients = recipe_json["ingredients"]
        self.recipe = recipe_json["recipe"]
        self.steps = len(self.recipe)
        self.step = 0
        self.instructions = self._create_instructions(self.recipe, self.ingredients)

    def _create_instructions(self, recipe: list, ingredients: dict) -> list:
        instructions = []
        ingredient_list = list(ingredients.keys())

        for step in recipe:
            ingredient_present = False

            for ingredient in ingredient_list:
                if ingredient in step:
                    ingredient_present = True
                    instructions.append(ingredients[ingredient])

                    ingredient_list.remove(ingredient)
                    break
                    
            if ingredient_present == False:
                instructions.append("")

        return instructions
    
    def recipe_instructions(self):
        recipe_instruction = []

        for step in range(self.steps):
            recipe_instruction.append(self.instruction(step))

        return recipe_instruction

def test_Recipe_recipe_instructions():
    with open("teriyaki_chicken_recipe.json", 'r') as f:
        r = json.load(f)
        recipe = Recipe(r)

    print(recipe.recipe_instructions())

if __name__ == '__main__':
    # Test Cases
    test_Recipe_recipe_instructions()