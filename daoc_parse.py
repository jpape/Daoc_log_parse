import sys

## Counts the money paid/received.
def parse_money(openFile):
    money_spent = 0
    money_gained = 0
    for line in openFile:
        if line.find('gives you') != -1:
            ## price starts at char #38
            if line.find('plat') != -1:
                plat_text = line[line.find('plat')-4:line.find('gold')]
                money_gained += 10000000 * int(plat_text.split()[line(plat_text.split())-1])
            if line.find('gold') != -1:
                gold_text = line[line.find('gold')-4:line.find('gold')]
                money_gained += 10000 * int(gold_text.split()[len(gold_text.split())-1])
            if line.find('silver') != -1:
                money_gained += 100 * int(line[line.find('silver')-3:line.find('silver')-1])
            if line.find('copper') != -1:
                money_gained += int(line[line.find('copper')-3:line.find('copper')-1])
        elif line.find('You just bought') != -1:
            if line.find('plat') != -1:
                plat_text = line[line.find('plat')-4:line.find('gold')]
                money_spent += 10000000 * int(plat_text.split()[line(plat_text.split())-1])
            if line.find('gold') != -1:
                gold_text = line[line.find('gold')-4:line.find('gold')]
                money_spent += 10000 * int(gold_text.split()[len(gold_text.split())-1])
            if line.find('silver') != -1:
                money_spent += 100 * int(line[line.find('silver')-3:line.find('silver')-1])
            if line.find('copper') != -1:
                money_spent += int(line[line.find('copper')-3:line.find('copper')-1])
    plus_money = currency_breakdown(money_gained)
    minus_money = currency_breakdown(money_spent)
    print "Money gained: "+ str(plus_money[0]) + 'p ' + str(plus_money[1]) + 'g ' + str(plus_money[2]) + 's ' + str(plus_money[3]) + 'c'
    print "Money spent: "+ str(minus_money[0]) + 'p ' + str(minus_money[1]) + 'g ' + str(minus_money[2]) + 's ' + str(minus_money[3]) + 'c'
    if plus_money > minus_money:
        net_income = currency_breakdown(money_gained-money_spent)
        print "Net income: "+ str(net_income[0]) + 'p ' + str(net_income[1]) + 'g ' + str(net_income[2]) + 's ' + str(net_income[3]) + 'c'
    else:
        net_income = currency_breakdown(money_spent-money_gained)
        print "Net income: "+ str(net_income[0]) + 'p ' + str(net_income[1]) + 'g ' + str(net_income[2]) + 's ' + str(net_income[3]) + 'c'


## Prints out lines for gold loot picked up from mobs.
def parse_gold_loot(openFile):
    money_looted = 0
    for line in openFile:
        if line.find('You pick up') != -1:
            ## price starts at char #38
            if line.find('plat') != -1:
                plat_text = line[line.find('plat')-4:line.find('gold')]
                money_looted += 10000000 * int(plat_text.split()[line(plat_text.split())-1])
            if line.find('gold') != -1:
                gold_text = line[line.find('gold')-4:line.find('gold')]
                money_looted += 10000 * int(gold_text.split()[len(gold_text.split())-1])
            if line.find('silver') != -1:
                money_looted += 100 * int(line[line.find('silver')-3:line.find('silver')-1])
            if line.find('copper') != -1:
                money_looted += int(line[line.find('copper')-3:line.find('copper')-1])
    total_loot = currency_breakdown(money_looted)
    print "Total loot money: "+ str(total_loot[0]) + 'p ' + str(total_loot[1]) + 'g ' + str(total_loot[2]) + 's ' + str(total_loot[3]) + 'c'

## Helper method to parse_money. Seperates 'total' into largest denominations and returns them in a list.
def currency_breakdown(total):
    plat = total/10000000
    gold = (total%10000000)/10000
    silver = (total%10000)/100
    copper = (total%100)
    return [plat, gold, silver, copper]
            
