import copy
import random

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

count = [0,0,0,0,0,0,0,0,0,0]

def evaluate_you_won(you1,you2, opp1,opp2, com_cards):
	global count
	cards1 = copy.deepcopy(com_cards + [you1] + [you2])
	cards2 = copy.deepcopy(com_cards + [opp1] + [opp2])

	op1 = straight_flush(cards1) 
	op2 = straight_flush(cards2)
	if op1 > op2:
		count[0]+=1
		return 2
	if op2 > op1:
		return 0

	op1 = four_of_a_kind(cards1) 
	op2 = four_of_a_kind(cards2)
	if op1 > op2:
		count[1]+=1
		return 2
	if op2 > op1:
		return 0

	op1 = full_house(cards1) 
	op2 = full_house(cards2)
	if op1 > op2:
		count[2]+=1
		return 2
	if op2 > op1:
		return 0

	op1 = flush(cards1) 
	op2 = flush(cards2)
	if op1 > op2:
		count[3]+=1
		return 2
	if op2 > op1:
		return 0

	op1 = straight(cards1) 
	op2 = straight(cards2)
	if op1 > op2:
		count[4]+=1
		return 2
	if op2 > op1:
		return 0

	op1 = three_of_a_kind(cards1) 
	op2 = three_of_a_kind(cards2)
	if op1 > op2:
		count[5]+=1
		return 2
	if op2 > op1:
		return 0

	op1 = two_pair(cards1) 
	op2 = two_pair(cards2)
	
	if op1[0] > op2[0] or (op1[0]==op2[0] and op1[1]>op2[1]):
		count[6]+=1
		return 2
	if op2[0] > op1[0] or (op1[0]==op2[0] and op1[1]<op2[1]):
		return 0


	op1 = pair(cards1) 
	op2 = pair(cards2)
	if op1[0] > op2[0] or (op1[0]==op2[0] and op1[1]>op2[1]):
		count[7]+=1
		return 2
	if op2[0] > op1[0] or (op1[0]==op2[0] and op1[1]<op2[1]):
		return 0

	op1 = high(cards1) 
	op2 = high(cards2)
	if op1 > op2:
		count[8]+=1
		return 2
	if op2 > op1:
		return 0

	count[9]+=1
	return 1

def evaluate_perc(you1,you2, opp1,opp2, com_cards):
	global count
	cards1 = copy.deepcopy(com_cards + [you1] + [you2])

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


def calculate_percentage(cards, first, second, rounds=30000):
	count = 0
	for i in range(rounds):
		round_cards = copy.deepcopy(cards)
		op1 = random.choice(round_cards)
		round_cards.remove(op1)
		op2 = random.choice(round_cards)
		round_cards.remove(op2)
		com_cards = [0,0,0,0,0]
		for i in range(5):
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
#total_games = 10000
#hands = 2598960
#perc = all_calculate_percentage(all_cards, total_games)
#print(*["StraFlu", "4 Kind", "FullHou", "Flush", "Street", "3 Kind", "2 Pair", "1 Pair", "HighCard"], sep='\t')
#print(*count[:9], sep='\t')
#print(*[int(40.0/hands*total_games), int(total_games/4164), int(total_games/693), int(total_games/508), int(total_games/254), int(total_games/46), int(total_games/20), int(total_games/1.37), int(total_games)], sep='\t')

while True:
	cards = copy.deepcopy(all_cards)
	com_cards = [0,0,0,0,0]
	print("Your Cards")
	first = get_tuble_cards(input())
	second = get_tuble_cards(input())
	cards.remove(first)
	cards.remove(second)

	perc = calculate_percentage(cards, first, second)
	print(perc)
	print(count)
	continue

	action = "Raise"
	print(action)

	print("River Cards")

	com_cards[0] = get_tuble_cards(input())
	com_cards[1] = get_tuble_cards(input())
	com_cards[2] = get_tuble_cards(input())
	cards.remove(com_cards[0])
	cards.remove(com_cards[1])
	cards.remove(com_cards[2])

	action = "Raise"
	print(action)

	print("Flop Cards")

	com_cards[3] = get_tuble_cards(input())
	cards.remove(com_cards[3])

	action = "Raise"
	print(action)

	print("Final Cards")
	
	com_cards[4] = get_tuble_cards(input())
	cards.remove(com_cards[4])


	action = "Raise"
	print(action)
	print(cards)
