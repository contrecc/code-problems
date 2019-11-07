# Calculate the minimum number and allotment of coins needed to make change for a certain amount of cents.
# First solution min_coins_greedy is a greedy algorithm that fails some test cases.
# Second solution min_coins_thrifty calls min_coins_greedy internally to check for edge cases.

# Coin denominations available to use
coins = [25, 10, 5, 1]

def calculate_LCM(coins):
    '''
    Calculate the least common multiple of a list of numbers
    '''
    from math import gcd
    lcm = coins[0]
    for i in coins[1:]: 
        lcm = int(lcm * i / gcd(lcm, i))
    return lcm        

def min_coins_greedy(cents, coins):
    '''
    Inputs:
    cents - Number - the number of cents to make change for
    coins - List - the coin denominations available to use
    
    Outputs:
    coin_counts - Dictionary - the greedily calculated minimum allotment of coin denominatoins to add up to cents
    
    Example: min_coins_greedy(47, [25, 10, 5, 1]) returns {'25': 1, '10': 2, '5': 0, '1': 2, 'num_coins': 5}

    Notes:
    Greedy algorithm fails for edge cases like min_coins_greedy(30, [25, 10, 1]) returning {"25": 1, "10": 0, "1": 5, "num_coins": 6}. The correct answer is {"25": 0, "10": 3, "1": 0, "num_coins": 3}.
    Fails for some cases where always using high denomination coins results in more total coins needed.
    '''
    coin_counts = { str(coin): 0 for coin in coins }
    coin_counts["num_coins"] = 0

    lcm = calculate_LCM(coins)

    if cents >= lcm:
        multiples = cents // lcm
        remainder = cents % lcm
        num_largest_coin = multiples * lcm // coins[0]
        coin_counts[str(coins[0])] += num_largest_coin
        coin_counts["num_coins"] += num_largest_coin
        cents = remainder
    
    for coin in coins:
        new_coins_needed = cents // coin
        coin_counts[str(coin)] += new_coins_needed
        coin_counts["num_coins"] += new_coins_needed
        cents = cents % coin
        if cents == 0:
            break
    
    return coin_counts

def min_coins_thrifty(cents, coins):
    '''
    Inputs:
    cents - Number - the number of cents to make change for
    coins - List - the coin denominations available to use
    
    Outputs:
    final_coin_counts - Dictionary - the calculated minimum allotment of coin denominatoins to add up to cents
    
    Example: min_coins_thrifty(47, [25, 10, 5, 1]) returns {'25': 1, '10': 2, '5': 0, '1': 2, 'num_coins': 5}

    Notes:
    For each coin denomination, min_coins_thrifty calls min_coins_greedy to check whether avoiding using higher denomination coins results in fewer total coins needed.
    '''
    final_coin_counts = { str(coin): 0 for coin in coins }
    final_coin_counts["num_coins"] = float("Inf")

    lcm = calculate_LCM(coins)

    if cents >= lcm:
        multiples = cents // lcm
        remainder = cents % lcm
        num_largest_coin = multiples * lcm // coins[0]
        final_coin_counts[str(coins[0])] += num_largest_coin
        final_coin_counts["num_coins"] = num_largest_coin

        if remainder == 0:
            return final_coin_counts

        for i in range(len(coins)):
            coin_counts = min_coins_greedy(remainder, coins[i:])

            if i == 0:
                final_coin_counts = coin_counts.copy()
                final_coin_counts[str(coins[0])] += num_largest_coin
                final_coin_counts["num_coins"] += num_largest_coin
            elif coin_counts["num_coins"] < final_coin_counts["num_coins"]:
                final_coin_counts = coin_counts.copy()
            
        return final_coin_counts
    else:
        for i in range(len(coins)): 
            coin_counts = min_coins_greedy(cents, coins[i:])
            
            if coin_counts["num_coins"] < final_coin_counts["num_coins"]:
                final_coin_counts = coin_counts.copy()
    
        return final_coin_counts


# Test cases
print("min_coins_greedy fails test case where we want change for 30 cents but do not have nickels")
print("30", min_coins_greedy(30, [25, 10, 1]))
print("min_coins_thrifty fixes this failed test case")
print("30", min_coins_thrifty(30, [25, 10, 1]))#
print("\n")

print("min_coins_greedy fails test case where we want change for 21 cents with denominations [18, 7, 1]")
print("21", min_coins_greedy(21, [18, 7, 1]))
print("min_coins_thrifty fixes this failed test case")
print("21", min_coins_thrifty(21, [18, 7, 1]))
print("\n")

## Other test cases
print("min_coins_thrifty test cases")
print("47 cents with [25, 10, 5, 1] coins", min_coins_thrifty(47, coins))
print("26 cents with [25, 10, 5, 1] coins", min_coins_thrifty(26, coins))
print("13 cents with [25, 10, 5, 1] coins", min_coins_thrifty(13, coins))
print("11 cents with [25, 10, 5, 1] coins", min_coins_thrifty(11, coins))
print("0 cents with [25, 10, 5, 1] coins", min_coins_thrifty(0, coins))
print("2 cents with [25, 10, 5, 1] coins", min_coins_thrifty(2, coins))
print("\n")

print("min_coins_thrifty test cases for large numbers of cents to make change for")
print("276 cents with [26, 18, 7, 3, 1] coins", min_coins_thrifty(276, [26, 18, 7, 3, 1]))
print("24000 cents with [25, 10, 5, 1])", min_coins_thrifty(24000, [25, 10, 5, 1]))