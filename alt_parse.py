
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

CASTER_OFFENSE_ATTACK_MESSAGE = 'You hit'
# [21:57:40] You hit Aser for 269 (-14) damage! //Casted damage
# [19:40:26] You hit the cave trow for 75 damage! //Proc damage
CASTER_OFFENSE_SPELL_RESIST_MESSAGE = 'resists the effect'
# [21:57:59] Krok resists the effect!

CRITICAL_HIT_OFFENSE_MESSAGE = 'You critical hit'
# [19:05:13] You critical hit the cave trow for an additional 41 damage!

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

CASTER_DEFENSE_SPELL_RESISTED_MESSAGE = 'You resist the effect'
# [21:45:12] You resist the effect!

HEALING_RECEIVED_MESSAGE = 'You are healed by'
# [21:57:56] You are healed by Norseiaw for 85 hit points.


##region Money Matters
def parse_money(line):
    """Counts the money paid/received."""
    money_spent = 0
    money_gained = 0
    if line.find('gives you') != -1:
        if line.find('plat') != -1:
            plat_text = line[line.find('plat')-4:line.find('plat')]
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

def parse_gold_loot(line):
    """Prints out lines for gold loot picked up from mobs."""
    money_looted = 0
    if line.find('You pick up') != -1 or line.find('for this kill') != -1:
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

def currency_breakdown(total):
    """Helper method to parse_money. Seperates 'total' into largest denominations and returns them in a list."""
    plat = total/10000000
    gold = (total%10000000)/10000
    silver = (total%10000)/100
    copper = (total%100)
    return [plat, gold, silver, copper]
##endregion


##region All Things Melee
def parse_melee_combat(line):
    """Counts and returns the # of successful attacks with both hands"""
    try:
        hit_count = 0
        total_damage = 0
        if line.find('You attack') != -1 and line.find('with your') != -1:
            hit_count += 1
            damage_text = line[line.find('damage')-16:line.find('damage')]

            if line.find('-') != -1 or line.find('+') != -1:
                total_damage += int(damage_text.split()[len(damage_text.split())-2])
            else:
                total_damage += int(damage_text.split()[len(damage_text.split())-1])
        return hit_count
    except IndexError:
        print(str(line))
        exit(0)

def parse_caster_combat(line):
    try:
        hit_count = 0
        resist_count = 0
        total_damage = 0
        if line.find('You hit') != -1 and line.find('you attack') == -1:
            hit_count += 1
            damage_text = line[line.find('damage')-16:line.find('damage')]

            if line.find('-') != -1 or line.find('+') != -1:
                total_damage += int(damage_text.split()[len(damage_text.split())-2])
            else:
                total_damage += int(damage_text.split()[len(damage_text.split())-1])
        if line.find('resists the effect') != -1:
            resist_count += 1
        return hit_count
    except IndexError:
        print(str(line))
        exit(0)

def parse_defense(line):
    """Counts # blocks, # misses, # parries, # evades, # hits taken. Prints results, along with %'s."""
    block_count = 0
    parry_count = 0
    evade_count = 0
    hits_taken = 0
    total_damage = 0
    misses = 0
    try:
        if line.find('you block the blow') != -1:
            block_count +=1
        elif line.find('you parry the blow') != -1:
            parry_count +=1
        elif line.find('you evade the blow') != -1:
            evade_count +=1
        elif line.find('hits your') != -1:
            hits_taken +=1
            damage_text = line[line.find('damage')-9:line.find('damage')]
            if line.find('-') != -1 or line.find('+') != -1:
                total_damage += int(damage_text.split()[len(damage_text.split())-2])
            else:
                total_damage += int(damage_text.split()[len(damage_text.split())-1])
        elif line.find('attacks you and misses') != -1:
            misses += 1
        total_attacks = block_count + parry_count + evade_count + hits_taken + misses
        print("Defensive statistics:\n")
        print("Total attacks received: " + str(total_attacks))
        if total_attacks != 0:
            print(("Block count: " + str(block_count) + "\n\tBlock %: " + str((float(block_count))/(float(total_attacks))) +
                    "\nParry count: " + str(parry_count) + "\n\tParry %: " + str((float(parry_count))/(float(total_attacks)))+
                    "\nEvade Count " + str(evade_count) + "\n\tEvade %: " + str((float(evade_count))/(float(total_attacks)))+
                    "\nMiss count: " + str(misses) + "\n\tMiss %: " + str((float(misses))/(float(total_attacks))) +
                    "\nHits taken: " + str(hits_taken)) + "\n\tHit %: " + str((float(hits_taken))/(float(total_attacks))) + "\nTotal damage taken: " + str(total_damage) + "\n")
    except ValueError or IndexError:
        print(line)
        exit(0)

def parse_mainhand(line, weaponName):
    """Counts # of attacks made with user-input 'weaponName'."""
    mainhand_count = 0
    print(weaponName)
    if line.find('with your ' + weaponName) != -1:
        mainhand_count += 1
    print("# of mainhand hits: " + str(mainhand_count))
##endregion

##region Combat helpers
def parse_crit(openFile):
    """Counts and returns the # of critical hits inflicted with either hand."""
    crit_count = 0
    for line in openFile:
        if line.find('You critical hit') != -1:
            crit_count += 1
    print("# of crits: " + str(crit_count))
    return crit_count

##endregion