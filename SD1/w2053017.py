#Importing GraphWin, Rectangle, Text, Point graphics module
from graphics import GraphWin, Rectangle, Text, Point

# List to store user input data
input_data = []

# Valid credits range for each type of credit
VALID_CREDITS = list(range(0, 140, 20))
# Dictionary to record the progression outcomes
progression = {"progress": 0, "module_trailer": 0, "module_retriever": 0, "exclude": 0}

# Function to get valid credit input from the user
def get_credits(type: str):
    user_input = input(f"Enter the number of {type} credits: ")
    try:
        credit = int(user_input)
        if credit in VALID_CREDITS:
            return credit
        print("Out of range.")
    except ValueError:
        print("Integer required.")
    return get_credits(type)

# Function to determine the outcome based on pass, defer, and fail credits
def get_outcome(pass_credits: int, defer_credits: int, fail_credits: int):
    total = sum([pass_credits, defer_credits, fail_credits])
    if total != 120:
        return None
    if pass_credits == 120:
        return "progress"
    elif pass_credits == 100 and (defer_credits == 20 or fail_credits == 20):
        return "module_trailer"
    elif fail_credits >= 80:
        return "exclude"
    else:
        return "module_retriever"

# Function to format the outcome for display
def format_outcome(outcome: str):
    if outcome == "progress":
        return "Progress"
    elif outcome == "module_trailer":
        return "Progress (module trailer)"
    elif outcome == "module_retriever":
        return "Do not Progress – module retriever"
    else:
        return "Exclude"
# Function to ask the user if they want to continue entering data
def ask_continue():
    print("Would you like to enter another set of data.")
    answer = input("Enter 'y' for yes or 'q' to quit and view results: ").lower()
    if answer not in ["y", "q"]:
        return ask_continue()
    return answer == "y"
# Function to draw a histogram based on the progression data
def draw_histogram():
    win = GraphWin("Histogram", 500, 400)
    win.setBackground("white")
    student_total = sum(progression.values())
    factor = 100
    width = 70
    spacing = 50

#histogram title
    name = Text(Point(100, 30), "Histogram Result")
    name.setSize(20)
    name.setFill("blue")
    name.setFace("times roman")
    name.draw(win)
#histogram bar and bar colours
    bar_columns = ["Progress", "Trailer", "Retriever", "Exclude"]
    bar_colors = ["#34d399", "#fbbf24", "#fb923c", "#f87171"]

    num_bars = len(progression.keys())
    total_width = width * num_bars + spacing * (num_bars - 1)
    bar_x_coords = [i * (width + spacing) for i in range(num_bars)]

    for i, category in enumerate(progression.keys()):
        total_count = progression.get(category, 0)
        height = total_count / student_total * factor if total_count != 0 else 0
        x1 = bar_x_coords[i] + 30
        y1 = 300
        x2 = x1 + width
        y2 = y1 - height
        bar = Rectangle(Point(x1, y1), Point(x2, y2))
        bar.setFill(bar_colors[i])
        bar.draw(win)

        Text(Point(x1 + width / 2, y1 + 10), bar_columns[i]).draw(win)
        Text(Point(x1 + width / 2, y2 - 10), total_count).draw(win)
    #Total input display part
    total_out = Text(Point(100, 350), "Total Inputs")
    total_out.setSize(20)
    total_out.setFill("blue")
    total_out.setFace("times roman")
    total_out.draw(win)

     # Use the same color and size for the total count as for the bars
    total_count_text = Text(Point(160, 350), student_total)
    total_count_text.setSize(20)
    total_count_text.setFill("blue")
    total_count_text.setFace("times roman")
    total_count_text.draw(win)
    try:
        win.getMouse()
    except:
        pass
    win.close()
# Function to display the entered input data
def dis_input():
    for data in input_data:
        print(data)
# Function to save input data to a text file
def save_to_file(filename="output.txt"):
    with open(filename, "w") as file:
        for data in input_data:
            file.write(data + "\n")
# Main program logic
def main():
    pass_credits = get_credits("pass")
    defer_credits = get_credits("defer")
    fail_credits = get_credits("fail")
    # Determine the outcome based on the input
    outcome = get_outcome(pass_credits, defer_credits, fail_credits)
    if outcome is None:
        print("Total incorrect!")
        return main()
    # Update the progression dictionary based on the outcome
    progression[outcome] += 1
    formatted_outcome = format_outcome(outcome)
    print(formatted_outcome)
    # Store the input data
    input_data.append(f"({outcome}: {pass_credits}, {defer_credits}, {fail_credits})")

    # Ask if the user wants to continue entering data
    if ask_continue():
        return main()
    
    # Draw the histogram 
    draw_histogram()
    print("\npart 2:")
    print(" ")
    #display status with inputs
    dis_input()

    # Save the output to a text file
    save_to_file()
    print("\nResults saved to output.txt")
# Run the main program
main()
