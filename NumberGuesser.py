import random
import math

# Taking Inputs
lower = int(input("Enter lower bound:- "))

# Taking Inputs
upper = int(input("Enter upper bound:- "))

# Generating a random number between the upper and the lower
x = random.randint(lower, upper)
print("\n\tYou've only",
      round(math.log(upper - lower + 1, 2)),
      " chances to guess the integer!\n")

# Initializing the number of guesses.
count = 0

# For the calculation of the minimum number of guesses depends upon the range.
while count < math.log(upper - lower + 1, 2):
    count += 1

    # taking guessing number as input
    guess = int(input("Enter guess:- "))

    # Condition testing
    if x == guess:
        print("Congrats! You guessed the number!", count, "try")
        # Once guessed, loop should break.
        break
    elif x > guess:
        print("That's too small!")
    elif x < guess:
        print("That's too big!")

    # If Guessing is more than required guesses, shows this output.
    if count >= math.log(upper - lower + 1, 2):
        print("\nThe number is %d" % x)
        print("\tBetter Luck Next Time!")
