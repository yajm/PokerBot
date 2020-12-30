import copy
import random
import json
import numpy as np
from sklearn.preprocessing import Normalizer




def analysis(X, y, weight, current):
    if y.count(1) == 0 or y.count(0)==0:
        return .5
    X, y, weight, current = map(np.array, (X, y, weight, current))

    norm = Normalizer()
    X = norm.fit_transform(np.array(X)) * weight
    current = norm.transform(current.reshape(-1,1)) * weight

    d0 = np.linalg.norm(current-np.mean(X[np.where(y==0)],axis=0))
    d1 = np.linalg.norm(current-np.mean(X[np.where(y==1)],axis=0))
    return d0/(d0+d1)

"""
all_cards = []

for i in ["h", "t", "c", "p"]:
	for j in range(2, 10):
		all_cards.append(str(j)+i)
	for j in ["t", "y", "q", "k", "a"]:
		all_cards.append(j+i)
"""

def get_tuble_cards(as_string):
	if as_string[1]=="h":
		second=0
	elif as_string[1]=="t":
		second=1
	elif as_string[1]=="c":
		second=2
	elif as_string[1]=="p":
		second=3
	else:
		raise ValueError("This card color is not available")


	if as_string[0]=="2":
		first=2
	elif as_string[0]=="3":
		first=3
	elif as_string[0]=="4":
		first=4
	elif as_string[0]=="5":
		first=5
	elif as_string[0]=="6":
		first=6
	elif as_string[0]=="7":
		first=7
	elif as_string[0]=="8":
		first=8
	elif as_string[0]=="9":
		first=9
	elif as_string[0]=="t":
		first=10
	elif as_string[0]=="y":
		first=11
	elif as_string[0]=="q":
		first=12
	elif as_string[0]=="k":
		first=13
	elif as_string[0]=="a":
		first=14
	else:
		raise ValueError("This color value is not available")

	return (first, second)

def to_non_color(cards):
	return [i[0] for i in cards]

def to_non_number(cards):
	return [i[1] for i in cards]


def longest_sequence(nums):
	nums = sorted(to_non_color(set(nums)))
	max_cnt = 0
	max_num = 0
	cnt=0
	last_num=-1
	if 14 in nums:
		nums.insert(0, 1)
	for num in nums:
		if num==last_num+1:
			cnt+=1
			if cnt > max_cnt:
				max_cnt = cnt
				max_num = num
		elif num>last_num+1:
			cnt=1
		last_num=num
	return max_cnt, max_num

def find_same_card(nums):
	nums = to_non_color(nums)
	same_counter = {}
	for i in nums:
		if i in same_counter:
			same_counter[i]+= 1
		else:
			same_counter[i]=1
	return same_counter

def straight_flush(cards):
	street = straight(cards)
	if street==0:
		return 0

	new_cards = []
	for i in cards:
		if street-4<=i[0]<=street:
			new_cards.append(i)
	if flush(new_cards) > 0:
		return street
	return 0

def flush(cards):
	non_num = to_non_number(cards)
	most_freq = max(set(non_num), key = non_num.count)
	if non_num.count(most_freq)<5:
		return 0
	cards = [i for i in cards if i[1]==most_freq]
	score = 0
	for i in range(5):	
		high_c = high(cards)
		score += (14**(4-i))*high_c
		for j in cards:
			if j[0]==high_c:
				cards.remove(j)
	return score


def four_of_a_kind(cards):
	count_dict = find_same_card(cards)
	max_count = max(count_dict, key=count_dict.get)
	if count_dict[max_count]==4:
		return max_count
	else:
		return 0

def full_house(cards):
	max_value = three_of_a_kind(cards)
	if max_value == 0:
		return 0
	cards = [i for i in cards if i[0]!=max_value]
	value = pair(cards)
	if value[0] > 0:
		return max_value
	else:
		return 0

def straight(cards):
	seq, max_value = longest_sequence(cards)
	if seq >= 5:
		return max_value
	else:
		return 0

def three_of_a_kind(cards):
	count_dict = find_same_card(cards)
	max_count = max(count_dict, key=count_dict.get)
	if count_dict[max_count]==3:
		#print([i for i in cards if max_count==i[0]])
		return max_count
	else:
		return 0

