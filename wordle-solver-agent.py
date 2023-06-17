import asyncio
import sys
import pyautogui
import time
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAITextCompletion, OpenAIChatCompletion

boardX = 0
boardY = 0

kernel = sk.Kernel()
api_key, org_id = sk.openai_settings_from_dot_env()

kernel.add_chat_service("dv", OpenAIChatCompletion("gpt-4", api_key, org_id))

prompt = """
Wordle is a 5 letter word guessing game. Each letter in a guess will either be a correct letter in correct position (G) an invalid letter (X) or a correct letter present in the word but in a wrong position (Y). After each guess, we get a result

For example:
BAGEL
XXXGX

Here E is a valid letter in the final word and in the correct position.
You will get a list of previous guesses and its result. You will also get a word that has letters in correct position with unknown letters as '-'. Do not use invalid letters in the guess word. Do not reply with reasoning. Only reply with the guess word
The guess word should be a valid english word. 

{{$history}}

Invalid letters: {{$invalid_letters}}
Valid letters with positions: {{$valid_letter_word}}
Guess the correct 5 letter word.
Guess word:  """
wordle_guesser = kernel.create_semantic_function(prompt,  max_tokens=200, temperature=0.7)

context = kernel.create_new_context()
context["invalid_letters"] = ""
context["valid_letters"] = ""
context["history"] = ""
context["valid_letter_word"] = "-----"

# select wordle
def selectWordlePage():
    global boardX, boardY
    boardHeader = pyautogui.locateOnScreen('images/wordleLetterBoard.png')
    if boardHeader == None:
        raise Exception("Couldnt find wordle page on screen")
    boardX = boardHeader.left
    boardY = boardHeader.top
    x, y = pyautogui.center(boardHeader)
    pyautogui.click(x, y)

# write a word
def enterWord(word):
    pyautogui.write(word) 
    pyautogui.press('enter')

def observeScreen(row):
    if row > 6:
        raise Exception("Could not guess within limit!")
    y = boardY + (126 * (row - 1))
    im1 = pyautogui.screenshot(region=(boardX, y, 582, 126))
    letter1 = im1.getpixel((33, 33))
    letter2 = im1.getpixel((33+111, 33))
    letter3 = im1.getpixel((33+111*2, 33))
    letter4 = im1.getpixel((33+111*3, 33))
    letter5 = im1.getpixel((33+111*4, 33))
    resultStr = getColorLetter(letter1) + getColorLetter(letter2) + getColorLetter(letter3) + getColorLetter(letter4) + getColorLetter(letter5)

    if resultStr == "GGGGG":
        print("Wordle solver wins!")
        sys.exit(0)

    return resultStr

def getColorLetter(pixel):
    if pixel == (181,159,59):
        return "Y"
    elif pixel == (58,58,60):
        return "X"
    elif pixel == (83,141,78):
        return "G"
    else:
        raise Exception("couldnt identify color")

async def getWordFromLLM(last_guess, guess_result):
    sort_letters(last_guess, guess_result, context)
    updateValidLettersWord(last_guess, guess_result, context)
    updateHistory(last_guess, guess_result, context)
    bot_answer = await wordle_guesser.invoke_async(context=context)
    return bot_answer.result.strip()

def updateValidLettersWord(last_guess, guess_result, context):
    for i in range(len(last_guess)):
        if guess_result[i] == 'G':
            if context["valid_letter_word"][i] != last_guess[i]:
                context["valid_letter_word"] = context["valid_letter_word"][:i] + last_guess[i] + context["valid_letter_word"][i:]

def updateHistory(last_guess, guess_result, context):
    context["history"] += f"{last_guess}\n{guess_result}\n"

def sort_letters(last_guess, guess_result, context):
    for i in range(len(last_guess)):
        if guess_result[i] == 'G' or guess_result[i] == 'Y':
            if last_guess[i] not in context["valid_letters"]:
                context["valid_letters"] += f"{last_guess[i]} "
        else:
            if last_guess[i] not in context["invalid_letters"]:
                context["invalid_letters"] += f"{last_guess[i]} "

async def main():
    first_word = 'SALET' #good starting word
    selectWordlePage()
    enterWord(first_word)
    time.sleep(3)
    prevword = first_word
    
    for i in range(1,5):
        rowResult = observeScreen(i)
        guess_word = await getWordFromLLM(prevword, rowResult)
        enterWord(guess_word)
        print(guess_word)
        prevword = guess_word
        time.sleep(3)

    row6Result = observeScreen(6)
    print("Wordle solver fails :(")

asyncio.run(main())
