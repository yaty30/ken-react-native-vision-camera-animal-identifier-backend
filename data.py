import random

class Fishes:
    clownfish = {
        'title': "Clownfish",
        'description': "The clownfish can be many different colours, depending on its species, including yellow, orange, red, and black. Most have white details. They are smaller fish, with the smallest around 7 to 8cm long and the longest 17cm long."
    }
    
    blue_tang = {
        'title': "Blue Tang",
        'description': "Blue tangs are high-bodied, compressed, pancake-shaped fishes with pointed snouts and small scales. Their eyes are located high on their heads and their mouths are small and positioned low. Their dorsal fins are continuous."
    }

    yellow_tang = {
        'title': "Yellow Tang",
        'description': "A popular marine fish known for its vibrant yellow color and oval shape, the Yellow Tang is a herbivore that primarily feeds on algae. Native to the reefs of the Pacific Ocean, it is often seen in groups and is a favorite among aquarium enthusiasts."
    }

    powder_blue_tang = {
        'title': "Powder Blue Tang",
        'description': "This strikingly beautiful tang has a bright blue body with a yellow tail and a distinctive black pattern on its face. It is known for its active swimming behavior and is commonly found in coral reefs in the Indo-Pacific region."
    }

    butterflyfish = {
        'title': "Butterflyfish",
        'description': "Butterflyfish are small, colorful reef fish characterized by their laterally compressed bodies and vibrant patterns. They feed on coral polyps and small invertebrates and are often seen in pairs or small groups, adding beauty to coral reef ecosystems."
    }

    bicolor_foxface = {
        'title': "Bicolor Foxface",
        'description': "The Bicolor Foxface, also known as the Bicolor Rabbitfish, has a unique coloration with a yellow body and a black face. This species is known for its ability to adapt to various environments and primarily feeds on algae and plant material."
    }

    black_surgeonfish = {
        'title': "Black Surgeonfish",
        'description': "Also known as the Black Tang, this fish features a dark, almost black body with a unique shape and sharp spines on its tail. It is a herbivore that grazes on algae and is found in the reefs of the Pacific Ocean, often seeking shelter in crevices."
    }

    fish_list = [clownfish, blue_tang, yellow_tang, powder_blue_tang, butterflyfish, bicolor_foxface, black_surgeonfish]
    
    def get_random_target(self):
        return self.fish_list[random.randint(0, len(self.fish_list) - 1)]
    



