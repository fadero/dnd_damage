import numpy as np  #so we can simulate many things in parallel
import matplotlib.pyplot as plt    #so we can save simulations as figures
import time     #so we can report the time it takes to run the code

start = time.time()

def damage(adv='0', atk_bonus=0, crit=20, lucky=0, atk_die='0d0', arm_class=10,
    dmg_die0='1d8', dmg_bonus=0,  GWM=0, GWF=0, brutal=0, vicious=0, dmg_die1=0,
    dmg_die2=0, n_atks=1e5, progress=0):
    """'Damage output' a floating point number.

    INPUTS
    'adv'       string for advantage ('0', 'adv', 'disadv', 'adv+', 'adv++')
    'atk_bonus' integer modifier to apply to d20 attack roll
    'crit'      integer value [1,20] on the d20 at or above which is a crit hit
    'lucky'     logical value for if natural 1s on the d20 are re-rolled
    'atk_die'   string die to be added as integer bonus to d20 attack roll
    'arm_class' integer armor class of the attack's target creature
    'dmg_die0'  string of di(c)e to be rolled on a hit for damage
    'dmg_bonus' integer bonus to be added to dmg_die roll
    'GWM'       logical value for if great weapon master was declared
    'GWF'       logical value for if great weapon fighting style is applicable
    'brutal'    whole number value for extra damage dice to be rolled on crit
    'vicious'   integer value for bonus damage to be added on natural 20
    'dmg_die1'  string of second damage di(c)e to be rolled on hit
    'dmg_die2'  string of third damage di(c)e to be rolled on a hit
    'n_atks'    whole number of attacks to be simulated
    'progress'  logical value for whether to print progress bar to command line

    OUTPUTS
    'damage'    float number representing average expected damage per attack"""

    if atk_die==0 or atk_die=='0': #parse user inputs
        atk_die = '0d0'
    if dmg_die1==0 or dmg_die1=='0':
        dmg_die1 = '0d0'
    if dmg_die2==0 or dmg_die2=='0':
        dmg_die2 = '0d0'
    n_atks = int(n_atks)

    n_atk_dice =    int(atk_die[0:atk_die.find('d')])   #how many bonus atk dice
    atk_dice =      int(atk_die[1+atk_die.find('d'):])  #what bonus atk di(c)e

    n_dmg_dice0 =   int(dmg_die0[0:dmg_die0.find('d')]) #how many dmg0 dice
    dmg_dice0 =     int(dmg_die0[1+dmg_die0.find('d'):])#what bonus dmg0 di(c)e

    n_dmg_dice1 =   int(dmg_die1[0:dmg_die1.find('d')]) #how many dmg1 dice
    dmg_dice1 =     int(dmg_die1[1+dmg_die1.find('d'):])#what bonus dmg1 di(c)e

    n_dmg_dice2 =   int(dmg_die2[0:dmg_die2.find('d')]) #how many dmg2 dice
    dmg_dice2 =     int(dmg_die2[1+dmg_die2.find('d'):])#what bonus dmg2 di(c)e
    
    if adv == 0:    #if user doesn't use a string
        adv == '0'  #make it a string

    if GWM == 1:    #if using great weapon master
        dmg_bonus = dmg_bonus+10    #increase the damage of any hit by 10
        atk_bonus = atk_bonus-5     #decrease the attack bonus by 5

    results = np.zeros((n_atks, 1), dtype='float16') #empty list to put dmg in
    
    if adv == '0':  #make some text to report back to the user while code runs
        adv_str = 'no advantage'
    elif adv == 'disadv':
        adv_str = 'disadvantage'
    elif adv == 'adv':
        adv_str = 'advantage'
    elif adv == 'adv+':
        adv_str = 'superior advantage'

    if progress == 1:    
        print("Simulating %i attack rolls at %s against AC %i..."
              %(n_atks, adv_str, arm_class), end='')
    
    for atk in range(n_atks):   #simulate many attacks
        rolls = np.zeros((n_dmg_dice0+brutal+n_dmg_dice1+n_dmg_dice2, 1))
        if adv == '0':
            atk_roll = np.random.randint(low=1, high=21, size=1)
            if 1 in atk_roll and lucky == 1: #if lucky and 1 rolled...
                atk_roll = np.random.randint(low=1, high=21) #reroll the 1
        elif    adv == 'adv':
            atk_roll = atk_roll = np.random.randint(low=1, high=21,
                                                    size=(1, 2))
            if 1 in atk_roll and lucky == 1: #if lucky and 1 rolled...
                row, column = np.where(atk_roll==1) #find first 1 and reroll it
                atk_roll[row[0], column[0]] = np.random.randint(low=1, high=21)
            atk_roll = np.amax(atk_roll)
        elif adv == 'adv+':
            atk_roll = atk_roll = np.random.randint(low=1, high=21,
                                                    size=(1, 3))
            if 1 in atk_roll and lucky == 1: #if lucky and 1 rolled...
                row, column = np.where(atk_roll==1) #find first 1 and reroll it
                atk_roll[row[0], column[0]] = np.random.randint(low=1, high=21)
            atk_roll= np.amax(atk_roll)
        elif adv == 'adv++':
            atk_roll = atk_roll = np.random.randint(low=1, high=21,
                                                    size=(1, 4))
            if 1 in atk_roll and lucky == 1: #if lucky and 1 rolled...
                row, column = np.where(atk_roll==1) #find first 1 and reroll it
                atk_roll[row[0], column[0]] = np.random.randint(low=1, high=21)
            atk_roll= np.amax(atk_roll)
        elif adv == 'disadv':
            atk_roll = atk_roll = np.random.randint(low=1, high=21,
                                                    size=(1, 2))
            if 1 in atk_roll and lucky == 1: #if lucky and 1 rolled...
                row, column = np.where(atk_roll==1) #find first 1 and reroll it
                atk_roll[row[0], column[0]] = np.random.randint(low=1, high=21)
            atk_roll= np.amin(atk_roll)
        else:
            print('ERROR: incorrect advantage string entered')
            break   #something's wrong

        if atk_roll >= crit:    #if it's a critical hit
            for roll in range(n_dmg_dice0+brutal+n_dmg_dice1+n_dmg_dice2):
                if roll <= n_dmg_dice0+brutal: #keep rolling dmg
                    roll_temp = np.random.randint(low=1, high=dmg_dice0+1)
                    if GWF == 1 and roll_temp < 3: #reroll dmg if rolled low
                        roll_temp = np.random.randint(low=1,
                                                      high=dmg_dice0+1)
                    rolls[roll, 0] = roll_temp+(1+brutal)*dmg_dice0 #crit dmg
                else:
                    if dmg_dice1 > 0 and roll <= n_dmg_dice0+brutal+n_dmg_dice1:
                        roll_temp = np.random.randint(low=1, high=dmg_dice1+1)
                        if GWF == 1 and roll_temp < 3: #reroll dmg if rolled low
                            roll_temp = np.random.randint(low=1,
                                                          high=dmg_dice1+1)
                        rolls[roll, 0] = roll_temp+dmg_dice1 #crit dmg
                    if dmg_dice2 > 0 and roll > n_dmg_dice0+brutal+n_dmg_dice1:
                        roll_temp = np.random.randint(low=1,
                                                      high=dmg_dice2+1)
                        if GWF == 1 and roll_temp < 3: #reroll dmg if rolled low
                            roll_temp = np.random.randint(low=1,
                                                          high=dmg_dice2+1)
                        rolls[roll, 0] = roll_temp+dmg_dice2 #crit dmg

            if atk_roll == 20:  #only add vicious bonus on nat 20
                vicious_temp = vicious
            else:
                vicious_temp = 0
            dmg = np.sum(rolls)+dmg_bonus+vicious_temp

        elif atk_roll == 1: #critical miss
            dmg = 0
            
        else: #neither crit hit or crit fail
            atk_roll = atk_roll+atk_bonus

            if n_atk_dice > 0:  #roll and add any attack bonus dice to atk roll
                for roll in range(n_atk_dice):
                    roll_temp = np.random.randint(low=1, high=atk_dice+1)
                    atk_roll = atk_roll+roll_temp

            if atk_roll >= arm_class:   #normal hit
                for roll in range(n_dmg_dice0+n_dmg_dice1+n_dmg_dice2):
                    if roll <= n_dmg_dice0+brutal: #keep rolling dmg
                        roll_temp = np.random.randint(low=1, high=dmg_dice0+1)
                        if GWF == 1 and roll_temp < 3: #reroll dmg if rolled low
                            roll_temp = np.random.randint(low=1,
                                                          high=dmg_dice0+1)
                        rolls[roll, 0] = roll_temp
                    else:
                        if dmg_dice1>0 and roll<=n_dmg_dice0+brutal+n_dmg_dice1:
                            roll_temp = np.random.randint(low=1,
                                                          high=dmg_dice1+1)
                            if GWF == 1 and roll_temp < 3:
                                roll_temp=np.random.randint(low=1,
                                                            high=dmg_dice1+1)
                            rolls[roll, 0] = roll_temp
                        if dmg_dice2>0 and roll>n_dmg_dice0+brutal+n_dmg_dice1:
                            roll_temp = np.random.randint(low=1,
                                                          high=dmg_dice2+1)
                            if GWF == 1 and roll_temp < 3:
                                roll_temp=np.random.randint(low=1,
                                                            high=dmg_dice2+1)
                            rolls[roll, 0] = roll_temp
                dmg = np.sum(rolls)+dmg_bonus
                
            else:   #normal miss
                dmg = 0
        
        results[atk, 0] = dmg   #record damage
        
        if (atk/(n_atks/10)).is_integer() and progress == 1:
            print('.', end='', sep='') #print a period for every 1/10 of n_atks
        
    avg_dmg = np.mean(results[:,0]) #take the arithmetic mean over all attacks

    if progress == 1:
        print(' Done.')
    return avg_dmg  #pass the average damage back to the user