def two_pair(cards):
	max_count, high = pair(cards)
	if max_count==0:
		return 0, 0
	cards = [i for i in cards if i[0]!=max_count]
	max_count2, high2 = pair(cards)
	if max_count2>0:
		return max_count, high2
	else:
		return 0, 0


def pair(cards):
	count_dict = find_same_card(cards)
	max_count = max(count_dict, key=count_dict.get)
	if count_dict[max_count]==2:
		cards = [i for i in cards if i[0]!=max_count]
		return max_count, high(cards)
	else:
		return 0, 0


def high(cards):
	return max(to_non_color(cards))


def evaluate_you_won(you1,you2, opp1,opp2, com_cards):

	cards1 = copy.deepcopy(com_cards + [you1] + [you2])
	cards2 = copy.deepcopy(com_cards + [opp1] + [opp2])

	op1 = straight_flush(cards1) 
	op2 = straight_flush(cards2)
	if op1 > op2:
		return 2
	if op2 > op1:
		return 0

	op1 = four_of_a_kind(cards1) 
	op2 = four_of_a_kind(cards2)
	if op1 > op2:

		return 2
	if op2 > op1:
		return 0

	op1 = full_house(cards1) 
	op2 = full_house(cards2)
	if op1 > op2:
		return 2
	if op2 > op1:
		return 0

	op1 = flush(cards1) 
	op2 = flush(cards2)
	if op1 > op2:
		return 2
	if op2 > op1:
		return 0

	op1 = straight(cards1) 
	op2 = straight(cards2)
	if op1 > op2:
		return 2
	if op2 > op1:
		return 0

	op1 = three_of_a_kind(cards1) 
	op2 = three_of_a_kind(cards2)
	if op1 > op2:
		return 2
	if op2 > op1:
		return 0

	op1 = two_pair(cards1) 
	op2 = two_pair(cards2)
	
	if op1[0] > op2[0] or (op1[0]==op2[0] and op1[1]>op2[1]):
		return 2
	if op2[0] > op1[0] or (op1[0]==op2[0] and op1[1]<op2[1]):
		return 0


	op1 = pair(cards1) 
	op2 = pair(cards2)
	if op1[0] > op2[0] or (op1[0]==op2[0] and op1[1]>op2[1]):
		return 2
	if op2[0] > op1[0] or (op1[0]==op2[0] and op1[1]<op2[1]):
		return 0

	op1 = high(cards1) 
	op2 = high(cards2)
	if op1 > op2:
		return 2
	if op2 > op1:
		return 0

	return 1

def evaluate_perc(you1,you2, opp1,opp2, com_cards):
	global count
	cards1 = copy.deepcopy(com_cards + [you1] + [you2])
	print(cards1)

	op1 = straight_flush(cards1) 
	if op1 > 0:
		print("StraightFlush", cards1)
		count[0]+=1

	op1 = four_of_a_kind(cards1) 
	if op1 > 0:
		print("4 Kind", cards1)
		count[1]+=1

	op1 = full_house(cards1) 
	if op1 > 0:
		print("Full House", cards1)
		count[2]+=1

	op1 = flush(cards1) 
	if op1 > 0:
		print("Flush", cards1)
		count[3]+=1

	op1 = straight(cards1) 
	if op1 > 0:
		print("Street", cards1)
		count[4]+=1

	op1 = three_of_a_kind(cards1) 
	if op1 > 0:
		print("3 Kind", cards1)
		count[5]+=1

	op1 = two_pair(cards1) 
	if op1[0] > 0:
		print("2 Pair", cards1)
		count[6]+=1


	op1 = pair(cards1) 
	if op1[0] > 0:
		count[7]+=1

	op1 = high(cards1) 
	if op1 > 0:
		count[8]+=1

	count[9]+=1
	return 1

def all_calculate_percentage(cards, rounds=100000):
	count_per = 0
	for i in range(rounds):
		round_cards = copy.deepcopy(cards)
		first = random.choice(round_cards)
		round_cards.remove(first)
		second = random.choice(round_cards)
		round_cards.remove(second)
		com_cards = [0,0,0,0,0]
		for i in range(5):
			com_cards[i] = random.choice(round_cards)
			round_cards.remove(com_cards[i])
		count_per += evaluate_perc(first, second, 0, 0, com_cards)

	return 1.0*count_per/(2*rounds)


