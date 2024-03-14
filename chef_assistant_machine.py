from recipe import Recipe
from user_interface import *
from statemachine import StateMachine, State


class ChefAssistantMachine(StateMachine):
    """Chef Voice Assistant State Machine"""
    # States
    recipe_state = State(initial=True)
    cooking_state = State()
    adjust_recipe_state = State()
    
    # Events -> Transitions
    next = recipe_state.to(cooking_state)
    next |= cooking_state.to.itself(unless = "error")
    next |= cooking_state.to(recipe_state)
    
    back = cooking_state.to.itself(unless = "error")
    back |= cooking_state.to(recipe_state)

    adjust = recipe_state.to(adjust_recipe_state)
    adjust |= adjust_recipe_state.to(adjust_recipe_state)

    exit = cooking_state.to(recipe_state)
    exit |= adjust_recipe_state.to(recipe_state)

    @property
    def allowed_event_names(self):
        """List of the current allowed event names."""
        return self.current_state.transitions.unique_events
    
    def error(self, code):
        return code != 0