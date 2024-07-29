import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import Hoi4_construction_simulator as sim

def create_plot(X, Y):
    fig, ax = plt.subplots()
    plot_line, = ax.plot(X, Y, color="blue")
    ax.set_title("Civvis", fontsize=15)
    ax.set_xlabel("Tid")
    ax.set_ylabel("CIVVIS")
    ax.grid(True)
    return fig, plot_line

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

def update_plot(plot_line, X, Y):
    plot_line.set_xdata(X)
    plot_line.set_ydata(Y)
    plt.gca().relim()
    plt.gca().autoscale_view()
    plt.draw()

def make_column_layout(queue, construction_types):
    column_layout_queue = []
    for task in queue:
        construction_type = task["construction_type"]
        column_layout_queue.append([sg.Text(construction_type), sg.ProgressBar(max_value=construction_types[construction_type], orientation="h", size=(30, 15), key="-" + task["state"].name + construction_type + "-")])
    return column_layout_queue

def update_column(window, queue):
    for task in queue:
        construction_type = task["construction_type"]
        construction_progress = task["construction_progress"]
        window["-" + task["state"].name + construction_type + "-"].update(construction_progress)

def main():
    states, queue, consumer_goods, CIV_COST, MILL_COST, INFRA_COST, national_spirits, advisors, trade_law, eco_law, construction_types, stats, time, time_data = sim.init()

    sg.theme('Dark Blue 8')
    column_layout_queue = make_column_layout(queue, construction_types)
    layout = [
        [sg.Canvas(size=(640, 480), key="-CANVAS-"), sg.Column(column_layout_queue, vertical_alignment='top')],
    ]

    window = sg.Window('Hoi4 Simulator', layout, finalize=True)
    canvas_elem = window["-CANVAS-"]
    canvas = canvas_elem.TKCanvas

    # Create initial plot
    figure, plot_line = create_plot(time_data, stats)
    figure_canvas_agg = draw_figure(canvas, figure)

    c = 0

    run = True
    while run:
        event, values = window.read(timeout=10)

        if event in (sg.WINDOW_CLOSED, "Exit"):
            run = False
        
        # Update simulation state
        time_data, time, stats, states, queue = sim.main(states, queue, consumer_goods, CIV_COST, MILL_COST, INFRA_COST, national_spirits, advisors, trade_law, eco_law, construction_types, stats, time, time_data)

        if c % 168 == 0:
            # Update the plot with new data
            update_plot(plot_line, time_data, stats)

        # Update the progress bars
        update_column(window, queue)

        c += 1

        if queue == []:
            run = False

    sim.save_stats(time_data, stats)
    window.close()

if __name__ == "__main__":
    main()
