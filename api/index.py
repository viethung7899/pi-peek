from os.path import join

from flask import Flask, Response

app = Flask(__name__)

def preload():
    print('Preloading...')
    with open(join('data', 'pi-million.txt'), 'r') as f:
        return f.read()

data = preload()  
length = len(data)
RANGE = 5

@app.route('/find/<digits>', methods=['GET'])
def hello(digits: str):
    # Check all characters is digit
    for c in digits:
        if not c.isdigit():
            return Response(f'Input must be a string of numbers', 400)
    # Find index of digits
    index = data.find(digits)
    if (index < 0):
        return {
            'length': length,
            'before': '',
            'between': '',
            'after': f'3.{data[:10]}...'
        }
    
    # Get before and after
    beforeStart = max(index - RANGE, 0)
    before = data[beforeStart: index]
    if beforeStart > 0:
        before = f'...{before}'
    else:
        before = f'3.{before}'
    afterStart = min(index + len(digits), length)
    afterEnd = min(afterStart + RANGE, length)
    after = f'{data[afterStart: afterEnd]}...'
    
    return {
        'length': length,
        'index': index,
        'before': before,
        'between': digits,
        'after': after
    }

