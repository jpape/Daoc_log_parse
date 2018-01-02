
GOLD_PICKUP_MESSAGE = 'You pick up'
# [19:04:48] You pick up 1 gold, 5 silver and 61 copper pieces.
GOLD_FOR_KILL_MESSAGE = 'for this kill'
# [21:45:03] You get 54 silver and 63 copper pieces for this kill.
MONEY_RECEIVED_MESSAGE = 'gives you'
# [15:04:51] Galdur Bonsavoir gives you 25 silver pieces for 2 earthen distill.
MONEY_SPENT_MESSAGE = 'You just bought'
# [15:05:42] You just bought an ancient treant wood for 20 silver pieces.

MELEE_OFFENSE_ATTACK_MESSAGE = 'You attack'
MELEE_OFFENSE_WEAPON_ATTACK_MESSAGE = 'with your'
# [19:41:05] You attack the cave trow with your Grim Maul and hit for 96 damage!
MELEE_OFFENSE_ATTACK_EVADE_MESSAGE = 'evades your attack'
# [21:51:25] Thatguy evades your attack!

CASTER_OFFENSE_ATTACK_MESSAGE = 'You hit'
# [21:57:40] You hit Aser for 269 (-14) damage! //Casted damage
# [19:40:26] You hit the cave trow for 75 damage! //Proc damage
CASTER_OFFENSE_SPELL_RESIST_MESSAGE = 'resists the effect'
# [21:57:59] Krok resists the effect!

CRITICAL_HIT_OFFENSE_MESSAGE = 'You critical hit the'
# [19:05:13] You critical hit the cave trow for an additional 41 damage!
CRITICAL_HIT_SPELL_MESSAGE = 'critical hit for'
# [21:57:19] You critical hit for an additional 41 damage!

MELEE_DEFENSE_BLOCK_MESSAGE = 'you block the blow'
# [19:05:20] The cave trow attacks you and you block the blow!
MELEE_DEFENSE_PARRY_MESSAGE = 'you parry the blow'
# [19:05:17] The cave trow attacks you and you parry the blow!
MELEE_DEFENSE_EVADE_MESSAGE = 'you evade the blow'
# [19:05:28] The cave trow attacks you and you evade the blow!
MELEE_DEFENSE_DAMAGE_RECEIVED_MESSAGE = 'hits your'
# [21:36:46] Krok hits your leg with his bright arcanium fortified mace for 102 damage!
MELEE_DEFENSE_OPPONENT_MISS_MESSAGE = 'attacks you and misses'
# [21:35:46] Krok attacks you and misses!
MELEE_DEFENSE_OPPONENT_CRIT_MESSAGE = 'critical hits you for an additional'
# [21:51:42] Dacy critical hits you for an additionnal 19 damage!

CASTER_DEFENSE_SPELL_RESISTED_MESSAGE = 'You resist the effect'
# [21:45:12] You resist the effect!

HEALING_RECEIVED_MESSAGE = 'You are healed by'
# [21:57:56] You are healed by Norseiaw for 85 hit points.

def collapse_comments():
    print('boo')
    # if sys.argv[1] == 'help':
    #         print(("Available options are: \nmeleeCombat, \ncasterCombat, \nMainhand <weaponName>, " +
    #             "\nCrit, \nDefense, \nallCombat, \nMoney, \nlootMoney, \nallMoney, \nAll"))
    #     elif len(sys.argv) > 2:
    #         readf = open('./Log Files/' + sys.argv[1], 'r')
    #         if sys.argv[2] == "meleeCombat":
    #             parse_melee_combat(readf)
    #         elif sys.argv[2] == "casterCombat":
    #             parse_caster_combat(readf)
    #         elif sys.argv[2] == "Mainhand":
    #             parse_mainhand(readf, sys.argv[3])
    #         elif sys.argv[2] == 'Crit':
    #             parse_crit(readf)
    #         elif sys.argv[2] == 'Defense':
    #             parse_defense(readf)
    #         elif sys.argv[2] == 'allCombat':
    #             parse_allCombat(readf)
    #         elif sys.argv[2] == "Money":
    #             parse_money(readf)
    #         elif sys.argv[2] == 'lootMoney':
    #             parse_gold_loot(readf)
    #         elif sys.argv[2] == 'allMoney':
    #             parse_allMoney(readf)
    #         elif sys.argv[2] == 'All':
    #             parse_all(readf)
    #         elif sys.argv[2] == 'help':
    #             print(("Available options are: \nmeleeCombat, \ncasterCombat, \nMainhand <weaponName>, " +
    #                    "\nCrit, \nDefense, \nallCombat, \nMoney, \nlootMoney, \nallMoney, \nAll"))
    #         readf.close()
    #     else:
    #         print("No method for parsing indicated topic. Please use argument 'help' for a list of available arguments.")

##region Money Matters

def parse_cash_flow(readf):
    # [positive_inc, negative_inc]
    trade_money = parse_trade_money(readf)
    # [looted_money]
    loot_money = parse_loot_money(readf)
    return [trade_money[0], trade_money[1], loot_money]

