from openai import OpenAI

class ChefAI():
    def __init__(self):
        self.client = OpenAI()

    def ask(self, question):
        """
        Asks ChatGPT the question and returns out the incoming result
        """
        stream = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a chef, well versed in all aspects of cooking and baking."},
                {"role": "user", "content": question}
            ],
            stream = True
        )

        line = ""

        for chunk in stream:
            chunk_content = chunk.choices[0].delta.content
            
            if chunk_content:
                line += chunk_content
                if "\n" in chunk_content:
                    yield line
                    line = ""
            elif line:
                yield line

    
    def adjust(self, adjustment, recipe_json_string):
        print(adjustment)
        print(recipe_json_string)
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": '''You are a chef, well versed in all aspects of cooking and baking. 
Constraints: Each step in "recipe" can only include one ingredient. 
The ingredient has to be present in the list of "ingredients".
All ingredient in "ingredients" utilize mass or count based measurements.
Modify the recipe through the .json file
Result: Return a .json file.'''},
                {"role": "user", "content": f"{adjustment}. {recipe_json_string}"}
            ],
        )

        return completion.choices[0].message.content
    
if __name__ == "__main__":
    chef_ai = ChefAI()
    for line in chef_ai.ask("What is 2 + 2?"):
        print(line)