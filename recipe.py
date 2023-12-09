class Recipe():
    def __init__(self, recipe):
        self.name = recipe["name"]
        self.chef = recipe["chef"]
        self.ingredients = recipe["ingredients"]
        self.instructions = recipe["instructions"]

class RecipeList():
    def __init__(self, recipe_list: list = []):
        self.recipe_list = recipe_list
        self.recipe_names = self._recipe_names()
    
    def add(self, recipe):
        self.recipe_list.append(recipe)
        self.recipe_names.append(self._recipe_name(recipe))

    def _recipe_names(self):
        return [self._recipe_name(recipe) for recipe in self.recipe_list]

    def _recipe_name(recipe):
        return recipe["name"]