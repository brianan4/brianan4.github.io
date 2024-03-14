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
def say(input):
    text = input
    
    if type(input) != str:
        text = str(input)

    text_to_speech.text_to_audio(text)

def transcribe(text = ""):
    if text:
        say(text)

    return speech_to_text.audio_to_text()

def run(recipe: Recipe, state_machine: ChefAssistantMachine, chef_ai: ChefAI):
    while (True):
        state_phrase = f"Current State: {state_machine.current_state.name}"
        print(state_phrase)
        print(state_machine.allowed_event_names)

        word = transcribe()

        if word == "ask":
            question = transcribe("What is your question?")
            response_stream = chef_ai.ask(question)
            
            for line in response_stream:
                print(line)
                say(line)

        elif word in state_machine.allowed_event_names:
            code = 0

            match word:
                case "adjust":
                    state_machine.send(word)
                    say("What feedback/adjustment would you make to the recipe?")
                    feedback = transcribe()

                    response = chef_ai.adjust(feedback, recipe.json_string)

                    adjustment = ExtractJSON(response)

                    say(adjustment.intro)
                    print(response)
                    print(adjustment.json_string)
                    adjustment_json = json.loads(adjustment.json_string)

                    with open(f"previous_{recipe.file}", 'w') as pf:
                        json.dump(recipe.json, pf, indent = 4)
                    
                    with open(recipe.file, 'w') as f:
                        json.dump(adjustment_json, f, indent = 4)

                    recipe.adjust(adjustment_json)

                    say(adjustment.outro)
                case _:
                    match word:
                        case "next":
                            code = recipe.next()
                        case "back":
                            code = recipe.back()
                        case "exit":
                            recipe.end()

                    state_machine.send(word, code)

                    if code == 0:
                        instruction_phrase = f"Step {recipe.current_step()}. {recipe.instruction()}"
                        say(instruction_phrase)
        else:
            say("Unknown command")
                    
        print()


def main():
    recipes = ["test_recipe.json", "teriyaki_chicken_recipe.json"]
    recipe_file = recipes[1]
    
    recipe = Recipe(recipe_file)
    state_machine = ChefAssistantMachine()
    chef_ai = ChefAI()

    run(recipe, state_machine, chef_ai)
    
if __name__ == '__main__':
    main()