def calculate_percentage(cards, first, second, com_cards, index_start, rounds=140000):
	count = 0
	for i in range(rounds):
		round_cards = copy.deepcopy(cards)
		op1 = random.choice(round_cards)
		round_cards.remove(op1)
		op2 = random.choice(round_cards)
		round_cards.remove(op2)
		for i in range(index_start, 5):
			com_cards[i] = random.choice(round_cards)
			round_cards.remove(com_cards[i])
		count += evaluate_you_won(first, second, op1, op2, com_cards)

	return 1.0*count/(2*rounds)
	


all_cards = []

for i in range(4):
	for j in range(2, 15):
		all_cards.append((j, i))


# print(evaluate_you_won((10,0), (11,0),(3,0),(4,0), [(12,0), (13,0), (14,0), (3,3), (2,2)]))
# print(count)
#total_games = 400000
#hands = 2598960
#perc = all_calculate_percentage(all_cards, total_games)
#print(*["StraFlu", "4 Kind", "FullHou", "Flush", "Street", "3 Kind", "2 Pair", "1 Pair", "HighCard"], sep='\t')
#print(*count[:9], sep='\t')
#print(*[int(40.0/hands*total_games), int(total_games*0.00168067227), int(total_games/693), int(total_games/508), int(total_games/254), int(total_games/46), int(total_games/20), int(total_games/1.37), int(total_games)], sep='\t')
turn = True
sb = 0.5
bb = 1
chris_bank = 500
yannick_bank = 500
chris_pot = 0
yannick_pot = 0
games_played = 0


def find_threeshold(perc, level, chris_paid, yannick_bank, yannick_pot, chris_bank, chris_pot):
	global log_book_unknown_chris_card, log_book_known_chris_card
	weights = [0.4, 0.1, 0.3,0.2,0.1,0]

	win = []
	added_to_win = []
	for k in range(int(yannick_bank*2)):
		to_add = k/2
		added_to_win.append(to_add)
		y=[]
		for i in log_book_known_chris_card[level]:
			if i[5]==3:
				y.append(1)
			elif i[5]==4:
				y.append(0)
		known_win = analysis(log_book_known_chris_card[level], y, weights, [perc,yannick_bank-chris_pot+yannick_pot-to_add, chris_pot, chris_pot+to_add, chris_paid, 0])

		y=[]
		for i in log_book_unknown_chris_card[level]:
			if i[5]==1:
				y.append(1)
			elif i[5]==2:
				y.append(0)
		unknown_win = analysis(log_book_unknown_chris_card[level], y, weights, [perc,yannick_bank-chris_pot+yannick_pot-to_add, chris_pot, chris_pot + to_add, chris_paid, 0])

		win.append(0.7*known_win+0.3*unknown_win)
	return win, added_to_win


def calculate(games_played, perc, level, chris_paid, yannick_bank, yannick_pot, chris_bank, chris_pot):
	bluff = [0.1,0.3,0.5,0.01]
	
	win, added_to_win = find_threeshold(perc, level, chris_paid, yannick_bank, yannick_pot, chris_bank, chris_pot)

	if games_played<10 or (perc>0.5 and win[0]==0.5):
		to_pay = chris_pot - yannick_pot
		if 1 < to_pay < 10:
			return to_pay, win[0]
		else:
			return 1, win[0]

	if win[0] < 0.5:
		if random.random() < bluff[level]*win[0]:
			win, added_to_win = find_threeshold(0.8, level, chris_paid, yannick_bank, yannick_pot, chris_bank, chris_pot)
		else:
			return 0, win[0]

	default_bet = int(1.5 * (chris_pot+yannick_pot))/2
	risky_bet = default_bet

	for i in win:
		if win[i] > 0.5: # Error: numpy.float64 Why
			risky_bet = chris_pot-yannick_pot+added_to_win[threeshold]

	
	to_call = chris_pot - yannick_pot
	bet = 0 
	if perc>0.6:
		if random.random()>0.9:
			bet = min(default_bet, risky_bet)
		else:
			bet = max(default_bet, risky_bet)

		final_bet = min(max(to_call, bet), yannick_bank)
	else:
		if random.random()*0.5 < bluff[level]*win[0]:
			final_bet = to_call
		else:
			final_bet = 0

	return final_bet, win[0]


