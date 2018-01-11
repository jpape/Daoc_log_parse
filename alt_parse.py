"""Opens a saved chatlog from Dark Age of Camelot and parses various numbers
    and stats from it"""
__author__ = "robert.pape"
__date__ = "2018/01/04"

import json
import operator

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
MELEE_OFFENSE_ATTACK_PARRY_MESSAGE = 'parries your attack'
MELEE_OFFENSE_ATTACK_BLOCK_MESSAGE = 'blocks your attack'
MELEE_OFFENSE_ATTACK_MISS_MESSAGE = 'you miss'

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
MELEE_DEFENSE_OPPONENT_CRIT_MESSAGE = 'critical hits you for an additionnal'
# [21:51:42] Dacy critical hits you for an additionnal 19 damage!
MELEE_DEFENSE_SPELL_PROC_MESSAGE = 'hits you for'
# [21:25:47] Aser hits you for 150 damage !
MELEE_BUFFER_ABSORB_MESSAGE = 'melee buffer absorbs'
# [18:54:28] Your melee buffer absorbs 25 damage!

CASTER_DEFENSE_SPELL_RESISTED_MESSAGE = 'You resist the effect'
# [21:45:12] You resist the effect!

HEALING_RECEIVED_MESSAGE = 'You are healed by'
# [21:57:56] You are healed by Norseiaw for 85 hit points.
HEALING_DELIVERED_MESSAGE = 'You heal'
# [21:38:30] You heal the skeletal commander for 158 hit points!
LIFETAP_HEALTH_STOLEN_MESSAGE = 'You steal'
# [21:44:57] You steal 109 hit points.


def parse_cash_flow(readf):
    """Parses money traded (received / payed) and looted"""
    money = {}
    trade_money = parse_trade_money(readf)
    money['Income'] = trade_money[0]
    money['Expense'] = trade_money[1]
    money['Loot'] = parse_loot_money(readf)
    return money

def parse_trade_money(readf):
    """Counts the money paid/received."""
    readf.seek(0)
    money_spent = 0
    money_gained = 0
    for line in readf:
        if MONEY_RECEIVED_MESSAGE in line:
            money_gained = parse_money_denomination(line)
        elif MONEY_SPENT_MESSAGE in line:
            money_spent = parse_money_denomination(line)
    plus_money = currency_breakdown(money_gained)
    minus_money = currency_breakdown(money_spent)
    return [plus_money, minus_money]

def parse_loot_money(readf):
    """Prints out lines for gold loot picked up from mobs."""
    readf.seek(0)
    money_looted = 0
    for line in readf:
        if GOLD_PICKUP_MESSAGE in line or GOLD_FOR_KILL_MESSAGE in line:
            money_looted += parse_money_denomination(line)
    total_loot = currency_breakdown(money_looted)
    return total_loot

def parse_money_denomination(line):
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
    """Helper method to parse_money. Seperates 'total' into
    largest denominations and returns them in a list."""
    plat = int(total/10000000)
    gold = int((total%10000000)/10000)
    silver = int((total%10000)/100)
    copper = int(total%100)
    return [plat, gold, silver, copper]



def parse_combat(readf):
    """Parses attack and defense values"""
    combat = {}
    combat['MeleeAttack'] = parse_melee_attack(readf)
    combat['CasterAttack'] = parse_caster_attack(readf)
    combat['Defense'] = parse_defense_combat(readf)

    return combat

