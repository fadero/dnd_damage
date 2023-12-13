# dnd_damage
Python3 code to simulate average expected damage output per attack in D&amp;D 5e.

DESCRIPTION
This code takes various string and integer inputs from the user for simulating an arbitrary number of attacks in D&D 5e. This code is mainly useful for determining the average damage that an attack will deal to a creature with a user-defined armor class. 

DEPENDENCIES
numpy: https://numpy.org
matplotlib: https://matplotlib.org
multiprocessing: https://docs.python.org/3/library/multiprocessing.html
time: https://docs.python.org/3/library/time.html

ASSUMPTIONS
This code uses a home-brew rule for critical hits, which is as follows: 

The attack hits, regardless of any modifiers or the target’s AC.
Roll for damage normally. Then determine the maximum damage that you can possibly roll before applying any modifiers (basically, the maximum sum of all dice rolled). Then add your modifiers. This is your total critical hit damage.

Example: In a last-ditch attempt to save himself from death, Shin the Wizard (with a +0 STR modifier) picks up a greatsword (for which he has no proficiency) and lunges at a bloodied Ancient Red Dragon (AC 22) with it.

Shin rolls 1d20 for his attack roll. The roll is a 20; critical hit!
The greatsword slides cleanly in between the scales of the dragon, stabbing a vital organ.
Shin rolls 2d6 (it’s a 4 and a 3; not bad), adds 12 (the maximum roll of 2d6) , then adds his STR modifier (+0; he’s scrawny).

The dragon takes 19 points of slashing damage and collapses in anguish, dead.

INPUTS
'adv' - The string for the advantage on the d20 roll. '0' for no advantage, 'adv' for advantage, 'disadv' for disadvantage, 'adv+' for superior advantage (see: Elven Accuracy) (default '0')

'atk_bonus' - The integer modifier to apply to the d20 attack roll. This can, but shouldn't, include any Great Weapon Master modifiers (there is an input argument for GWM) (default 0)

'crit' - Value on the d20 at or above which a critial hit is scored. (default 20)

'lucky' - The logical value for the Halfing Lucky trait (not the Lucky feat) that rerolls ones. See this rules thread for clarification on using Lucky on rolls with advantage: https://rpg.stackexchange.com/questions/79657/when-rolling-with-advantage-do-halflings-get-to-apply-their-luck-trait-and-rerol (default: 0)

'atk_die' - A string for the di(c)e to be added as a bonus to the attack roll (e.g. '1d4' for the bless spell) (default: '0d0')

'arm_class' - The integer armor class of the attack's target. (default: 10)

'dmg_die0' - The string for the default damage di(c)e rolled on a hit (e.g., '1d4', '2d6') (default: '1d8')

'dmg_bonus' - The integer bonus to the damage done on a hit (default: 0)

'GWM' - The logical value for if the Great Weapon Master feat is used in the attack. (default: 0)

'GWF' - The logical value for if the Great Weapon Fighting fighting style is used. (default: 0)

'brutal' - The integer value for the extra number of damage dice rolled on a critical hit (e.g. Barbarian's Brutal Critical, the Piercer feat) (default: 0)

'vicious' - The integer value for the damage bonus added on a natural 20 attack roll (e.g. Vicious weapons) (default: 0)

'dmg_die1' - The string for an additional type of damage di(c)e rolled on a hit. (e.g. Paladin's Divine Smite '1d8'). Note: extra damage dice are not subject to the brutal input argument. (default: 0)

'dmg_die2' - The string for an additional type of damage di(c)e rolled on a hit. (e.g. the hex spell '1d6') Note: extra damage dice are not subject to the brutal input argument. (default: 0)

'n_atks' - Whole number of attacks to be simulated (default: 1e5)

'progress' – The logical value for if progress reports on the code are to be printed.

NOTES
- For damage subject to the Elemental Adept feat (i.e. all 1s on damage dice are considered 2s), I recommend adding the expected increase in damage to dmg_bonus. Example: 1d4 gives an average of 2.5 (1+2+3+4)/4. 1d4 (1s become 2s) gives an average of 2.75 (2+2+3+4)/4. The difference in average is 0.25 because rolling a 1 has a 1-in-4 chance of occuring, so the average roll experiences a bonus of 0.25. From a statistical average viewpoint, 1d4 (1s become 2s) is equivalent to 1d4+0.25. This is a bit more math on the user up-front, but the alternative is adding in input arguments for which of the damage dice are subject to Elemental Adept, which makes the code a lot messier. This edge-case is not frequent enough to justify additional input args. 
