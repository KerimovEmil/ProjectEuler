import os
import argparse
import sys
import requests
from bs4 import BeautifulSoup

def get_problem_description(n):
    url = f"https://projecteuler.net/problem={n}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            problem_content = soup.find('div', class_='problem_content')
            if problem_content:
                # Remove script and style tags
                for script in problem_content(["script", "style"]):
                    script.decompose()
                
                # Replace <br> with newlines
                for br in problem_content.find_all('br'):
                    br.replace_with('\n')
                
                # Replace <p> with newlines around content
                for p in problem_content.find_all('p'):
                    p.insert_before('\n')
                    p.insert_after('\n')
                
                # Extract text
                text = problem_content.get_text()
                
                # Clean up multiple newlines and spaces
                lines = [line.strip() for line in text.split('\n')]
                # Filter out multiple consecutive empty lines
                cleaned_lines = []
                for line in lines:
                    if line or (cleaned_lines and cleaned_lines[-1] != ''):
                        cleaned_lines.append(line)
                
                return '\n'.join(cleaned_lines).strip()
    except Exception as e:
        print(f"Warning: Could not fetch problem description: {e}")
    return "PROBLEM DESCRIPTION COULD NOT BE AUTOMATICALLY RETRIEVED."

TEMPLATE = """r\"\"\"
PROBLEM

{1}

ANSWER: 
Solve time: 
\"\"\"

import unittest
from util.utils import timeit


class Problem{0}:
    def __init__(self):
        pass

    @timeit
    def solve(self):
        raise NotImplementedError('Please implement this method!')


class Solution{0}(unittest.TestCase):
    def setUp(self):
        self.problem = Problem{0}()

    def test_solution(self):
        # Fill this in once you've got a working solution!
        self.assertEqual(1, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='What problem are you trying to solve?')
    parser.add_argument(
        'p',
        action='store',
        type=int,
        help="The integer representing the problem that you're trying to solve!")
    args = parser.parse_args()
    fn = f'PE{args.p}.py'
    if os.path.exists(f'./{fn}'):
        raise AssertionError(
            f'{fn} already exists! Just update the file you lazy bastard!')
    
    print(f"Fetching problem {args.p} description...")
    description = get_problem_description(args.p)
    
    with open(fn, 'w', encoding='utf-8') as f:
        f.write(TEMPLATE.format(args.p, description))

    print(f"Created {fn} with problem description.")
    sys.exit(0)
