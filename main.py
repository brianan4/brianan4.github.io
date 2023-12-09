import json
from user_interface import *
from recipe import Recipe
from chef_assistant_machine import ChefAssistantMachine
from chef_ai import ChefAI

def run(state_machine, chef_ai):
    while (True):
        print()
        print(f"Current State: {state_machine.current_state.name}")
        print("Options")
        print("0. Ask ChefAI Question")
        print_list(state_machine.allowed_event_names)
        
        option = get_user_int(len(state_machine.allowed_event_names))

        if option != None:
            if option == 0:
                print()
                question = input("Question: ")
                chef_ai.ask(question)
            else:
                result = state_machine.send(state_machine.allowed_event_names[option - 1])
                print(result)


def main():
    with open("recipes.json", 'r') as f:
        recipes = json.load(f)

    state_machine = ChefAssistantMachine(recipes["recipe_list"])
    chef_ai = ChefAI()

    run(state_machine, chef_ai)
    
if __name__ == '__main__':
    main()