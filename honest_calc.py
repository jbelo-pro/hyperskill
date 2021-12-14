# write your code here
from re import match, compile
msg_0 = "Enter an equation"
msg_1 = "Do you even know what numbers are? Stay focused!"
msg_2 = "Yes ... an interesting math operation. You've slept through all classes, haven't you?"
msg_3 = "Yeah... division by zero. Smart move..."
msg_4 = "Do you want to store the result? (y / n):"
msg_5 = "Do you want to continue calculations? (y / n):"
msg_6 = " ... lazy"
msg_7 = " ... very lazy"
msg_8 = " ... very, very lazy"
msg_9 = "You are"

def number(n):
	intpat = compile('^-?[0-9]+$')
	floatpat = compile('^-?[0-9]+.[0-9]?$')
	if match(intpat, str(n)):
		return int(n)
	if match(floatpat, str(n)):
		return int(float(n)) if  float(n).is_integer() else float(n)


def single_digit(v):
	return isinstance(v, int) and -10 < v < 10


def check(oper, x, y):
	msg = ''
	if single_digit(x) and single_digit(y):
		msg = msg + msg_6
	if (x == 1 or y == 1) and oper == '*':
		msg = msg + msg_7
	if (x == 0 or y == 0) and oper in ['*', '+', '-']:
		msg = msg + msg_8
	if msg != '':
		msg = msg_9 + msg
		print(msg)


def is_one_digit(v):
	msg = ["Are you sure? It is only one digit! (y / n)",
		   "Don't be silly! It's just one number! Add to the memory? (y / n)",
		   "Last chance! Do you really want to embarrass yourself? (y / n)"]
	for m in msg:
		print(m)
		r = input()
		if r == 'n':
			return False
	else:
		return True



def main():
	operators = ['+', '-', '*', '/']
	memory = 0
	while True:
		print(msg_0)
		calc:list = input().split(' ')
		equ0 = memory if calc[0] == 'M' else calc[0]
		equ2 = memory if calc[2] == 'M' else calc[2]
		x = number(equ0)
		oper = calc[1]
		y = number(equ2)
		if x is None or y is None:
			print(msg_1)
			continue
		if oper not in operators:
			print(msg_2)
			continue
		check(oper, x, y)
		result = None
		match oper:
			case '+':
				result = x + y
			case '-':
				result = x - y
			case '*':
				result = x * y
			case '/':
				if y == 0:
					print(msg_3)
					continue
				result = x / y
		print(float(result))
		print(msg_4)
		r = input()
		if r == 'y':
			if single_digit(result):
				if is_one_digit(result):
					memory = result
			else:
				memory = result
		print(msg_5)
		r1 = input()
		if r1 == 'y':
			continue
		break


if __name__ == '__main__':
    main()