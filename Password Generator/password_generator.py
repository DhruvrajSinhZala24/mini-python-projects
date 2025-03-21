import random

def get_password_length():
    while True:
        try:
            length = int(input("Enter the desired password length (minimum 8): "))
            if length < 8:
                print("⚠️ Password length must be at least 8 for stronger security.")
            else:
                return length
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")

def generate_password(length):
    # Character sets
    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    LOCASE = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
              'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 
              'u', 'v', 'w', 'x', 'y', 'z']
    UPCASE = [char.upper() for char in LOCASE]
    SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', 
               '~', '>', '*', '(', ')', '<']
    # Ensure at least one character from each set
    password = [random.choice(DIGITS),random.choice(LOCASE),random.choice(UPCASE),random.choice(SYMBOLS)]

    # Fill remaining characters randomly
    COMBINED_LIST = DIGITS + LOCASE + UPCASE + SYMBOLS
    password += [random.choice(COMBINED_LIST) for _ in range(length - 4)]

    # Shuffle the password for randomness
    random.shuffle(password)

    # Convert list to string
    return ''.join(password)


print("\n🔒 Secure Password Generator 🔒\n")
password_length = get_password_length()
password = generate_password(password_length)
print("\n✅ Generated Password:", password)