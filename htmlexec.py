from bs4 import BeautifulSoup
import sys
from colorama import *

def error(e):
  print(f'{Fore.RED}error: {Style.RESET_ALL}{e}')

file = open(sys.argv[1], 'r')
soup = BeautifulSoup(file.read(), 'html.parser')
i = 1

for el in soup.find_all():
    try:
        if i == 1 and el.name != 'html':
            error(f'couldn\'t find <html> tag')
            break
        if el.name == 'println':
            try:
                print(eval(el.string))
            except SyntaxError:
                print(el.string)
            except Exception as e:
                error(f'error when printing "{el.string}: {e}"')
        elif el.name == 'print':
            try:
                print(eval(el.string), end='')
            except SyntaxError:      
                print(el.string, end='')
            except Exception as e:
                error(f'error when printing "{el.string}: {e}"')
        elif el.name == 'var':
            try:
                try:
                    exec(f'{el["name"]} = {eval(el.string)}')
                except SyntaxError:
                    exec(f'{el["name"]} = "{el.string}"')
            except Exception as e:
                error(f'error while setting a variable {el["name"]}: {e}')
        elif el.name == 'input':
            if el["type"] == None:
                exec(f'{el["var"]} = input("{el["placeholder"]}")')
            else:
                exec(f'{el["var"]} = {el["type"]}(input("{el["placeholder"]}"))')
        elif el.name != 'html': 
            error(f'unknown tag "{el.name}"')
            break
        i+=1
    except Exception as e:
        error(e)