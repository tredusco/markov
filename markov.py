import pandas as pd
import random
import argparse

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("FILE", help="Sample of delimited ")
    parser.add_argument("-n", "--num", help="Number of names to generate. DEFAULT: 10", type=int, default=10)
    parser.add_argument("-s", "--sep", help="Field separator in CSV file. DEFAULT: ;", default=";")
    parser.add_argument("-c", "--col", help="Name of the column to use. DEFAULT: name", default="name")
    parser.add_argument("-t", "--temp", help="Temperature, integer for randomness of the results. DEFAULT: 3", type=int, default=3)
    args = parser.parse_args()
    return args.FILE, args.num, args.sep, args.col, args.temp

def build_markov_chain(data, n):
    chain = {
        '_initial':{},
        '_names': set(data)
    }
    for word in data:
        word_wrapped = str(word) + '.'
        for i in range(0, len(word_wrapped) - n):
            tuple = word_wrapped[i:i + n]
            next = word_wrapped[i + 1:i + n + 1]
            
            if tuple not in chain:
                entry = chain[tuple] = {}
            else:
                entry = chain[tuple]
            
            if i == 0:
                if tuple not in chain['_initial']:
                    chain['_initial'][tuple] = 1
                else:
                    chain['_initial'][tuple] += 1
                    
            if next not in entry:
                entry[next] = 1
            else:
                entry[next] += 1
    return chain 

def select_random_item(items):
    rnd = random.random() * sum(items.values())
    for item in items:
        rnd -= items[item]
        if rnd < 0:
            return item

def generate(chain):
    tuple = select_random_item(chain['_initial'])
    result = [tuple]
    
    while True:
        tuple = select_random_item(chain[tuple])
        last_character = tuple[-1]
        if last_character == '.':
            break
        result.append(last_character)
    
    generated = ''.join(result)
    if generated not in chain['_names']:
        return generated
    else:
        return generate(chain)

def main():
    file, num, sep, col, temp = parse()
    names = pd.read_csv(file, sep=sep)
    chain = build_markov_chain(names[col].tolist(), temp)
    print([generate(chain) for _ in range(num)])

if __name__ == "__main__":
    main()