def parse_melee_attack(readf):
    """Counts and returns the # of successful attacks with both hands"""
    readf.seek(0)
    result = {}
    targets = {}
    result['Targets'] = []
    result['Hits'] = 0
    result['BaseDamage'] = 0
    result['Crits'] = 0
    result['CritDamage'] = 0
    result['Evades'] = 0
    result['Parries'] = 0
    result['Blocks'] = 0
    #TODO: What does this look like?
    result['Misses'] = 0
    for line in readf:
        if MELEE_OFFENSE_ATTACK_MESSAGE in line and MELEE_OFFENSE_WEAPON_ATTACK_MESSAGE in line:
            result['Hits'] += 1
            damage_and_target = parse_damage_and_target(line)
            result['BaseDamage'] += damage_and_target[0]
            if damage_and_target[1] in targets.keys():
                targets[damage_and_target[1]] += damage_and_target[0]
            else:
                targets[damage_and_target[1]] = damage_and_target[0]
        elif CRITICAL_HIT_OFFENSE_MESSAGE in line:
            result['Crits'] += 1
            damage_and_target = parse_damage_and_target(line)
            result['CritDamage'] += damage_and_target[0]
            if damage_and_target[1] in targets.keys():
                targets[damage_and_target[1]] += damage_and_target[0]
            else:
                targets[damage_and_target[1]] = damage_and_target[0]
        elif MELEE_OFFENSE_ATTACK_EVADE_MESSAGE in line:
            result['Evades'] += 1
        elif MELEE_OFFENSE_ATTACK_PARRY_MESSAGE in line:
            result['Parries'] += 1
        elif MELEE_OFFENSE_ATTACK_BLOCK_MESSAGE in line:
            result['Blocks'] += 1
        elif MELEE_OFFENSE_ATTACK_MISS_MESSAGE in line:
            result['Misses'] += 1

    result['Targets'] = sorted(targets.items(), key=operator.itemgetter(1), reverse=True)

    result['TotalAttacks'] = result['Hits'] + result['Misses'] + \
        result['Evades'] + result['Parries'] + result['Blocks']
    result['TotalDamage'] = result['BaseDamage'] + result['CritDamage']
    return result

def parse_caster_attack(readf):
    """Parses the log file for casting statistics.
    This includes spells + procs until I figure out how to differentiate them."""
    readf.seek(0)
    result = {}
    targets = {}
    result['Targets'] = {}
    result['Landed'] = 0
    result['Crits'] = 0
    result['Resists'] = 0
    result['BaseDamage'] = 0
    result['CritDamage'] = 0
    for line in readf:
        if CASTER_OFFENSE_ATTACK_MESSAGE in line and MELEE_OFFENSE_ATTACK_MESSAGE not in line:
            result['Landed'] += 1
            damage_and_target = parse_damage_and_target(line)
            result['BaseDamage'] += damage_and_target[0]
            if damage_and_target[1] in targets.keys():
                targets[damage_and_target[1]] += damage_and_target[0]
            else:
                targets[damage_and_target[1]] = damage_and_target[0]
        elif CRITICAL_HIT_SPELL_MESSAGE in line:
            result['Crits'] += 1
            damage_and_target = parse_damage_and_target(line)
            result['CritDamage'] += damage_and_target[0]
            if damage_and_target[1] in targets.keys():
                targets[damage_and_target[1]] += damage_and_target[0]
            else:
                targets[damage_and_target[1]] = damage_and_target[0]
        elif CASTER_OFFENSE_SPELL_RESIST_MESSAGE in line:
            result['Resists'] += 1

    result['Targets'] = sorted(targets.items(), key=operator.itemgetter(1), reverse=True)

    result['TotalDamage'] = result['BaseDamage'] + result['CritDamage']
    result['TotalAttacks'] = result['Landed'] + result['Resists']
    return result

## TODO: Can we differentiate between spells and procs?
def parse_defense_combat(readf):
    """Parses attacks against the player."""
    readf.seek(0)
    result = {}
    sources = {}
    result['Sources'] = []
    result['Blocks'] = 0
    result['Parries'] = 0
    result['Evades'] = 0
    result['Hits'] = 0
    result['MeleeDamage'] = 0
    result['Misses'] = 0
    result['Resists'] = 0
    result['Crits'] = 0
    result['CritDamage'] = 0
    result['Absorbed'] = 0
    result['SpellsLanded'] = 0
    result['SpellDamage'] = 0
    for line in readf:
        if MELEE_DEFENSE_BLOCK_MESSAGE in line:
            result['Blocks'] += 1
        elif MELEE_DEFENSE_PARRY_MESSAGE in line:
            result['Parries'] += 1
        elif MELEE_DEFENSE_EVADE_MESSAGE in line:
            result['Evades'] += 1
        elif CASTER_DEFENSE_SPELL_RESISTED_MESSAGE in line:
            result['Resists'] += 1
        elif MELEE_DEFENSE_OPPONENT_MISS_MESSAGE in line:
            result['Misses'] += 1
        elif MELEE_DEFENSE_DAMAGE_RECEIVED_MESSAGE in line:
            result['Hits'] += 1
            damage_and_source = parse_damage_and_source(line)
            result['MeleeDamage'] += damage_and_source[0]
            if damage_and_source[1] in sources.keys():
                sources[damage_and_source[1]] += damage_and_source[0]
            else:
                sources[damage_and_source[1]] = damage_and_source[0]
        elif MELEE_DEFENSE_OPPONENT_CRIT_MESSAGE in line:
            result['Crits'] += 1
            damage_and_source = parse_damage_and_source(line)
            result['CritDamage'] += damage_and_source[0]
            if damage_and_source[1] in sources.keys():
                sources[damage_and_source[1]] += damage_and_source[0]
            else:
                sources[damage_and_source[1]] = damage_and_source[0]
        elif MELEE_DEFENSE_SPELL_PROC_MESSAGE in line:
            result['SpellsLanded'] += 1
            damage_and_source = parse_damage_and_source(line)
            result['SpellDamage'] += damage_and_source[0]
            if damage_and_source[1] in sources.keys():
                sources[damage_and_source[1]] += damage_and_source[0]
            else:
                sources[damage_and_source[1]] = damage_and_source[0]
        elif MELEE_BUFFER_ABSORB_MESSAGE in line:
            result['Absorbed'] += parse_healing_and_source(line)[0]

    result['Sources'] = sorted(sources.items(), key=operator.itemgetter(1), reverse=True)

    result['TotalMeleeAttacks'] = result['Blocks'] + result['Parries'] + result['Evades'] + \
        result['Hits'] + result['Misses']

    result['TotalSpellAttacks'] = result['Resists'] + result['SpellsLanded']

    result['TotalAttacks'] = result['TotalMeleeAttacks'] + result['TotalSpellAttacks']
    
    result['TotalDamage'] = result['MeleeDamage'] + result['CritDamage'] + result['SpellDamage']

    return result


