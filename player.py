execfile('dealer.py')

def compute_probs_stand(cards,p,dealer_card,sum_cards,split_aces):
	probs_player = [0]*3 # win lose draw
	if sum_cards == 0:
		sum_ = soft_sum(cards)
	else:
		sum_ = sum_cards
	if sum_ <= 16:
		probs_player[0] = probabilities[dealer_card-1][-1]
		probs_player[1] = 1 - probs_player[0]
	elif sum_ == 17:
		probs_player[2] = probabilities[dealer_card-1][4]
		probs_player[0] = probabilities[dealer_card-1][-1]
		probs_player[1] = 1 - probs_player[0] - probs_player[2]
	elif sum_ == 18:
		probs_player[2] = probabilities[dealer_card-1][3] 
		probs_player[0] = probabilities[dealer_card-1][-1] + probabilities[dealer_card-1][4]
		probs_player[1] = 1 - probs_player[0] - probs_player[2]
	elif sum_ == 19:
		probs_player[2] = probabilities[dealer_card-1][2]
		probs_player[0] = probabilities[dealer_card-1][-1] + probabilities[dealer_card-1][3] + probabilities[dealer_card-1][4] # 22 or 18
		probs_player[1] = 1 - probs_player[0] - probs_player[2]
	elif sum_ == 20:
		probs_player[2] = probabilities[dealer_card-1][1]
		probs_player[0] = probabilities[dealer_card-1][-1] + probabilities[dealer_card-1][3] + probabilities[dealer_card-1][2] + probabilities[dealer_card-1][4]
		probs_player[1] = 1 - probs_player[0] - probs_player[2]
	elif sum_ == 21:
		# TO_DO: case of black-jack
		if ((cards == [1,10]) or (cards == [10,1])):	# case of blackjack
			if split_aces:
				probs_player[1] = probabilities[dealer_card-1][-2] 
				probs_player[2] = probabilities[dealer_card-1][0] 
				probs_player[0] = (1 - probs_player[2] - probs_player[1])

			else:
				probs_player[2] = probabilities[dealer_card-1][-2]
				probs_player[0] = 1.5*(1 - probs_player[2])
				probs_player[1] = 0	
		else:
			probs_player[2] = probabilities[dealer_card-1][0]
			probs_player[1] = probabilities[dealer_card-1][-2]
			probs_player[0] = 1 - probs_player[2] - probs_player[1]
	else:
		probs_player[1] = 1
	return probs_player

def getPossibleAction(state,is_d,split_aces):
	if is_d:
		return ["S"]
	if split_aces:
		return ["S"]
	if soft_sum(state) < 21:
		actions = ["S","H"]
	else:
		return ["S"]
	if len(state) == 2:
		actions.append("D")
		if state[1] == state[0]:
			actions.append("P")
	return actions

data = []
for i in range(0,23):
	temp_i =[]
	for j in range(0,10):
		temp_j = []
		for k in range(0,2):
			temp_k = []
			for l in range(0,2):
				temp_l = []
				for m in range(0,2):
					temp_m = []
					for n in range(0,2):
						temp_n = []
						for o in range(0,2):
							temp_n.append(None)
						temp_m.append(temp_n)
					temp_l.append(temp_m)
				temp_k.append(temp_l)
			temp_j.append(temp_k)
		temp_i.append(temp_j)
	data.append(temp_i)


def value(state,p,dealer_card,is_d,split_aces):
	global data
	k_ = 0
	l_ = 0
	n_ = 0
	m_ = 0
	i_ = sum(state)
	if 1 in state:
		k_ = 1
		i_ = i_-1
	if len(state) == 1:
		l_ = 1
	elif len(state) == 2:
		n_ = 1
		if state[0] == state[1]:
			m_ = 1
	if i_ > 21:
		i_ = 22
	if state == [1,10]:
		i_ = 21
	elif state == [10,1]:
		i_ = 21
	if is_d:
		o_ = 1
	else:
		o_ = 0
	if data[i_-1][dealer_card-1][k_][l_][m_][n_][o_] != None:
		return data[i_-1][dealer_card-1][k_][l_][m_][n_][o_]

	probs = []					# I mean reward
	actions = getPossibleAction(state, is_d,split_aces)
	for action in actions:
		is_double = False
		if action == "D":
			is_double = True

		if action == "S":
			prob_win_lose = compute_probs_stand(state,p,dealer_card,0,split_aces)
			la = (prob_win_lose[0] - prob_win_lose[1])
			if is_d:
				probs.append(2*la)
			else:
				probs.append(la)

		elif action == "P":
			to_return = 0
			ravi = False
			if state == [1,1]:
				ravi = True
			for i in range(10):
				if i != state[0]-1:
					if i != 9:
						to_return += 2.0*((1-p)/9.0)*value([state[0]]+[i+1],p,dealer_card,is_double,ravi)[1]		# update_the_equations
					else:
						to_return += 2.0*p*value([state[0]]+[i+1],p,dealer_card,is_double,ravi)[1]
			if state[0] == 10:
				to_return = (to_return/(1.0-(2.0*p)))
			else:
				to_return = (to_return/(1.0-(2.0*(1-p)/9.0)))
			probs.append(to_return)

		else:
			to_return = 0
			for i in range(10):
				if i != 9:
					to_return += ((1-p)/9.0)*(value(state+[i+1],p,dealer_card, is_double,split_aces)[1])
				else:
					to_return += (p)*(value(state+[10],p,dealer_card, is_double,split_aces)[1])
			probs.append(to_return)
	data[i_-1][dealer_card-1][k_][l_][m_][n_][o_] = (actions[probs.index(max(probs))], max(probs))

	return (actions[probs.index(max(probs))], max(probs))


states = [[2,3],[2,4],[2,5],[2,6],[2,7],[2,8],[2,9],[3,9],[4,9],[5,9],[6,9],[7,9],[8,9],[8,10],[9,10],[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[1,9],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9],[10,10],[1,1]]

for i in range(len(states)):
	if i <= 14:
		to_print = str(i+5) 
	elif i <= 22:
		to_print = "A"+str(states[i][1])
	elif i == 32:
		to_print = "AA"
	else:
		to_print = 2*str(states[i][1])
	to_print = to_print + '\t'
	for j in range(9):
		to_print = to_print + str(value(states[i],given,j+2,False,False)[0]) + " "
	if i == len(states)-1:
		sys.stdout.write(to_print + str(value(states[i],given,1,False,False)[0])	)
	else:
		print to_print + str(value(states[i],given,1,False,False)[0])


