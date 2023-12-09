from recipe import Recipe
from user_interface import *
from statemachine import StateMachine, State


class ChefAssistantMachine(StateMachine):
    """Chef Voice Assistant State Machine"""
    
    def __init__(self, recipe_list: [Recipe] = []):
        self.recipe_list = recipe_list
        self.recipe_names = self._recipe_names()
        self.selected_recipe_name = None
        self.ingredients = None
        self.recipe = None
        self.step = 0
        super().__init__()

    # States
    home_state = State(initial=True)
    
    recipe_list_state = State()
    insert_recipe_state = State()

    single_recipe_state = State()

    ingredient_list_state = State()
    shopping_list_state = State()

    cooking_start_state = State()
    cooking_state = State()
    cooking_end_state = State()

    adjust_recipe_state = State()
    
    # Events -> Transitions
    back = (recipe_list_state.to(home_state)
        | insert_recipe_state.to(recipe_list_state)
        | single_recipe_state.to(recipe_list_state)
    )

    back |= (
        ingredient_list_state.to(single_recipe_state)
        | shopping_list_state.to(ingredient_list_state)
    )

    back |= cooking_start_state.to(single_recipe_state)
    
    exit = (
        shopping_list_state.to(single_recipe_state) 
        | adjust_recipe_state.to(single_recipe_state) 
        | cooking_end_state.to(single_recipe_state)
    )

    cancel = cooking_state.to(single_recipe_state)
    
    finish = shopping_list_state.to(single_recipe_state)

    recipes = home_state.to(recipe_list_state)
    insert_recipe = recipe_list_state.to(insert_recipe_state)
    select_recipe = recipe_list_state.to(single_recipe_state)
    manage_ingredients = single_recipe_state.to(ingredient_list_state)
    shop_ingredients = ingredient_list_state.to(shopping_list_state)
    start_cooking = single_recipe_state.to(cooking_start_state)
    next_instruction = (
        cooking_start_state.to(cooking_state) 
        | cooking_state.to.itself(unless = "second_last_step")
        | cooking_state.to(cooking_end_state)
    )
    previous_instruction = (
        cooking_state.to(cooking_start_state, cond = "second_step")
        | cooking_state.to.itself() 
        | cooking_end_state.to(cooking_state)
    )
    adjust_recipe = single_recipe_state.to(adjust_recipe_state) | cooking_end_state.to(adjust_recipe_state)
    apply_adjustment = adjust_recipe_state.to.itself()

    # Actions
    def on_select_recipe(self):
        option = None

        while(option == None):
            print()
            print_list(self.recipe_names, "Recipes: ")
            
            option = get_user_int(len(self.recipe_names))
            
            if option != None:
                self.step = 0
                self.selected_recipe_name = self.recipe_names[option]
                self.ingredients = self._recipe_ingredients()
                self.recipe = self._recipe_instructions()
        
        return f"Selected Recipe: {self.selected_recipe_name}"

    # Cooking Actions
    def on_next_instruction(self):
        self.step += 1

    def on_previous_instruction(self):
        self.step -= 1

    def on_start_cooking(self):
        print()
        print_dict(self.ingredients, "Ingredients:")

    def on_enter_cooking_start_state(self):
        self.step = 0
        self._print_recipe_step()

    def on_enter_cooking_state(self):
        self._print_recipe_step()

    @property
    def allowed_event_names(self):
        """List of the current allowed event names."""
        return self.current_state.transitions.unique_events
    
    def _recipe_names(self):
        return [recipe["name"] for recipe in self.recipe_list]
    
    def _ingredients(self, recipe_name):
        for recipe in self.recipe_list:
            if recipe_name == recipe["name"]:
                return recipe["ingredients"]
            
    def _recipe_ingredients(self):
        return self._ingredients(self.selected_recipe_name)

    def _recipe(self, recipe_name):
        for recipe in self.recipe_list:
            if recipe_name == recipe["name"]:
                return recipe["instructions"]
            
    def _recipe_instructions(self):
        return self._recipe(self.selected_recipe_name)
    
    def _print_recipe_step(self):
        print()
        print(f"{self.step + 1}. {self.recipe[self.step]}")

    def second_step(self):
        return (self.step == 1)
    
    def second_last_step(self):
        return (self.step == len(self.recipe) - 1)