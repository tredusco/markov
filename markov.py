import pandas as pd
import random
import argparse

# usage: markov.py [-h] [-n NUM] [-s SEP] [-c COL] [-t TEMP] [-cc CATEGORY] [-cn CATNAME] FILE

# positional arguments:
  # FILE                  Sample of delimited

# optional arguments:
  # -h, --help            show this help message and exit
  # -n NUM, --num NUM     Number of names to generate. DEFAULT: 10
  # -s SEP, --sep SEP     Field separator in CSV file. DEFAULT: ;
  # -c COL, --col COL     Name of the column to use. DEFAULT: name
  # -t TEMP, --temp TEMP  Temperature, integer for randomness of the results. DEFAULT: 3
  # -cc CATEGORY, --category CATEGORY
                        # Category to filter data. If not provided, not filtering is done.
  # -cn CATNAME, --catname CATNAME
                        # Category column name. DEFAULT: category
def parse():
	parser = argparse.ArgumentParser()
	parser.add_argument("FILE", help="Sample of delimited ")
	parser.add_argument("-n", "--num", help="Number of names to generate. DEFAULT: 10", type=int, default=10)
	parser.add_argument("-s", "--sep", help="Field separator in CSV file. DEFAULT: ;", default=";")
	parser.add_argument("-c", "--col", help="Name of the column to use. DEFAULT: name", default="name")
	parser.add_argument("-t", "--temp", help="Temperature, integer for randomness of the results. DEFAULT: 3", type=int, default=3)
	parser.add_argument("-cc", "--category", help="Category to filter data. If not provided, not filtering is done.", default="")
	parser.add_argument("-cn", "--catname", help="Category column name. DEFAULT: category", default="category")
	args = parser.parse_args()
	return args.FILE, args.num, args.sep, args.col, args.temp, args.category, args.catname

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

def generate_amount_by_category(data, category_column, category, name_column, n, temp):
	return generate_amount(data[data[category_column] == category], name_column, n, temp)

def generate_amount(data, name_column, n, temp):
	chain = build_markov_chain(data[name_column].tolist(), temp)
	return [generate(chain) for _ in range(n)]

def main():
	file, num, sep, col, temp, category, catname = parse()
	names = pd.read_csv(file, sep=sep)
	if category == "":
		print(generate_amount(names, col, num, temp))
	else:
		print(generate_amount_by_category(names, catname, category, col, num, temp))

if __name__ == "__main__":
	main()