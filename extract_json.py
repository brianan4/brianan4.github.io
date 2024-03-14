class ExtractJSON():
    def __init__(self, text: str):
        self.intro = ""
        self.outro = ""
        self.json_string = ""

        first_brace_index = text.find('{')
        last_brace_index = text.rfind('}')

        if first_brace_index != -1 and last_brace_index != -1:
            self.intro = text[0:first_brace_index].strip()
            self.outro = text[last_brace_index + 1: -1].strip()
            self.json_string = text[first_brace_index: last_brace_index + 1].strip()


if __name__ == "__main__":
    data = ExtractJSON('''To make the Teriyaki Chicken more flavorful, let's incorporate additional spices from the provided list into the recipe steps. Here's the updated recipe:

{    
    "name": "Spicy Teriyaki Chicken",
    "ingredients": {
        "chicken thigh": "2 lb",
        "soy sauce": "132 g",
        "rice vinegar": "115 g",
        "sesame oil": "5 g",
        "garlic": "3 cloves",
        "red pepper flakes": "1 g",
        "ground black pepper": "1 g",
        "honey": "64 g",
        "corn starch": "3 g",
        "water": "8 g"
    },
    "recipe": [
        "In a medium sized bowl add soy sauce",
        "Add rice vinegar",
        "Add sesame oil",
        "Mince and add garlic",
        "Add red pepper flakes",
        "Add ground black pepper",
        "Mix thoroughly and use just enough to marinate and cover the chicken thigh",
        "Airfry the marinated chicken at 400F for 12:00",
        "Mix in honey to your remaining marinade",
        "In a small sized bowl add corn starch",
        "Mix in water and set aside",
        "Fire a pan over medium heat and add the marinade",
        "Once the marinade is hot, mix in the starch slurry",
        "Add an extra 1 g of red pepper flakes to the marinade mixture for added spice",
        "Remove the marinade off the heat once it has thickened",
        "Flip and airfry for an additional 12:00",
        "Cut and serve over rice and vegetables"
    ]
}

In this updated recipe, I've added an additional step to incorporate more red pepper flakes into the marinade mixture for an extra kick of spice. This should make your Teriyaki Chicken more flavorful and spicy.)''')
    
    print(data.intro)
    print(data.outro)
    print(data.json_string)