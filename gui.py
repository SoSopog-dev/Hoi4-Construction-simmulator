import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import Hoi4_construction_simulator as sim 

def create_plot(X, Y):
    plt.plot(X, Y, color = "blue", marker = "o")
    plt.title("Civvis", fontsize = 15)
    plt.xlabel("Tid")
    plt.ylabel("CIVVIS")
    plt.grid(True)
    return plt.gcf()

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg






def make_column_layout(queue, construction_types):

    column_layout_queue = []

    

    for task in queue:
        construction_type = task["construction_type"] 
        column_layout_queue.append( [sg.Text(construction_type), sg.ProgressBar(max_value = construction_types[construction_type], orientation="h", size=(30, 15), key = "-" + task["state"].name + construction_type + "-")] )
    
    return column_layout_queue

def update_coloumn(window, queue):
    

    for task in queue:
        construction_type = task["construction_type"]
        construction_progress = task["construction_progress"]
        window["-" + task["state"].name + construction_type + "-"].update(construction_progress)


def main():

    
    states, queue, bonus, CONSUMER_GOODS, CIV_COST, MILL_COST, INFRA_COST, construction_types, stats, time = sim.innit()

    # ------ GUI Definition ------ #

    sg.theme('Dark Blue 8')

    column_layout_queue = make_column_layout(queue, construction_types)

    layout = [
        [ sg.Canvas(size = (1000, 1000), key="-CANVAS-") , sg.Column(column_layout_queue,  vertical_alignment='top')],

    ]

    """
    layout = [[sg.Text('Line Plot')],
            [sg.Canvas(size=(1000, 1000), key='-CANVAS-')],
            [sg.Exit()]]
    """
    window = sg.Window('Hoi4 simmulator', layout, finalize=True)
    

    

    run = True
    while run:
        event, values = window.read()
        #print(event, values)

        

        if event in (sg.WINDOW_CLOSED, "Exit"):
            run = False

        print("This is before calling sim.main")
        time, stats, states, queue = sim.main(states, queue, bonus, CONSUMER_GOODS, CIV_COST, MILL_COST, INFRA_COST, construction_types, stats, time)
        print("This is after calling sim.main")

        #draw_figure(window["-CANVAS-"].TKCanvas, create_plot(time, stats))
        
    

        update_coloumn(window, queue)
 
    window.close()

if __name__ == "__main__":
    main()