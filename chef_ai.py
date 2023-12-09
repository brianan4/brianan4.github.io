from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class ChefAI():
    def __init__(self):
        self.client = OpenAI()

    def ask(self, question):
        """
        Asks ChatGPT the question and prints out the incoming result
        """
        stream = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a chef, well versed in all aspects of cooking and baking."},
                {"role": "user", "content": question}
            ],
            stream = True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")
        
        print()