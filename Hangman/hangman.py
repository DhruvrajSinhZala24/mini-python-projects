import random

hangman = [
    '''
       +---+
           |
           |
           |
         ===
    ''',
    '''
       +---+
       O   |
           |
           |
         ===
    ''',
    '''
       +---+
       O   |
       |   |
           |
         ===
    ''',
    '''
       +---+
       O   |
      /|   |
           |
         ===
    ''',
    '''
       +---+
       O   |
      /|\  |
           |
         ===
    ''',
    '''
       +---+
       O   |
      /|\  |
      /    |
         ===
    ''',
    '''
       +---+
       O   |
      /|\  |
      / \  |
         ===
    '''
]

words = [
    'python', 'java', 'swift', 'kotlin', 'javascript', 'typescript', 'react', 'angular', 'nodejs', 'django',
    'flask', 'ruby', 'rails', 'html', 'css', 'bootstrap', 'tailwind', 'express', 'mongodb', 'sql',
    'graphql', 'docker', 'kubernetes', 'terraform', 'ansible', 'devops', 'linux', 'ubuntu', 'windows', 'macos',
    'bash', 'powershell', 'git', 'github', 'gitlab', 'bitbucket', 'firebase', 'supabase', 'strapi', 'heroku',
    'netlify', 'vercel', 'aws', 'azure', 'gcp', 'openai', 'huggingface', 'pytorch', 'tensorflow', 'scipy',
    'numpy', 'pandas', 'matplotlib', 'seaborn', 'plotly', 'dash', 'streamlit', 'fastapi', 'bottle', 'cherrypy',
    'tkinter', 'pygame', 'pillow', 'opencv', 'transformers', 'beautifulsoup', 'scrapy', 'selenium', 'robotframework',
    'unittest', 'pytest', 'junit', 'mocha', 'chai', 'jest', 'cypress', 'puppeteer', 'playwright', 'robot',
    'jupyter', 'colab', 'notebook', 'matlab', 'octave', 'sas', 'r', 'stata', 'tableau', 'powerbi', 'looker',
    'excel', 'vba', 'sqlalchemy', 'peewee', 'pony', 'djangoorm', 'sqlmodel', 'asyncio', 'aiohttp', 'quart', 'falcon'
]


def get_hint(word, guesses):
    return random.choice([ch for ch in word if ch not in guesses])


def display_status(missed, correct, word):
    print(hangman[len(missed)])
    print('Missed letters:', ' '.join(missed))
    blanks = ['_' if ch not in correct else ch for ch in word]
    print('Word:', ' '.join(blanks))


def play_game():
    word = random.choice(words)
    missed_letters = []
    correct_letters = []
    hints_used = 0

    while True:
        display_status(missed_letters, correct_letters, word)
        guess = input('Guess a letter (or type "hint" to use a hint): ').lower()

        if guess == 'hint':
            if hints_used < 2:
                hint = get_hint(word, correct_letters + missed_letters)
                print(f'Hint: Try the letter "{hint}"')
                hints_used += 1
            else:
                print('No hints left for this word.')
            continue

        if len(guess) != 1 or not guess.isalpha():
            print('Please enter a single letter.')
            continue

        if guess in correct_letters + missed_letters:
            print('You have already guessed that letter. Choose again.')
            continue

        if guess in word:
            correct_letters.append(guess)
            if all(ch in correct_letters for ch in word):
                print(f'Congratulations! You guessed the word "{word}" correctly!')
                break
        else:
            missed_letters.append(guess)
            if len(missed_letters) == len(hangman) - 1:
                print(hangman[-1])
                print(f'You lost! The word was "{word}"')
                break

    if input("Do you want to play again? (yes/no): ").lower().startswith("y"):
        play_game()
    else:
        print("Thanks for playing!")


play_game()