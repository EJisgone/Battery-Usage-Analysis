# Install required packages before any imports or other code
import subprocess

try:
    subprocess.check_call(["pip", "install", "-r", "requirement.txt"])
    print("All packages installed successfully!")
except subprocess.CalledProcessError as e:
    print(f"Error occurred while installing packages: {e}")
    exit(1)  # Exit the program if package installation fails

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import pandas as pd

# Get the directory path of the current script
dir_path = os.path.dirname(os.path.abspath(__file__))

# Create the main window
root = tk.Tk()
root.title("Battery Usage Analysis Dashboard")

# Make the window a full window (maximized but not fullscreen)
root.state("zoomed")  # For Windows systems, ensures the window is maximized

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set background as a JPEG file (ensure 'background.jpg' is in the same directory)
background_image = Image.open(os.path.join(dir_path, "background.jpg"))
background_photo = ImageTk.PhotoImage(background_image.resize((screen_width, screen_height)))
canvas = tk.Canvas(root, width=screen_width, height=screen_height, highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_photo, anchor="nw")

# Add a title label
title_label = tk.Label(
    root,
    text="🔋 Battery Usage Analysis Dashboard 🔋",
    font=("Helvetica", 24, "bold"),
    bg="black",
    fg="gold",
)
title_label.place(relx=0.5, rely=0.05, anchor="center")

# Function to execute a Python file
def execute_file(file_name):
    file_path = os.path.join(dir_path, file_name)
    try:
        subprocess.check_call(["python", file_path])
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing {file_path}: {e}")

# Function to execute gone.py and exit the program
def execute_exit():
    gone_path = os.path.join(dir_path, "gone.py")
    try:
        subprocess.check_call(["python", gone_path])
        print("All files deleted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing {gone_path}: {e}")
    finally:
        root.destroy()  # Close the window and exit the program

# Function to switch to the new page
def open_analysis_page():
    # Clear the canvas
    canvas.delete("all")

    # Add the background image to the new page
    canvas.create_image(0, 0, image=background_photo, anchor="nw")

    # Add a description paragraph with enhanced content
    description = (
        "🔋 **Battery Analysis Report** 🔋\n\n"
        "Welcome to the Battery Analysis Dashboard! This tool provides a comprehensive overview "
        "of your system's battery performance. Here, you can explore detailed insights into:\n\n"
        "1. **Recent Usage**: Track how your battery has been used over time, including capacity and state.\n"
        "2. **Battery Usage**: Analyze energy drained during specific periods of activity.\n"
        "3. **Usage History**: Review historical data on battery and AC power usage.\n"
        "4. **Capacity History**: Monitor changes in your battery's full charge and design capacity.\n"
        "5. **Life Estimates**: Estimate your battery's life based on current and design capacities.\n\n"
        "Use the sidebar on the left to navigate through different sections of the dashboard. "
        "Each section provides detailed reports and visualizations to help you better understand your battery's performance.\n\n"
        "Stay informed and optimize your battery usage for better efficiency and longevity!"
    )
    description_label = tk.Label(
        root,
        text=description,
        font=("Helvetica", 14),
        bg="black",
        fg="white",
        justify="left",
        wraplength=screen_width - 300,
    )
    description_label.place(relx=0.5, rely=0.15, anchor="center")

    # Display system information and battery details
    try:
        # Read and format system information
        system_info_path = os.path.join(dir_path, "battery-report", "system_info.csv")
        system_info_df = pd.read_csv(system_info_path)
        system_info = "\n".join([f"{column.upper():<25}: {value}" for column, value in system_info_df.iloc[0].items()])

        # Read and format battery details
        battery_details_path = os.path.join(dir_path, "battery-report", "battery_details.csv")
        battery_details_df = pd.read_csv(battery_details_path)
        battery_details = "\n".join([f"{column.upper():<25}: {value}" for column, value in battery_details_df.iloc[0].items()])

        # Combine the formatted data
        formatted_data = f"SYSTEM INFORMATION\n{'-' * 20}\n{system_info}\n\nBATTERY DETAILS\n{'-' * 20}\n{battery_details}"
    except FileNotFoundError:
        formatted_data = "Error: Required CSV files not found. Please ensure extract.py ran successfully."
    except Exception as e:
        formatted_data = f"Error reading CSV files: {e}"

    # Display the formatted data higher
    data_label = tk.Label(
        root,
        text=formatted_data,
        font=("Helvetica", 12),
        bg="black",
        fg="white",
        justify="left",
        anchor="nw",
        wraplength=screen_width - 300,
    )
    data_label.place(relx=0.5, rely=0.8, anchor="center")

    # Create a sidebar frame at the bottom-left corner
    sidebar = tk.Frame(root, bg="black", width=200, height=screen_height // 2)
    sidebar.place(relx=0, rely=1, anchor="sw")

    # Add buttons to the sidebar
    button_style = {"font": ("Helvetica", 12), "bg": "gray", "fg": "white", "relief": "flat"}
    button1 = tk.Button(sidebar, text="Battery Capacity History", **button_style, command=lambda: execute_file("battery_cap_hist.py"))
    button1.pack(fill="x", pady=10, padx=10)

    button2 = tk.Button(sidebar, text="Battery Life Estimates", **button_style, command=lambda: execute_file("battery_life_estimate.py"))
    button2.pack(fill="x", pady=10, padx=10)

    button3 = tk.Button(sidebar, text="Battery Usage", **button_style, command=lambda: execute_file("battery_usage.py"))
    button3.pack(fill="x", pady=10, padx=10)

    button4 = tk.Button(sidebar, text="Recent Usage", **button_style, command=lambda: execute_file("recent_usage.py"))
    button4.pack(fill="x", pady=10, padx=10)

    button5 = tk.Button(sidebar, text="Usage History", **button_style, command=lambda: execute_file("usage_history.py"))
    button5.pack(fill="x", pady=10, padx=10)

    # Add an "Exit" button to the bottom-right corner
    exit_button = tk.Button(root, text="Exit", **button_style, command=execute_exit)
    exit_button.place(relx=1, rely=1, anchor="se")

# Function to print CSV contents
def print_csv_contents(file_name, title):
    """Reads a CSV file and prints its contents in an elegant format."""
    file_path = os.path.join(dir_path, "battery-report", file_name)
    print(f"\n{title}\n" + "-" * len(title))
    try:
        df = pd.read_csv(file_path)
        for column, value in df.iloc[0].items():
            print(f"{column.upper():<25}: {value}")
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

# Add a "Start" button
def start_button_action():
    try:
        # Hide the "Start" button
        start_button.place_forget()

        # Execute the extract.py file
        execute_file("extract.py")
        print("extract.py executed successfully!")

        # Print system info
        print_csv_contents("system_info.csv", "SYSTEM INFORMATION")

        # Print battery details
        print_csv_contents("battery_details.csv", "BATTERY DETAILS")

        # Open the analysis page
        open_analysis_page()

    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

start_button = tk.Button(
    root,
    text="Start",
    font=("Helvetica", 20, "bold"),
    bg="gold",
    fg="black",
    command=start_button_action,  # Fixed the command to call the correct function
)
start_button.place(relx=0.5, rely=0.5, anchor="center")

# Add an icon (ensure the icon file 'icon.ico' is in the same directory)
root.iconbitmap(os.path.join(dir_path, "icon.ico"))

# Keep a reference to the background image to prevent garbage collection
canvas.image = background_photo

# Run the application
root.mainloop()
