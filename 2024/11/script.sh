aocd 11 2024 > input.real
# Unfortunately claude is somewhat stubborn and does not want to respond in python code only, it alwys adds some explanation and indents the code.
curl https://adventofcode.com/2024/day/11 | markdownify | hey this is an advent of code puzzle, please solve it in python. your whole response should be executable python code. all comments or explanations MUST BE part of the code. Your response should contain nothing but executable python code. The input to the puzzle will be piped into the script via stdin. > solve.py
cat input.real | python solve.py