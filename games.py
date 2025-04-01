import random

class Games:

    @staticmethod
    def play_lottery():
        print("🎰 Welcome to the Lottery Game! 🍀💰\n")
        print("📜 How to Play:")
        print("1️⃣ Choose 5 unique numbers between 1 and 50.")
        print("2️⃣ The system will randomly draw 5 winning numbers.")
        print("3️⃣ If all your numbers match, you win the jackpot! 🎉\n")
        
        user_numbers = set()
        winning_numbers = set(random.sample(range(1, 51), 5))
        
        while len(user_numbers) < 5:
            try:
                user_input = int(input(f"🔢 Enter number {len(user_numbers) + 1} (1-50): "))
                
                if user_input < 1 or user_input > 50:
                    print("⚠️ Invalid input! Please enter a number between 1 and 50.")
                    print(f"📌 You still need to pick {5 - len(user_numbers)} numbers.")
                elif user_input in user_numbers:
                    print("⚠️ You already picked this number. Try another!")
                else:
                    user_numbers.add(user_input)
                    print(f"✅ Your current numbers: {sorted(user_numbers)}")
            except ValueError:
                print("⚠️ Invalid input! Please enter a valid number.")
        
        print("\n🔹 Your lottery numbers:", sorted(user_numbers))
        print("🎯 Winning numbers:", sorted(winning_numbers))
        
        if user_numbers == winning_numbers:
            print("\n🎉🎊 JACKPOT! You won the lottery! 🎊🎉")
        else:
            print("\n😢 Better luck next time!")

    @staticmethod
    def play_number_guessing():
        print("🎯 Welcome to the Number Guessing Game! 🔢✨\n")
        print("📜 How to Play:")
        print("1️⃣ The system selects a random number between 1 and 100.")
        print("2️⃣ You have 5 attempts to guess the correct number.")
        print("3️⃣ After each guess, you'll get a hint whether it's higher or lower.\n")
        
        random_number = random.randint(1, 100)
        guessed_numbers = []
        attempts = 5
        
        while attempts > 0:
            try:
                user_input = int(input("🔢  Guess a number (1-100): 🤔 "))
                
                if user_input < 1 or user_input > 100:
                    print("⚠️ Out of range! Pick a number between 1 and 100.")
                    continue
                
                guessed_numbers.append(user_input)
                
                if user_input == random_number:
                    print("\n🎯 BOOM! You guessed it right! 🎉")
                    return
                
                print(f"📜 Your guesses so far: {', '.join(map(str, guessed_numbers))}")
                
                if user_input > random_number:
                    print("📉 Too high! Try a smaller number.")
                else:
                    print("📈 Too low! Try a bigger number.")
                    
                attempts -= 1
                print(f"🕒 Attempts left: {attempts}")

            except ValueError:
                print("⚠️ Invalid input! Please enter a number.")
        
        print(f"\n😢 No more attempts! The correct number was {random_number}. Better luck next time! 🎭")
        print(f"📜 Your guesses: {guessed_numbers}")
    
    @staticmethod
    def play_rock_paper_scissors():
        print("✊📄✂️ Welcome to the Rock, Paper, Scissors Game! ✨\n")
        print("📜 How to Play:")
        print("✅ You will play against the computer. 🤖")
        print("✅ The computer will randomly select rock, paper, or scissors. 🎲")
        print("✅ You can choose between rock, paper, or scissors. 🔄")
        print("✅ The winner will be decided based on the following rules:")
        print("   - ✊ Rock crushes ✂️ Scissors")
        print("   - ✂️ Scissors cuts 📄 Paper")
        print("   - 📄 Paper covers ✊ Rock")
        print("🏆 First to 3 points wins!\n")

        player_score = 0
        computer_score = 0
        
        def get_emoji(choice):
            emojis = {
                "rock": "✊",
                "paper": "📄",
                "scissors": "✂️"
                }
            return emojis.get(choice, "")
    
        print("🎮 Let's Begin! First to 3 points wins. Good luck! 🍀")

        while player_score < 3 and computer_score < 3:
            computer_choice = random.choice(["rock", "paper", "scissors"])
            player_choice = input("\n📝 Choose (rock, paper, or scissors): ").lower().strip()

            if player_choice not in ['rock', 'paper', 'scissors']:
                print("⚠️ Invalid choice! Please select rock, paper, or scissors.")
                continue

            print(f"\n🙋‍♂️ You chose: {player_choice.capitalize()} {get_emoji(player_choice)}")
            print(f"🤖 Computer chose: {computer_choice.capitalize()} {get_emoji(computer_choice)}")

            if computer_choice == player_choice:
                print("⚖️ It's a tie! No points given.")
            elif (computer_choice == "rock" and player_choice == "scissors") or \
                    (computer_choice == "paper" and player_choice == "rock") or \
                    (computer_choice == "scissors" and player_choice == "paper"):
                print("💻 Computer wins this round! ❌")
                computer_score += 1
            else:
                print("🎉 You win this round! ✅")
                player_score += 1
            
            print(f"📊 Scoreboard - You: {player_score} | Computer: {computer_score}")
        
        print("\n🏆 Final Scoreboard - You: {} | Computer: {}".format(player_score, computer_score))

        # Game over
        if player_score == 3:
            print("\n🏆🎊 Congratulations, you won the game! 🎉🥇")
        else:
            print("\n🤖💀 The computer won the game. Better luck next time! 😞")

    @staticmethod
    def play_hangman():
        print("🎭 Welcome to the Hangman Challenge! 🎭\n")
        print("📜 How to Play:")
        print("✅ The system will randomly select a word related to occupations. 🏢")
        print("✅ You have 5 attempts to guess the correct word. 🎯")
        print("✅ After each guess, you will see if the letter is in the word. 🧐")
        print("✅ Guess all letters before running out of attempts! ❌\n")

        words = ["Engineer", "Doctor", "Teacher", "Architect", "Pilot",
                    "Lawyer", "Nurse", "Carpenter", "Electrician", "Plumber", "Chef",
                    "Farmer", "Scientist", "Accountant", "Journalist", "Artist",
                    "Mechanic", "Librarian", "Veterinarian", "Programmer"]

        chosen_word = random.choice(words).lower()  # Convert to lowercase for consistency
        guess_attempts = 5
        guessed_letters = []  # Tracks guessed letters
        revealed_word = ["_"] * len(chosen_word)  # Tracks the current state of the word

        while guess_attempts > 0:
            print("\n🔤 Word:", " ".join(revealed_word))  # Show the current word state
            user_input = input("\n🔡 Guess a letter: ").lower().strip()

            if len(user_input) != 1 or not user_input.isalpha():
                print("⚠️ Please enter a single valid letter! 🧐")
                continue

            if user_input in guessed_letters:
                print("🔄 You've already guessed that letter. Try again! 🔁")
                continue

            guessed_letters.append(user_input)

            if user_input in chosen_word:
                print("✅ Great! The letter is in the word! 🎉")

                # Reveal all occurrences of the guessed letter
                for i, letter in enumerate(chosen_word):
                    if letter == user_input:
                        revealed_word[i] = user_input
            else:
                print("❌ Oops! That letter is not in the word. 😔")
                guess_attempts -= 1
                print(f"🕒 Attempts left: {guess_attempts}")

            # Check if the word is fully revealed
            if "_" not in revealed_word:
                print(f"\n🎊 Congratulations! You've guessed the word: {''.join(revealed_word)} 🏆")
                break
        else:
            print(f"\n💀 Game Over! You've run out of attempts. The correct word was: '{chosen_word}' 😢")
    
    @staticmethod
    def play_quiz():
        print("🧠🎉 Welcome to the Quiz Challenge! 🎉🧠\n")
        print("📜 How to Play:")
        print("✅ Answer multiple-choice questions.")
        print("✅ Each correct answer earns you 1 point. 🏆")
        print("✅ No negative marking for incorrect answers. ❌")
        print("✅ Your total score will be displayed at the end. 📊\n")

        quiz = [
            {
                "question": "🌍 What is the capital of France?",
                "options": ["a) Berlin", "b) Madrid", "c) Paris", "d) Rome"],
                "answer": "c"
            },
            {
                "question": "💻 Which programming language is used for web development?",
                "options": ["a) Python", "b) JavaScript", "c) C++", "d) Ruby"],
                "answer": "b"
            },
            {
                "question": "🪐 What is the largest planet in our solar system?",
                "options": ["a) Earth", "b) Mars", "c) Jupiter", "d) Venus"],
                "answer": "c"
            },
            {
                "question": "🔬 Which element has the chemical symbol 'O'?",
                "options": ["a) Oxygen", "b) Gold", "c) Osmium", "d) Iron"],
                "answer": "a"
            },
            {
                "question": "🥑 What is the main ingredient in guacamole?",
                "options": ["a) Tomato", "b) Avocado", "c) Cucumber", "d) Onion"],
                "answer": "b"
            }
        ]

        score = 0

        for index, value in enumerate(quiz, start=1):
            print(f"\n❓ Question {index}: {value['question']}")
            for option in value['options']:
                print(option)

            # Loop until a valid input is entered
            while True:
                user_input = input("\n🔠 Enter your answer (a, b, c, or d): ").lower()
                if len(user_input) == 1 and user_input in ['a', 'b', 'c', 'd']:
                    break  # Exit loop when the input is valid
                else:
                    print("⚠️ Invalid choice! Please enter a valid option (a, b, c, or d).")

            if user_input == value['answer']:
                print("🎉 Correct! You earned a point. 🏅")
                score += 1
                print(f"🔢 Your current score: {score}")
            else:
                print("❌ Oops! Wrong answer. No points this time.")

        print(f"\n🎊 Quiz Completed! 🎊")
        print(f"📊 Your final score: {score}/{len(quiz)} ✅")

# # Call the games here
# Games.play_lottery()
# Games.play_number_guessing()
# Games.play_rock_paper_scissors()
# Games.play_hangman()
# Games.play_quiz()
