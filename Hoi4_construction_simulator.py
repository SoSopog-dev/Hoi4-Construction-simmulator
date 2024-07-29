#Hoi4 construction simulator
import math
import csv

#TODO
"""



Times events
Calculate Bonus
make Consumer goods affected by stability
"""




class state():
    def __init__(self, civs, mills, infra, name, slots):
        self.name = name
        self.civs = civs
        self.mills = mills
        self.infra = infra
        self.slots = slots

def eco_laws(law_name):
    #TODO make other laws and return based on law_name
    civilian_eco = {
        "name" : "civilian_eco",
        "consumer_goods" : 35/100,
        "mills" : -30,
        "civs" : -30,
    }

    return civilian_eco


def calculate_bonus(natinal_spirits, advisors, construction_techs, trade_law, eco_law, building):
    bonus = 0

    #National Spirits
    for spirit in natinal_spirits:
        if building in spirit:
            bonus += spirit[building]

        if "construction" in spirit:
            bonus += spirit["construction"]

    #Advisors
    for advisor in advisors:
        if building in advisor:
            bonus += advisor[building]

        if "construction" in advisor:
            bonus += advisor["construction"]

    #Construction techs

    for tech in  construction_techs:
        bonus += tech
    #Trade Law

    bonus += trade_law["construction"]
    #Eco Law

    if building in eco_law:
        bonus += eco_law[building]

    return bonus

def calculate_progress(state, construction_progress, available_civs, bonus):
    #print(available_civs)
    construction_progress += 5 * available_civs * (1 + (state.infra/ 5)) * (1 + bonus/100) #NB!!! the base is normaly 5 not 8 

    #print(f"This is the base contruction:{8 * available_civs * (1 + (state.infra / 5)) * (1 + bonus/100)}, that is 8 * {available_civs} = {8 * available_civs} \n * {(1+ (state.infra / 5))} * {1 + bonus/100}")

    return construction_progress

def get_civ_amount(states):
    civs = 0

    for state in states:
        civs += state.civs
    
    return civs

def get_factory_amount(states):
    factories = 0

    for state in states:
        factories += state.civs
        factories += state.mills
    
    return factories

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

def save_stats(times, stats):
    filename = 'data.csv'

    # Open the file in write mode
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(['Column1', 'Column2'])
        
        # Write the data from the arrays
        for item1, item2 in zip(times, stats):
            writer.writerow([item1, item2])


def init():

    # --- States ---
    
    states = []
    york = state(0, 0, 3, "York", 15)
    dover = state(0, 0, 3, "Dover", 25)
    rio = state(0, 0, 3, "Rio", 25)
    london = state(33, 8, 5, "London", 30)

    states.append(york)
    states.append(dover) 
    states.append(rio)
    states.append(london)



    queue = [   make_task(york, "infra", 1,0),
                make_task(york, "civs", 3,0),
                make_task(dover, "infra", 1,0),
                make_task(dover, "civs", 3,0),
                make_task(rio, "infra", 1,0),
                make_task(rio, "civs", 3,0)
             ]
    
    #national spirits

    national_spirits = []
    advisors = []

    trade_law = {
        "research" : 5,
        "construction" : 10
    }

    eco_law = eco_laws("civilian_eco")

    consumer_goods = eco_law["consumer_goods"] #TODO make stability affect consumergoods


    #Constants


    CIV_COST = 10800
    MILL_COST = 7200
    INFRA_COST = 6000

    construction_types = {
                        "civs" : CIV_COST,
                        "mills" : MILL_COST,
                        "infra" : INFRA_COST
                }


    time = 0
    times = []
    stats = []

    return states, queue, consumer_goods, CIV_COST, MILL_COST, INFRA_COST, national_spirits, advisors, trade_law, eco_law, construction_types, stats, time, times

def main(states, queue, consumer_goods, CIV_COST, MILL_COST, INFRA_COST, national_spirits, advisors, trade_law, eco_law, construction_types, stats, time, times):

    """
    run = True
    while run:
    """
    #TODO: calculate available civs 
    total_civs = get_civ_amount(states)
    total_factories = get_factory_amount(states)
    #print(total_civs)
    available_civs =  total_civs - math.floor(total_factories * consumer_goods)

    construction_techs = []

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

            bonus = calculate_bonus(national_spirits, advisors, construction_techs, trade_law, eco_law, construction_type)


            construction_progress = calculate_progress(state, construction_progress, civs, bonus)

            
            

            #print(f"The contruction progress is at  {construction_progress} out of {CIV_COST}")

            

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
    
    #else:
        #print(f"Done in {time} days, which is {(time / 30)} months, which is {(time) / 365.24} years")
        #i = input()


    times.append(time)
    time += 1
    
    stats = track_stats(states, stats)

    return times, time, stats, states, queue



                    
            


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