##Below is an example of multiple calls of the damage function for the purpose
##of plotting damage as a function of armor class

arm_class_min = 10
arm_class_max = 25

arm_class = list(range(arm_class_min, arm_class_max+1))  #range of ACs to test

avg_dmg_plt = np.zeros((arm_class_max-arm_class_min+1, 3, 2)) #AC, adv, atk type

def make_a_figure(avg_dmg_plt, num=0, arm_class_min=10, arm_class_max=25,
                  title='', adv_idx=0,  #define inputs for making figs
                  legend=['attack0', 'attack1', 'attack2', 'attack3']):
    fig = plt.figure(num=num)   #change the figure number to match the adv
    for atk_idx in range(len(avg_dmg_plt[0, 0, :])):    #plot for all atk types
        plt.plot(arm_class, avg_dmg_plt[:, adv_idx, atk_idx],
                 label=legend[atk_idx])
    plt.legend()    #include a legend, defined by the label arg in plt.plot
    plt.grid('on')  #turn the grid on
    plt.xlim(arm_class_min, arm_class_max)  #set x limits to match ACs tested
    plt.ylim(avg_dmg_plt[:, adv_idx, :].min(), avg_dmg_plt[:, adv_idx, :].max())
    plt.xlabel("target armor class")    #^set y limits to match damage output
    plt.ylabel("average damage per attack")
    plt.title(title)