def log_book_update(log_book, number):
	for i in log_book:
		for j in i:
			j[5]=number
	return log_book


log_book_current_round = [[],[],[],[]]
if True:
	log_book_known_chris_card = [[[0.5,0, 500, 500, 250, 4]],[[0.5,0, 500, 500, 250, 4]],[[0.5,0, 500, 500, 250, 4]],[[0.5,0, 500, 500, 250, 4]]]
	log_book_unknown_chris_card = [[[0.5,0, 500, 500, 250, 4]],[[0.5,0, 500, 500, 250, 4]],[[0.5,0, 500, 500, 250, 4]],[[0.5,0, 500, 500, 250, 4]]]
else:
	with open("log_book_known_chris_card.txt", "r") as fp:
		log_book_unknown_chris_card = json.load(fp)
	with open("log_book_unknown_chris_card.txt", "r") as fp:
		log_book_unknown_chris_card = json.load(fp)


def ask_for_raise(ask_string):
	try_again = True
	while try_again:
		try:
			paid = float(input(ask_string))
			try_again = False
		except:
			pass
	return paid


def pay_money(games_played, turn, perc, level, bb, sb, chris_bank, yannick_bank, chris_pot, yannick_pot):
	global log_book_current_round
	chris_paid = 0
	while True:
		if turn:
			if chris_pot==0:
				chris_paid = sb
			else:
				chris_paid = ask_for_raise("Chris raises by how much: ")
			chris_bank-= chris_paid
			chris_pot+= chris_paid
			# if chris_paid>0:
			log_book_current_round[level].append([perc,yannick_bank, chris_pot, yannick_pot, chris_paid, 0])
			if chris_pot < yannick_pot:
				log_book_current_round = log_book_update(log_book_current_round, 1)
				return chris_bank, yannick_bank+yannick_pot+chris_pot, 0, 0, True
			if yannick_pot==0:
				yannick_paid=bb
			else:
				suggestion, win_prob = calculate(games_played, perc, level, chris_paid, yannick_bank, yannick_pot, chris_bank, chris_pot)
				print("Yannick should pay: ", suggestion, "## Win Probability by Card: ", perc, "## Win Chance by previous Games", win_prob)
				yannick_paid = ask_for_raise("Yannick raises by how much: ")
			yannick_bank-= yannick_paid
			yannick_pot+= yannick_paid
			if yannick_pot < chris_pot:
				log_book_current_round = log_book_update(log_book_current_round, 2)
				return chris_bank+yannick_pot+chris_pot, yannick_bank, 0, 0, True
		else:
			if yannick_pot==0:
				yannick_paid=sb
			else:
				suggestion, win_prob = calculate(games_played, perc, level, chris_paid, yannick_bank, yannick_pot, chris_bank, chris_pot)
				print("Yannick should pay: ", suggestion, "## Win Probability by Card: ", perc, "## Win Chance by previous Games", win_prob)
				yannick_paid = ask_for_raise("Yannick raises by how much: ")
			yannick_bank-= yannick_paid
			yannick_pot+= yannick_paid
			if yannick_pot < chris_pot:
				log_book_current_round = log_book_update(log_book_current_round, 2)
				return chris_bank+yannick_pot+chris_pot, yannick_bank, 0, 0, True
			if chris_pot==0:
				chris_paid = bb
			else:
				chris_paid = ask_for_raise("Chris raises by how much: ")
			chris_bank-= chris_paid
			chris_pot+= chris_paid
			# if chris_paid>0:
			log_book_current_round[level].append([perc,yannick_bank, chris_pot, yannick_pot, chris_paid, 0])
			if chris_pot < yannick_pot:
				log_book_current_round = log_book_update(log_book_current_round, 1)
				return chris_bank, yannick_bank+yannick_pot+chris_pot, 0, 0, True

		print("Chris Bank: ", chris_bank, "Yannick Bank: ", yannick_bank, "Chris Pot: ", chris_pot, "Yannick Pot: ", yannick_pot)
		
		if int(round(2*chris_pot,0))==int(round(2*yannick_pot,0)):
			break

	return chris_bank, yannick_bank, chris_pot, yannick_pot, False