def parse_damage_and_source(line):
    """Helper method that finds the amount of damage and who it was dealt by"""
    split_line = line.split()
    source = ''

    is_name_part = True
    for word in split_line[1:]:
        if word == 'hits' or word == 'critical':
            is_name_part = False
        elif is_name_part:
            source += word + ' '
    source = source.replace('The ', '')

    for word in split_line:
        num = 0
        try:
            num = int(word)
        except ValueError:
            continue
        if num > 0:
            return [num, source]

    return [num, source]

def parse_damage_and_target(line):
    """Helper method that finds the amount of damage and who it was dealt to"""
    split_line = line.split()
    target = ''

    is_name_part = False
    for word in split_line:
        if word == 'for' or word == 'with':
            is_name_part = False
        elif is_name_part:
            target += word + ' '
        elif word == 'hit' or word == 'attack':
            is_name_part = True
    target = target.replace('the ', '')
    if target == '':
        target = '<Unassigned crits>'

    for word in split_line:
        num = 0
        try:
            num = int(word)
        except ValueError:
            continue
        if num > 0:
            return [num, target]

    return [num, target]


def parse_healing(readf):
    """Parses healing Received and Delivered. Includes LifeTap"""
    readf.seek(0)
    healing = {}
    sources = {}
    targets = {}
    healing['Sources'] = []
    healing['Targets'] = []
    healing['Received'] = 0
    healing['Lifetapped'] = 0
    healing['Delivered'] = 0
    for line in readf:
        if HEALING_RECEIVED_MESSAGE in line:
            healing_and_source = parse_healing_and_source(line)
            healing['Received'] += healing_and_source[0]
            if healing_and_source[1] in sources.keys():
                sources[healing_and_source[1]] += healing_and_source[0]
            else:
                sources[healing_and_source[1]] = healing_and_source[0]
        if LIFETAP_HEALTH_STOLEN_MESSAGE in line:
            healing['Lifetapped'] += parse_healing_and_source(line)[0]
        if HEALING_DELIVERED_MESSAGE in line:
            healing_and_target = parse_healing_and_target(line)
            healing['Delivered'] += healing_and_target[0]
            if healing_and_target[1] in targets.keys():
                targets[healing_and_target[1]] += healing_and_target[0]
            else:
                targets[healing_and_target[1]] = healing_and_target[0]

    healing['Sources'] = sorted(sources.items(), key=operator.itemgetter(1), reverse=True)
    healing['Targets'] = sorted(targets.items(), key=operator.itemgetter(1), reverse=True)
    
    return healing

def parse_healing_and_source(line):
    """Helper method that finds amount of healing and character providing it"""
    split_line = line.split()
    source = ''

    is_name_part = False
    for word in split_line:
        if word == 'for':
            is_name_part = False
        elif is_name_part:
            source += word + ' '
        elif word == 'by':
            is_name_part = True
    source = source.replace('the ', '')

    for word in split_line:
        num = 0
        try:
            num = int(word)
        except ValueError:
            continue
        if num > 0:
            return [num, source]

    return [num, source]

