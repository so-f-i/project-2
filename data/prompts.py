import random

REFLECTION_QUESTIONS = [
    "What made you smile today?",
    "What’s something you’ve been avoiding?",
    "What are you grateful for right now?",
    "When did you last feel truly at peace?",
    "What’s one small step you could take toward a goal today?",
    "What’s a lesson life is trying to teach you right now?",
    "What does success look like for you today?",
    "When do you feel most like yourself?",
    "What energizes you?",
    "What’s something you’d like to let go of?",
    "What's the best thing that happened today?",
    "What's the worst thing that happened today?",
    "What's the most interesting thing I saw or heard today?",
    "What's the most challenging thing I faced today?",
    "What am I grateful for today?",
    "What did I learn today?",
    "What was the most fun thing I did today?",
    "What was the most surprising thing that happened today?",
    "What did I do today that I am proud of?",
    "What is the decision I need to make?",
    "Why is your current lifestyle satisfactory? If it isn’t, why not?",
    "How did you meet your first best friend? What are they up to now?",
    "Describe a fear you overcame and how you did so.",
    "List your favorite foods, drinks, snacks, desserts, and more. When was the last time you got to enjoy one of them with a friend?",
    "Create a motto for your life."
]

def get_random_question():
    return random.choice(REFLECTION_QUESTIONS)