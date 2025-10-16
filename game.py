import random
import textwrap
import time
import os

RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
MAG = "\033[95m"

RANDOM_POOL = {
    "noun": ["pickle", "spaceship", "rubber chicken", "cactus", "toaster", "penguin"],
    "plural_noun": ["socks", "unicorns", "laptops", "pajamas", "donuts"],
    "adjective": ["sparkly", "moldy", "glittery", "mystical", "fierce", "soggy"],
    "verb": ["juggle", "sprint", "napsplode", "sashimi", "moonwalk", "twerk (gently)"],
    "verb_ing": ["juggling", "moonwalking", "snoozing", "whispering to plants"],
    "number": ["7", "42", "1001", "3.14", "88"],
    "place": ["Iceland", "the backyard", "Your Aunt's attic", "Mars", "the library"],
    "name": ["Alex", "Sam", "Zoë", "Captain Crunch", "Professor Bubble"],
    "exclamation": ["Yowza", "Holy guacamole", "Zing", "Egad", "Yeet"],
    "body_part": ["elbow", "left eyebrow", "big toe", "funny bone"],
    "food": ["wasabi ice cream", "spaghetti tacos", "peanut butter curry"],
    "animal": ["narwhal", "giraffe", "axolotl", "platypus"]
}

TEMPLATES = {
    "The Great Escape": textwrap.dedent("""
        Today I helped a {adjective} {noun} escape from {place}.
        It was wearing {adjective2} {plural_noun} and kept {verb_ing}.
        "Don't worry!" I yelled. "{exclamation}!" I grabbed my {noun2} and we ran for {number} minutes.
        In the end we hid inside a giant {food} and befriended a {animal} named {name}.
        It was the most {adjective3} afternoon of my life.
    """).strip(),
    "Space Tourist": textwrap.dedent("""
        I booked a one-way ticket to {place} because I wanted to {verb}.
        The flight attendant was a {adjective} {animal} who insisted we all wear {plural_noun}.
        Mid-flight we discovered the captain had replaced the steering wheel with a {noun}.
        We landed on a runway made of {food} and celebrated by {verb_ing2}.
        The souvenir shop sold {number} tiny {noun2}s — I bought them all.
    """).strip(),
    "Magical Job Interview": textwrap.dedent("""
        Interviewer: Tell me about yourself.
        Me: I'm a {adjective} {noun} from {place}. I love to {verb} and {verb2}.
        Interviewer: Any weaknesses?
        Me: Occasionally I speak fluent {animal} and my {body_part} glows when I'm excited.
        Interviewer: You're hired — you start on {number}!
        We celebrated by eating {food} and shouting "{exclamation}!" at the clouds.
    """).strip(),
    "Haunted Recipe": textwrap.dedent("""
        To make my famous {noun} stew you'll need {number} cups of {food}, {adjective} {plural_noun},
        a dash of {exclamation} and exactly one {body_part} (do not substitute).
        Stir clockwise while chanting "{exclamation2}" and add the {animal}.
        Serve to guests at {place} and watch them {verb} in delight.
    """).strip()
}

PLACEHOLDERS = {
    "noun": ["noun", "noun2"],
    "noun2": ["noun2"],
    "plural_noun": ["plural_noun"],
    "adjective": ["adjective"],
    "adjective2": ["adjective2"],
    "adjective3": ["adjective3"],
    "verb": ["verb"],
    "verb2": ["verb2"],
    "verb_ing": ["verb_ing"],
    "verb_ing2": ["verb_ing2"],
    "number": ["number"],
    "place": ["place"],
    "name": ["name"],
    "exclamation": ["exclamation"],
    "exclamation2": ["exclamation2"],
    "body_part": ["body_part"],
    "food": ["food"],
    "animal": ["animal"]
}

POOL_MAP = {
    "noun": "noun",
    "noun2": "noun",
    "plural_noun": "plural_noun",
    "adjective": "adjective",
    "adjective2": "adjective",
    "adjective3": "adjective",
    "verb": "verb",
    "verb2": "verb",
    "verb_ing": "verb_ing",
    "verb_ing2": "verb_ing",
    "number": "number",
    "place": "place",
    "name": "name",
    "exclamation": "exclamation",
    "exclamation2": "exclamation",
    "body_part": "body_part",
    "food": "food",
    "animal": "animal"
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def header():
    print(CYAN + BOLD)
    print("╔════════════════════════════════════════════════╗")
    print("║           Welcome to the  Mad Lips!            ║")
    print("╚════════════════════════════════════════════════╝")
    print(RESET)

def choose_template():
    names = list(TEMPLATES.keys())
    print(YELLOW + "Pick your story template or press Enter for a random one:" + RESET)
    for i, nm in enumerate(names, 1):
        print(f"  {i}. {nm}")
    choice = input("Enter number or press Enter: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(names):
        return names[int(choice) - 1]
    return random.choice(names)

def find_placeholders(template_text):
    ph = []
    start = template_text.find("{")
    while start != -1:
        end = template_text.find("}", start+1)
        if end == -1:
            break
        key = template_text[start+1:end].strip()
        ph.append(key)
        start = template_text.find("{", end+1)
    seen = set()
    result = []
    for p in ph:
        if p not in seen:
            seen.add(p)
            result.append(p)
    return result

def get_input_for(place):
    prompt = f"Give me a {place.replace('_',' ')} (or type '?' for surprise): "
    while True:
        val = input(prompt).strip()
        if val == "?":
            pool_key = POOL_MAP.get(place, None)
            if pool_key and pool_key in RANDOM_POOL:
                return random.choice(RANDOM_POOL[pool_key])
            return random.choice(sum(RANDOM_POOL.values(), []))
        if val == "":
            print("Please enter something or ? for surprise.")
            continue
        return val

def build_story(template_key):
    template = TEMPLATES[template_key]
    placeholders = find_placeholders(template)
    answers = {}
    print(GREEN + f"\nFILL IN THE BLANKS for '{template_key}'" + RESET)
    for ph in placeholders:
        val = get_input_for(ph)
        answers[ph] = val
    try:
        story = template.format(**answers)
    except Exception as e:
        for key in find_placeholders(template):
            if key not in answers:
                answers[key] = random.choice(RANDOM_POOL.get(POOL_MAP.get(key, ""), ["thing"]))
        story = template.format(**answers)
    return textwrap.fill(story, width=80)

def save_story(story):
    save = input("Save story to file? (y/N): ").strip().lower()
    if save == "y":
        fname = f"madlib_{int(time.time())}.txt"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(story + "\n")
        print(GREEN + f"Saved as {fname}" + RESET)

def main():
    clear_screen()
    header()
    random.seed()
    while True:
        template_key = choose_template()
        print(MAG + f"\nYou chose: {template_key}\n" + RESET)
        story = build_story(template_key)
        print("\n" + CYAN + BOLD + "— Your Mad Lib —" + RESET)
        print(story)
        print(CYAN + "— end —\n" + RESET)
        save_story(story)
        again = input("Play again? (Y/n): ").strip().lower()
        if again == "n":
            print(YELLOW + "Thanks for playing! Stay gloriously silly." + RESET)
            break
        clear_screen()
        header()

if __name__ == "__main__":
    main()
