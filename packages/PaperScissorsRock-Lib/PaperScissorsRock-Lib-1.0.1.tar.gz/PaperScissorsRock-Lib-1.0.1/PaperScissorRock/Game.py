# I Guess this is not cheating when you are tryin to make a paper scissors rock game in 1 lines...
import random

def play():
	while True:
		print("Paper, Scissors or Rock? (P/S/R)")
		option = input(">>>")
		option = option.lower()
		options = ["p", "s", "r"]
		if not option in options: 
			print("Option Does Not Exist")
		else:
			logic = {"p": "r", "r": "s", "s": "p"}
			bot_option = random.choice(options)
			if logic[option] == bot_option:
				print("U Win HAHA")
			elif logic[bot_option] == option:
				print("U Loose Haha")
			else:
				print("Its a draw")

			print(f"Bot chose {bot_option}")