def ask_for_card(ask_string):
	try_again = True
	while try_again:
		try:
			card = get_tuble_cards(input(ask_string))
			try_again = False
		except:
			pass
	return card


while True:
	cards = copy.deepcopy(all_cards)
	com_cards = [0,0,0,0,0]
	turn = not turn
	games_played+=1

	if len(log_book_current_round[0])>0:
		if log_book_current_round[0][0][5]==1 or log_book_current_round[0][0][5]==2:
			log_book_unknown_chris_card = [aa+bb for aa, bb in zip(log_book_unknown_chris_card, log_book_current_round)]
			with open("logs/log_book_unknown_chris_card_{}.txt".format(games_played), "w") as fp:
				json.dump(log_book_unknown_chris_card, fp)
		else:
			log_book_known_chris_card = [aa+bb for aa, bb in zip(log_book_known_chris_card, log_book_current_round)]
			with open("logs/log_book_known_chris_card_{}.txt".format(games_played), "w") as fp:
				json.dump(log_book_known_chris_card, fp)
		log_book_current_round = [[],[],[],[]]


	print("### NEW ROUND ###")
	print("Chris Bank: ", chris_bank, "Yannick Bank: ", yannick_bank, "Chris Pot: ", chris_pot, "Yannick Pot: ", yannick_pot)

	first = ask_for_card("First Card: ")
	second = get_tuble_cards(input("Second Card: "))
	cards.remove(first)
	cards.remove(second)

	perc = calculate_percentage(cards, first, second, com_cards, 0, 1000)
	
	chris_bank, yannick_bank, chris_pot, yannick_pot, stop = pay_money(games_played, turn, perc, 0, bb, sb, chris_bank, yannick_bank, chris_pot, yannick_pot)	
	if stop:
		continue
	print("Flop Cards")

	com_cards[0] = ask_for_card("Flop 1: ")
	com_cards[1] = ask_for_card("Flop 2: ")
	com_cards[2] = ask_for_card("Flop 3: ")
	cards.remove(com_cards[0])
	cards.remove(com_cards[1])
	cards.remove(com_cards[2])

	perc = calculate_percentage(cards, first, second, com_cards, 3, 1000)

	
	chris_bank, yannick_bank, chris_pot, yannick_pot, stop = pay_money(games_played, turn, perc, 1, bb, sb, chris_bank, yannick_bank, chris_pot, yannick_pot)	
	if stop:
		continue
	print("Turn Cards")

	com_cards[3] = ask_for_card("Turn: ")
	cards.remove(com_cards[3])

	perc = calculate_percentage(cards, first, second, com_cards, 4, 1000)

	chris_bank, yannick_bank, chris_pot, yannick_pot, stop = pay_money(games_played, turn, perc, 2, bb, sb, chris_bank, yannick_bank, chris_pot, yannick_pot)	
	if stop:
		continue
	print("River Cards")
	
	com_cards[4] = ask_for_card("River: ")
	cards.remove(com_cards[4])


	perc = calculate_percentage(cards, first, second, com_cards, 5, 1000)

	chris_bank, yannick_bank, chris_pot, yannick_pot, stop = pay_money(games_played, turn, perc, 3, bb, sb, chris_bank, yannick_bank, chris_pot, yannick_pot)	
	if stop:
		continue
	chris1 = ask_for_card("Chris Card 1: ")
	chris2 = ask_for_card("Chris Card 2: ")

	winner = evaluate_you_won(first, second, chris1, chris2, com_cards)
	if winner==2:
		print("Yannick won this round")
		yannick_bank+=chris_pot+yannick_pot
		log_book_current_round = log_book_update(log_book_current_round, 3)
	elif winner==0:
		print("Chris won this round")
		chris_bank+=chris_pot+yannick_pot
		log_book_current_round = log_book_update(log_book_current_round, 4)
	else:
		print("Pot will be splited")
		yannick_bank+=yannick_pot
		chris_bank+=chris_pot
		# log_book_current_round = log_book_update(log_book_current_round, 5)

	yannick_pot=0
	chris_pot=0

