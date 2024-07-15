#Hoi4 construction simulator
import math


#TODO
"""
Change order to dict not list
GUI?
Show stats
Times events
Calculate Bonus
"""



class state():
    def __init__(self, civs, mills, infra, name, slots):
        self.name = name
        self.civs = civs
        self.mills = mills
        self.infra = infra
        self.slots = slots

def calculate_bonus():
    pass

def calculate_progress(state, construction_progress, available_civs, bonus):
    #print(available_civs)
    construction_progress += 8 * available_civs * (1 + (state.infra/ 5)) * (1 + bonus/100) #NB!!! the base is normaly 5 not 8 

    #print(f"This is the base contruction:{8 * available_civs * (1 + (state.infra / 5)) * (1 + bonus/100)}, that is 8 * {available_civs} = {8 * available_civs} \n * {(1+ (state.infra / 5))} * {1 + bonus/100}")

    return construction_progress

def get_civ_amount(states):
    civs = 0

    for state in states:
        civs += state.civs
    
    return civs

def track_stats(states, stats):
    #STATES AND STATS MUST NOT BE CONFUSED
    stats = stats
    #civ amount
    civs = get_civ_amount(states)
    stats.append(civs)

    return stats


def make_task(state, construction_type, amount, construction_progress):
    """
    Makes the dictionary type required in the construction list

    """

    task = {
            "state" : state,
            "construction_type" : construction_type,
            "amount" : amount,
            "construction_progress" : construction_progress
        }

    return task

def display_stats():
    pass

def innit():
    
    states = []
    moscow = state(5, 2, 3, "Moscow", 15)
    leningrad = state(20, 0, 4, "Leningrad", 25)

    states.append(moscow)
    states.append(leningrad) 



    queue = [make_task(moscow, "civs", 10,0),
             make_task(moscow, "infra", 2,100),
             make_task(leningrad, "civs", 10,0),
             make_task(leningrad, "infra", 1,50)
             ]
    
    bonus = -20

    CONSUMER_GOODS = 35/100
    CIV_COST = 10800
    MILL_COST = 7200
    INFRA_COST = 6000

    construction_types = {
                        "civs" : CIV_COST,
                        "mills" : MILL_COST,
                        "infra" : INFRA_COST
                }


    time = 0
    stats = []

    return states, queue, bonus, CONSUMER_GOODS, CIV_COST, MILL_COST, INFRA_COST, construction_types, stats, time

def main(states, queue, bonus, CONSUMER_GOODS, CIV_COST, MILL_COST, INFRA_COST, construction_types, stats, time):

    """
    run = True
    while run:
    """
    #TODO: calculate available civs 
    total_civs = get_civ_amount(states)
    #print(total_civs)
    available_civs = math.floor(total_civs * (1-CONSUMER_GOODS))

    if queue != []:

        for task in queue[:]: # [:] <- this is to stop potential buggs when popping elements while looping
            #print(order, queue)
            #getting variables 
            state = task["state"]
            construction_type = task["construction_type"]
            amount = task["amount"]
            construction_progress = task["construction_progress"]

            if available_civs > 15:
                civs = 15
                available_civs -= 15
            else:
                civs = available_civs
                available_civs = 0


            construction_progress = calculate_progress(state, construction_progress, civs, bonus)

            

            

            print(f"The contruction progress is at  {construction_progress} out of {CIV_COST}")

            

            if construction_progress >= construction_types[construction_type]:
                #testing if we have enough to build

                setattr(state, construction_type, getattr(state, construction_type)+ 1)

                if amount == 1:
                    queue.pop(queue.index(task))
                else:
                    construction_progress -= construction_types[construction_type]
                    amount -= 1


        



            # --- Updating the variabels ---
            task["construction_progress"] = construction_progress
            task["amount"] = amount
    
    else:
        #print(f"Done in {time} days, which is {(time / 30)} months, which is {(time) / 365.24} years")
        i = input()


    
    time += 1
    stats = track_stats(states, stats)

    return time, stats, states, queue



                    
            


if __name__ == "__main__":

    states = []
    moscow = state(5, 2, 3, "Moscow", 15)
    leningrad = state(20, 0, 4, "Leningrad", 25)

    states.append(moscow)
    states.append(leningrad) 



    queue = [make_task(moscow, "civs", 10,0),
             make_task(moscow, "infra", 2,0),
             make_task(leningrad, "civs", 10,0)
             ]
    
    main(states, queue, -20)