def parse_trade_money(readf):
    """Counts the money paid/received."""
    readf.seek(0)
    money_spent = 0
    money_gained = 0
    for line in readf:
        if line.find('gives you') != -1:
            money_gained = parse_money_denomination_from_line(line)
        elif line.find('You just bought') != -1:
            money_spent = parse_money_denomination_from_line(line)
    plus_money = currency_breakdown(money_gained)
    minus_money = currency_breakdown(money_spent)
    return [plus_money, minus_money]

def parse_loot_money(readf):
    """Prints out lines for gold loot picked up from mobs."""
    readf.seek(0)
    money_looted = 0
    for line in readf:
        if line.find('You pick up') != -1 or line.find('for this kill') != -1:
            money_looted = parse_money_denomination_from_line(line)
    total_loot = currency_breakdown(money_looted)
    return total_loot

def parse_money_denomination_from_line(line):
    """Finds each currency denomination and breaks it all down to copper"""
    money_total = 0
    if line.find('plat') != -1:
        plat_text = line[line.find('plat')-4:line.find('gold')]
        money_total += 10000000 * int(plat_text.split()[line(plat_text.split())-1])
    if line.find('gold') != -1:
        gold_text = line[line.find('gold')-4:line.find('gold')]
        money_total += 10000 * int(gold_text.split()[len(gold_text.split())-1])
    if line.find('silver') != -1:
        money_total += 100 * int(line[line.find('silver')-3:line.find('silver')-1])
    if line.find('copper') != -1:
        money_total += int(line[line.find('copper')-3:line.find('copper')-1])

    return money_total

def currency_breakdown(total):
    """Helper method to parse_money. Seperates 'total' into largest denominations and returns them in a list."""
    plat = total/10000000
    gold = (total%10000000)/10000
    silver = (total%10000)/100
    copper = (total%100)
    return [plat, gold, silver, copper]
##endregion


##region All Things Combat
def parse_combat(readf):
    # [hits, misses, evades, parries, blocks, damage]
    melee_attack = parse_melee_attack(readf)
    # [hits, resists, damage]
    caster_combat = parse_caster_attack(readf)
    # [blocks, parries, evades, misses, resists, hits, crits, crit_damage, total_damage, total_attacks]
    defense_combat = parse_defense_combat(readf)
    return [melee_attack, caster_combat, defense_combat]

def parse_melee_attack(readf):
    """Counts and returns the # of successful attacks with both hands"""
    readf.seek(0)
    hit_count = 0
    total_damage = 0
    #TODO: What do these look like?
    miss_count = 0 
    evade_count = 0
    parry_count = 0
    block_count = 0

    for line in readf:
        try:
            if line.find('You attack') != -1 and line.find('with your') != -1:
                hit_count += 1
                damage_text = line[line.find('damage')-16:line.find('damage')]
                # If there's a damage augment (resist or weakness) it changes the offset
                if line.find('-') != -1 or line.find('+') != -1:
                    total_damage += int(damage_text.split()[len(damage_text.split())-2])
                else:
                    total_damage += int(damage_text.split()[len(damage_text.split())-1])
        except IndexError:
            print(str(line))
            exit(0)
    return [hit_count, miss_count, evade_count, parry_count, block_count, total_damage]

def parse_caster_attack(readf):
    """Parses the log file for casting statistics"""
    readf.seek(0)
    spells_landed = 0
    resist_count = 0
    total_damage = 0
    for line in readf:
        try:
            if line.find('You hit') != -1 and line.find('you attack') == -1:
                spells_landed += 1
                damage_text = line[line.find('damage')-16:line.find('damage')]

                if line.find('-') != -1 or line.find('+') != -1:
                    total_damage += int(damage_text.split()[len(damage_text.split())-2])
                else:
                    total_damage += int(damage_text.split()[len(damage_text.split())-1])
            if line.find('resists the effect') != -1:
                resist_count += 1
        except IndexError:
            print(str(line))
            exit(0)
    return [spells_landed, resist_count, total_damage]

