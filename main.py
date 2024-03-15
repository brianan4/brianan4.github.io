from dotenv import load_dotenv
import os
import json

from recipe import Recipe
from extract_json import ExtractJSON

from chef_assistant_machine import ChefAssistantMachine
from chef_ai import ChefAI

import text_to_speech
import speech_to_text

# Load API Credentials
load_dotenv()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google-cloud-api-key.json'

# Shortcut Calls
def say(input, print_out = True, end = "\n"):
    text = input
    
    if type(input) != str:
        text = str(input)

    if print_out == True:
        print(text)

    text_to_speech.text_to_audio(text)

def transcribe(text = ""):
    if text:
        say(text)

    return speech_to_text.audio_to_text()

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def run(recipe: Recipe, state_machine: ChefAssistantMachine, chef_ai: ChefAI):
    instruction_phrase = ""
    valid_command = True

    while (not state_machine.current_state.final):
        if valid_command == True:
            clear()

            state_phrase = f"Current State: {state_machine.current_state.name}"
            print(state_phrase)

            print()

            if instruction_phrase:
                say(instruction_phrase)

            print()

            allowed_event_phrase = "Commands: ask, "
            allowed_event_phrase += ", ".join(state_machine.allowed_event_names)
            print(allowed_event_phrase)
        else:
            valid_command = True

        command = transcribe()

        if command == "ask":
            print()
            question = transcribe("What is your question?")
            print(f"Question: {question}")
            
            response_stream = chef_ai.ask(question)
            
            line1 = next(response_stream)
            say(line1.strip("\n"), end = '')

            for line in response_stream:
                print(line, end = '')
                
            valid_command = False
            print()
        elif command in state_machine.allowed_event_names:
            event = command
            code = 0

            match command:
                case "adjust":
                    state_machine.send("adjust")
                    say("What feedback/adjustment would you make to the recipe?")
                    feedback = transcribe()

                    response = chef_ai.adjust(feedback, recipe.json_string)

                    adjustment = ExtractJSON(response)

                    say(adjustment.intro)
                    print(adjustment.json_string)
                    adjustment_json = json.loads(adjustment.json_string)

                    with open(f"previous_{recipe.file}", 'w') as pf:
                        json.dump(recipe.json, pf, indent = 4)
                    
                    with open(recipe.file, 'w') as f:
                        json.dump(adjustment_json, f, indent = 4)

                    recipe.adjust(adjustment_json)

                    say(adjustment.outro)

                    code = 1
                    valid_command = False
                case _:
                    match command:
                        case "next":
                            event = "next"
                            code = recipe.next()
                        case "back":
                            event = "back"
                            code = recipe.back()
                        case "exit":
                            event = "exit"
                            code = recipe.end()

                    state_machine.send(event, code)

            instruction_phrase = ""
            if code == 0:
                recipe_step, recipe_measurement = recipe.instruction()
                
                if recipe_measurement:
                    recipe_measurement = f"({recipe_measurement})"

                instruction_phrase = f"Step {recipe.current_step()}. {recipe_step} {recipe_measurement}"
        else:
            valid_command = False


def main():
    recipes = ["teriyaki_chicken_recipe.json"]
    recipe_file = recipes[0]
    
    recipe = Recipe(recipe_file)
    state_machine = ChefAssistantMachine()
    chef_ai = ChefAI()

    run(recipe, state_machine, chef_ai)
    
if __name__ == '__main__':
    main()