def parse_healing_and_target(line):
    """Helper method that finds the amount of healing and who it was provided to"""
    split_line = line.split()
    target = ''

    is_name_part = False
    for word in split_line:
        if word == 'for':
            is_name_part = False
        elif is_name_part:
            target += word + ' '
        elif word == 'heal':
            is_name_part = True
    target = target.replace('the ', '')

    for word in split_line:
        num = 0
        try:
            num = int(word)
        except ValueError:
            continue
        if num > 0:
            return [num, target]

    return [num, target]



def print_healing(healing):
    """Prints out the values from the <healing> dictionary"""
    print('%&%&%&%&%&%& Healing stats %&%&%&%&%&%&')
    for key, value in healing.items():
        if key != 'Sources' and key != 'Targets':
            print(key + ': ' + '{:,}'.format(value))
    print('++++Healed By++++')
    for key, value in healing['Sources'].items():
        print('\t' + key + ': ' + '{:,}'.format(value))
    print('++++Healing Given++++')
    for key, value in healing['Targets'].items():
        print('\t' + key + ': ' + '{:,}'.format(value))

def print_combat(combat):
    """Prints out the values from the <combat> dictionary"""
    print('=|====> COMBAT DATA <====|=')
    print('----> Offensive stats: <----')
    print('===[] Melee []===')
    for key, value in combat['Melee_attack'].items():
        if key != 'Targets':
            print(key + ': ' + '{:,}'.format(value))
    print('----Individual targets----')
    for key, value in combat['Melee_attack']['Targets'].items():
        print('\t' + key + ': ' + '{:,}'.format(value))
    print('\n')


    print('**** Casting/proc stats ****')
    for key, value in combat['Caster_attack'].items():
        if key != 'Targets':
            print(key + ': ' + '{:,}'.format(value))
    print('----Individual Targets----')
    for key, value in combat['Caster_attack']['Targets'].items():
        print('\t' + key + ': ' + '{:,}'.format(value))
    print('\n')

    print('||||| Defensive stats |||||')
    for key, value in combat['Defense'].items():
        if key != 'Sources':
            print(key + ': ' + '{:,}'.format(value))
    print('++++Individual attackers++++')
    for key, value in combat['Defense']['Sources'].items():
        print('\t' + key + ': ' + '{:,}'.format(value))
    print('\n')

def print_money(cash_flow):
    """Prints out the values from the <cash_flow> dictionary"""
    print('\n\n$$$$ CASH FLOW $$$$')
    print('Money looted: ' + currency_print_helper(cash_flow['Loot']))
    print('Money spent: ' + currency_print_helper(cash_flow['Expense']))
    print('Money received: ' + currency_print_helper(cash_flow['Income']))
    print('\n\n')


def parse_test_file():
    """Main function"""
    result = {}
    try:
        with open('./Log Files/miri_0108.log', 'r') as readf:
            cash_flow = parse_cash_flow(readf)
            combat = parse_combat(readf)
            healing = parse_healing(readf)

            # print_money(cash_flow)
            # print_combat(combat)
            # print_healing(healing)
            # print('\n\n')

        result['Cash'] = cash_flow
        result['Combat'] = combat
        result['Healing'] = healing

        j_result = json.dumps(result)
        print(j_result)
        
        # return j_result

    except IOError:
        print("Failed to open file")
        exit(0)

def parse_uploaded_file(readf):
    result = {}
    try:
        # with open(file, 'r') as readf:
        cash_flow = parse_cash_flow(readf)
        combat = parse_combat(readf)
        healing = parse_healing(readf)

            # print_money(cash_flow)
            # print_combat(combat)
            # print_healing(healing)
            # print('\n\n')

        result['Cash'] = cash_flow
        result['Combat'] = combat
        result['Healing'] = healing
        j_result = json.dumps(result)
        # print(j_result)
        
        return j_result

    except IOError:
        print("Failed to open file")
        exit(0)

def currency_print_helper(currency_dict):
    """Helper method for printing currency prettily"""
    result_text = ''
    if currency_dict[0] > 0:
        result_text += str(currency_dict[0]) + 'p '
    if currency_dict[1] > 0:
        result_text += str(currency_dict[1]) + 'g '
    if currency_dict[2] > 0:
        result_text += str(currency_dict[2]) + 's '
    if currency_dict[3] > 0:
        result_text += str(currency_dict[3]) + 'c'

    return result_text


# parse_test_file()