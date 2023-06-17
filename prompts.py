prompt1 = """
Wordle is a 5 letter word guessing game. Each letter in a guess will either be a correct letter in correct position (G) an invalid letter (X) or a correct letter present in the word but in a wrong position (Y). After each guess, we get a result

For example:
BAGEL
XXXGX

Here E is a valid letter in the final word and in the correct position.
You will get a list of invalid letters and valid letters.
Do not use invalid letters in the guess word.
The guess word should be a valid english word.
Guess the correct 5 letter word.

Invalid letters: {{$invalid_letters}}
Valid letters: {{$valid_letters}}
Guess word:  """


prompt2 = """
Wordle is a 5 letter word guessing game. Each letter in a guess will either be a correct letter in correct position (G) an invalid letter (X) or a correct letter present in the word but in a wrong position (Y). After each guess, we get a result

For example:
BAGEL
XXXGX

Here E is a valid letter in the final word and in the correct position.
You will get a list of previous guesses and its result. You will also get a word that has letters in correct position with unknown letters as '-'
The guess word should be a valid english word.
Guess the correct 5 letter word.

{{$history}}

Valid letters with positions: {{$valid_letter_word}}
Guess word:  """

prompt3 = """
Wordle is a 5 letter word guessing game. Each letter in a guess will either be a correct letter in correct position (G) an invalid letter (X) or a correct letter present in the word but in a wrong position (Y). After each guess, we get a result

For example:
BAGEL
XXXGX

Here E is a valid letter in the final word and in the correct position.
Do not use invalid letters in the guess word.
The guess word should be a valid english word.
You will get a list of previous guesses and its result, invalid letters and valid letters.
Write your reasoning for what should be the guess word, then write the guess word in this format: GUESS->
Guess the correct 5 letter word.

{{$history}}

Invalid letters: {{$invalid_letters}}
Valid letters: {{$valid_letters}}
Reasoning:  """