def parse_defense_combat(readf):
    """Counts # blocks, # misses, # parries, # evades, # hits taken. Prints results, along with %'s."""

    readf.seek(0)
    # Get critical hits in here somewhere
    block_count = 0
    parry_count = 0
    evade_count = 0
    hits_count = 0
    total_damage = 0
    total_attacks = 0
    miss_count = 0
    resist_count = 0
    crit_count = 0
    crit_damage = 0
    try:
        for line in readf:
            
            if MELEE_DEFENSE_BLOCK_MESSAGE in line:
                block_count +=1
            elif MELEE_DEFENSE_PARRY_MESSAGE in line:
                parry_count +=1
            elif MELEE_DEFENSE_EVADE_MESSAGE in line:
                evade_count +=1
            elif CASTER_DEFENSE_SPELL_RESISTED_MESSAGE in line:
                resist_count += 1
            elif MELEE_DEFENSE_OPPONENT_MISS_MESSAGE in line:
                miss_count += 1
            elif MELEE_DEFENSE_DAMAGE_RECEIVED_MESSAGE in line:
                hits_count +=1
                damage_text = line[line.find('damage')-9:line.find('damage')]
                if line.find('-') != -1 or line.find('+') != -1:
                    total_damage += int(damage_text.split()[len(damage_text.split())-2])
                else:
                    total_damage += int(damage_text.split()[len(damage_text.split())-1])
            elif MELEE_DEFENSE_OPPONENT_CRIT_MESSAGE in line:
                crit_count += 1
                damage_text = line[line.find('damage')-9:line.find('damage')]
                crit_damage += int(damage_text.split()[len(damage_text.split())-1])
        total_attacks = block_count + parry_count + evade_count + hits_count + miss_count
        # print("Defensive statistics:\n")
        # print("Total attacks received: " + str(total_attacks))
        # if total_attacks != 0:
        #     print(("Block count: " + str(block_count) + "\n\tBlock %: " + str((float(block_count))/(float(total_attacks))) +
        #             "\nParry count: " + str(parry_count) + "\n\tParry %: " + str((float(parry_count))/(float(total_attacks)))+
        #             "\nEvade Count " + str(evade_count) + "\n\tEvade %: " + str((float(evade_count))/(float(total_attacks)))+
        #             "\nMiss count: " + str(miss_count) + "\n\tMiss %: " + str((float(miss_count))/(float(total_attacks))) +
        #             "\nHits taken: " + str(hits_count)) + "\n\tHit %: " + str((float(hits_count))/(float(total_attacks))) + "\nTotal damage taken: " + str(total_damage) + "\n")
    except ValueError or IndexError:
        print(line)
        exit(0)
    return [block_count, parry_count, evade_count, miss_count, resist_count, hits_count, crit_count, crit_damage, total_damage, total_attacks]

def parse_crit(readf):
    """Counts and returns the # of critical hits inflicted"""
    readf.seek(0)
    crit_count = 0
    crit_damage = 0
    for line in readf:
        if line.find('You critical hit') != -1:
            crit_count += 1
            damage_text = line[line.find('damage')-9:line.find('damage')]
            crit_damage += int(damage_text.split()[len(damage_text.split())-1])
    return [crit_count, crit_damage]


def parse_mainhand(line, weaponName):
    """Counts # of attacks made with user-input 'weaponName'."""
    mainhand_count = 0
    print(weaponName)
    if line.find('with your ' + weaponName) != -1:
        mainhand_count += 1
    print("# of mainhand hits: " + str(mainhand_count))
##endregion


def main() :
    try:
        with open('./Log Files/Thid.log', 'r') as readf:
            cash_flow = parse_cash_flow(readf)
            print('$$$$ CASH FLOW $$$$')
            print('Money looted: ' + currency_print_helper(cash_flow[2]))
            print('Money spent: ' + currency_print_helper(cash_flow[1]))
            print('Money received: ' + currency_print_helper(cash_flow[0]))
            print('\n\n')
            
            combat = parse_combat(readf)
            print('=|====> COMBAT DATA <====|=')
            print('----> Offensive stats: <----')
            print('===[] Melee []===')
            print('Hits: ' + str(combat[0][0]))
            print('Misses: ' + str(combat[0][1]))
            print('Evades: ' + str(combat[0][2]))
            print('Parries: ' + str(combat[0][3]))
            print('Blocks: ' + str(combat[0][4]))
            print('Damage: ' + str(combat[0][5]))
            print('\n')

            print('**** Casting/proc stats ****')
            print('Hits: ' + str(combat[1][0]))
            print('Resists: ' + str(combat[1][1]))
            print('Total damage: ' + str(combat[1][2]))
            print('\n')

            print('||||| Defensive stats |||||')
            print('Blocks: ' + str(combat[2][0]))
            print('Parries: ' + str(combat[2][1]))
            print('Evades: ' + str(combat[2][2]))
            print('Misses: ' + str(combat[2][3]))
            print('Resists: ' + str(combat[2][4]))
            print('Hits: ' + str(combat[2][5]))
            print('Crits: ' + str(combat[2][6]))
            print('Crit dmg: ' + str(combat[2][7]))
            print('Total dmg: ' + str(combat[2][8]))
            print('Total attacks: ' + str(combat[2][9]))
            print('\n\n')



    except IOError:
        print("Failed to open file")

def currency_print_helper(currency_dict):
    result_text = ''
    if currency_dict[0] > 0:
        result_text += str(currency_dict[0]) + 'p '
    if currency_dict[1] > 0:
        result_text += str(currency_dict[0]) + 'g '
    if currency_dict[2] > 0:
        result_text += str(currency_dict[0]) + 's '
    if currency_dict[3] > 0:
        result_text += str(currency_dict[0]) + 'c '
    
    return result_text

main()