## Counts and returns the # of successful attacks with both hands
def parse_combat(openFile):
    hit_count = 0
    for line in openFile:
        if line.find('You attack') != -1:
##                print line
            hit_count += 1
    print "# of hits: " +str(hit_count)
    return hit_count
        
## Counts and returns the # of critical hits inflicted with either hand.
def parse_crit(openFile):
    crit_count = 0
    for line in openFile:
        if line.find('You critical hit') != -1:
##                print line
            crit_count += 1
    print "# of crits: " + str(crit_count)
    return crit_count

## Counts # of attacks made with user-input 'weaponName'.
def parse_mainhand(openFile, weaponName):
    mainhand_count = 0
    print weaponName
    for line in openFile:
        if line.find('with your ' + weaponName) != -1:
            mainhand_count += 1
    print "# of mainhand hits: " + str(mainhand_count)


## Counts # blocks, # misses, # parries, # evades, # hits taken. Prints results, along with %'s.
def parse_defense(openFile):
    block_count = 0
    parry_count = 0
    evade_count = 0
    hits_taken = 0
    misses = 0
    for line in openFile:
        if line.find('you block the blow') != -1:
            block_count +=1
        elif line.find('you parry the blow') != -1:
            parry_count +=1
        elif line.find('you evade the blow') != -1:
            evade_count +=1
        elif line.find('hits your') != -1:
            hits_taken +=1
        elif line.find('attacks you and misses') != -1:
            misses += 1
        total_attacks = block_count + parry_count + evade_count + hits_taken + misses
    print "Total attacks received: " + str(total_attacks)
    print ("Block count: " + str(block_count) + "\n\tBlock %: " + str((float(block_count))/(float(total_attacks))) +
           "\nParry count: " + str(parry_count) + "\n\tParry %: " + str((float(parry_count))/(float(total_attacks)))+
           "\nEvade Count " + str(evade_count) + "\n\tEvade %: " + str((float(evade_count))/(float(total_attacks)))+
           "\nMiss count: " + str(misses) + "\n\tMiss %: " + str((float(misses))/(float(total_attacks))) +
           "\nHits taken: " + str(hits_taken)) + "\n\tHit %: " + str((float(hits_taken))/(float(total_attacks))) + "\n"


## Executes parse_combat, parse_crit, and parse_defense.
def parse_allCombat(openFile):
    hit_count = parse_combat(openFile)
    openFile.seek(0)
    crit_count = parse_crit(openFile)
    print "Crit %: " + str(float(crit_count)/float(hit_count)) + "\n"
    openFile.seek(0)
    parse_defense(openFile)

## Executes parse_money and parse_gold_loot.
def parse_allMoney(openFile):
    parse_money(openFile)
    print "\n"
    openFile.seek(0)
    parse_gold_loot(openFile)

## Executes parse_allCombat and parse_allMoney.
def parse_all(openFile):
    print "Combat statistics: "
    parse_allCombat(openFile)
    openFile.seek(0)
    print "Financial statistics: "
    parse_allMoney(openFile)
    
def main() :
    try:
        readf = open(sys.argv[1], 'r')
        if sys.argv[2] == "Combat":
            parse_combat(readf)
        elif sys.argv[2] == "Mainhand":
            parse_mainhand(readf, sys.argv[3])
        elif sys.argv[2] == 'Crit':
            parse_crit(readf)
        elif sys.argv[2] == 'Defense':
            parse_defense(readf)
        elif sys.argv[2] == 'allCombat':
            parse_allCombat(readf)
        elif sys.argv[2] == "Money":
            parse_money(readf)
        elif sys.argv[2] == 'lootMoney':
            parse_gold_loot(readf)
        elif sys.argv[2] == 'allMoney':
            parse_allMoney(readf)
        elif sys.argv[2] == 'All':
            parse_all(readf)
        else:
            print "No method for parsing indicated topic."
    except IOError:
        print "Failed to open "+ sys.argv[1]
    readf.close()

main()