print("Simulating %i sets of attack rolls..."%(avg_dmg_plt.size), end='')

for adv_idx in range(len(avg_dmg_plt[0, :, 0])):    #for all advantages
    for arm_class_idx in range(arm_class_min, arm_class_max+1): #for all ACs
        for atk_idx in range(len(avg_dmg_plt[0, 0, :])):    #for all atk types

            #define title strings and advantage strings
            if adv_idx == 0:
                adv = '0'
                title = 'no advantage'
            elif adv_idx == 1:
                adv = 'adv'
                title = 'advantage'
            elif adv_idx == 2:
                adv = 'disadv'
                title = 'disadvantage'

            #run the damage calculation
            avg_dmg_plt[arm_class_idx-arm_class_min, adv_idx, atk_idx] = damage(
                adv=adv, atk_bonus=14, crit=18, arm_class=arm_class_idx,
                dmg_die0='2d6', dmg_bonus=6, GWM=atk_idx, GWF=1, brutal=1,
                n_atks=1e5, progress=0)
        print('.', end='', sep='') #print a period for every AC finished

    #make a figure for each advantage type, plot all attack types on each figure
    make_a_figure(avg_dmg_plt, num=adv_idx, arm_class_min=10, arm_class_max=25,
        title=title, adv_idx=adv_idx,legend=['greatsword', 'greatsword+GWM'])

end = time.time()
print(' Done.\n')
print("Elapsed time is %i seconds."%(end-start), end='')
plt.show()  #show all the figures once the calculations are done
