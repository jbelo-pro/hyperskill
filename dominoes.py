# Write your code here
import random
from re import match, compile


def create_domino_set():
	doset = []
	for n1 in range(0, 7):
		for n2 in range(0, 7):
			if n2 < n1:
				continue
			doset.append([n1,n2])
	return doset


def split_parts(doset: list):
	computer = []
	player = []
	commuter = True
	for p in range(0, 14):
		n = random.randint(0, len(doset) - 1)
		if commuter:
			computer.append(doset.pop(n))
		else:
			player.append(doset.pop(n))

		commuter = False if commuter else True

	return computer, player


def get_double_do(player):
	dd = None
	index = None
	for i in range(0,len(player) - 1):
		p = player[i]
		if p[0] == p[1]:
			if not dd or dd[0] < p[0]:
				dd = p
				index = i
	return dd, index


def select_starting(computer, player):

	ddcomp, indexcom = get_double_do(computer)
	ddpla, indexpla = get_double_do(player)

	if not ddcomp and not ddpla:
		return None
	if ddpla and not ddcomp:
		player.pop(indexpla)
		return 'computer', ddpla
	if ddcomp and not ddpla:
		computer.pop(indexcom)
		return 'player', ddcomp
	if ddcomp[0] > ddpla[0]:
		computer.pop(indexcom)
		return 'player', ddcomp
	if ddpla[0] > ddcomp[0]:
		player.pop(indexpla)
		return 'computer', ddpla


def domino_statistics(computer: list, snake: list):
	comvalues = [v for l in computer for v in l]
	snakevalues = [v for l in snake for v in l]
	scores = {i:0 for i in comvalues}
	for k in scores.keys():
		scores[k] = scores[k] + comvalues.count(k) + snakevalues.count(k)
	scorescom = {}
	for i in range(len(computer)):
		scorescom[i] = scores[computer[i][0]] + scores[computer[i][1]]
	scorescom = {x[0]: x[1] for x in
			  sorted(scorescom.items(), key= lambda x:x[1], reverse=True)}
	return scorescom


def computer_play(doset: list, computerset: list, snake: list):

	dummym = input()
	scores:dict = domino_statistics(computerset, snake)
	snakel = snake[0][0]
	snaker = snake[-1][1]

	for k, v in scores.items():
		if snakel in computerset[k]:
			place_domino('-', k, computerset, snake)
			break
		if snaker in computerset[k]:
			place_domino('+', k, computerset, snake)
			break
	else:
		if doset:
			computerset.append(doset.pop())


def validate_input(playerin, playerset):
	rexp = compile('^-?[1-9][0-9]?$')
	if not match(rexp, playerin):
		return False
	number = int(playerin[1:]) if playerin[0] == '-' else int(playerin)
	side = '-' if playerin[0] == '-' else '+'
	if number > len(playerset):
		return False
	return side, number


def place_domino(side, position, playerset, snake: list):
	domino: list = playerset.pop(position)
	snakedomino = snake[0][0] if side == '-' else snake[-1][1]
	if side == '-':
		if domino[1] != snakedomino:
			domino.reverse()
		snake.insert(0, domino)
	else:
		if domino[0] != snakedomino:
			domino.reverse()
		snake.insert(len(snake), domino)


def player_play(doset: list, playerset: list, snake: list):
	while True:
		m = input()
		if m == '0':
			if doset:
				playerset.append(doset.pop())
			break
		userchoice = validate_input(m, playerset)
		if not userchoice:
			print('Invalid input. Please try again.')
			continue
		side, position = userchoice
		if not validate_movement(side, position - 1, playerset, snake):
			print('Illegal move. Please try again.')
			continue
		place_domino(side, position -1, playerset, snake)
		break


def check_endgame(computerset: list, playerset: list, snake: list):
	winner = None
	if not computerset:
		winner = 'The game is over. The computer won!'
	elif not playerset:
		winner = 'The game is over. You won!'
	elif len(snake) > 1:
		if snake[0][0] == snake[-1][1]:
			c = 0
			for d in snake:
				if snake[0][0] == d[0]:
					c += 1
				if snake[0][0] == d[1]:
					c += 1
			if c == 8:
				winner = "The game is over. It's a draw!"
	return winner


def print_snake(snakedo):
	strsnake = ''
	if len(snakedo) > 6:
		for p in range(3):
			strsnake = strsnake + str(snakedo[p])
		strsnake = strsnake + '...'
		for p in range(-3, 0):
			strsnake = strsnake + str(snakedo[p])
	else:
		for p in snakedo:
			strsnake = strsnake + str(p)
	print(strsnake)


def validate_movement(side, position, dominoset, snake):
	domino = dominoset[position]
	snakedomino = snake[0][0] if side == '-' else snake[-1][1]
	if snakedomino not in domino:
		return False
	else:
		return True


def main():

	while True:
		domino_snake = []
		doset = create_domino_set()
		computer, player = split_parts(doset)
		stplay = select_starting(computer, player)
		if not stplay:
			continue
		domino_snake.append(stplay[1])
		nextplayer = stplay[0]

		while True:
			print('='*70)
			print(f'Stock size: {len(doset)}')
			print(f'Computer pieces: {len(computer)}\n')
			print_snake(domino_snake)
			print('\n')
			print('Your pieces:')
			for i in range(len(player)):
				print(f'{i + 1}:{player[i]}')
			print('\n')
			winner = check_endgame(computer, player, domino_snake)
			if winner:
				print(f'Status: {winner}')
				break

			if nextplayer == 'computer':
				print('Status: Computer is about to make a move. Press Enter to continue...')
				computer_play(doset,computer, domino_snake)
				nextplayer = 'player'

			else:
				print("Status: It's your turn to make a move. Enter your command.")
				player_play(doset, player, domino_snake)
				nextplayer = 'computer'
		break


if __name__ == '__main__':
	main()