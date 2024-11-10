from tkinter import *
from tkinter import ttk
import os
from tkcalendar import Calendar  
import datetime

root = Tk()
root.geometry("800x800")
root.title("Taxi Booking")

# Main Frame
main_frame = Frame(root)
main_frame.pack(pady=10)

# Title Label
title_label = Label(main_frame, text="TAXI BOOKING", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

# Display Image
image_path = os.path.join("images", "Taxi-PNG-Image.png")
try:
    image = PhotoImage(file=image_path)
    imagelabel = Label(main_frame, image=image)
    imagelabel.image = image  # keep a reference to the image
    imagelabel.pack()
except Exception as e:
    print(f"Error loading image: {e}")

pickup_location = StringVar()
selected_time = StringVar()
selected_date = StringVar()
destination = StringVar()

# Define sample fare rates between locations
fare_rates = {
    ("Mount Maunganui", "bayfir"): 15,
    ("Mount Maunganui", "Toiohomai"): 20,
    ("bayfir", "Bethlehem"): 10,
    ("Bethlehem", "Pyes pa"): 12,
    ("Toiohomai", "Greeton"): 18,
    "default": 25
}

def go_to_time_date_page():
    for widget in main_frame.winfo_children():
        widget.destroy()

    next_image_path = os.path.join("images", "logo.png") 
    try:
        next_image = PhotoImage(file=next_image_path)
        image_label = Label(main_frame, image=next_image)
        image_label.image = next_image  
        image_label.pack(pady=10)
    except Exception as e:
        print(f"Error loading next page image: {e}")

    time_label = Label(main_frame, text="Choose The Time:", font=("Helvetica", 12))
    time_label.pack(pady=5)

    hour_var = StringVar()
    minute_var = StringVar()

    hours = [str(hour).zfill(2) for hour in range(24)]  
    minutes = [str(minute).zfill(2) for minute in range(0, 60, 5)]

    hour_cb = ttk.Combobox(main_frame, values=hours, textvariable=hour_var, state='readonly')
    hour_cb.set("Select Hour")
    hour_cb.pack(pady=5)

    minute_cb = ttk.Combobox(main_frame, values=minutes, textvariable=minute_var, state='readonly')
    minute_cb.set("Select Minute")
    minute_cb.pack(pady=5)

    calendar_label = Label(main_frame, text="Select Date:", font=("Helvetica", 12))
    calendar_label.pack(pady=5)

    cal = Calendar(main_frame, selectmode='day', year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day)
    cal.pack(pady=10)

    global time_display_label
    time_display_label = Label(main_frame, text="", font=("Helvetica", 12))
    time_display_label.pack(pady=10)

    def update_selection():
        hour = hour_var.get()
        minute = minute_var.get()
        date = cal.get_date()

        if hour != "Select Hour" and minute != "Select Minute":
            selected_time.set(f"{hour}:{minute}")
            selected_date.set(date)
            time_display_label.config(text=f"Selected Time: {hour}:{minute}, Date: {date}")
            print(f"Selected Time: {hour}:{minute}, Date: {date}")

    hour_cb.bind("<<ComboboxSelected>>", lambda event: update_selection())
    minute_cb.bind("<<ComboboxSelected>>", lambda event: update_selection())
    cal.bind("<<CalendarSelected>>", lambda event: update_selection())

    pickup_location_button = Button(main_frame, text="Continue to Pickup Location", font=("Helvetica", 12), command=go_to_pickup_page)
    pickup_location_button.pack(pady=(20, 5))

def go_to_pickup_page():
    for widget in main_frame.winfo_children():
        widget.destroy()

    time_label = Label(main_frame, text=f"Selected Time: {selected_time.get()}, Date: {selected_date.get()}", font=("Helvetica", 12))
    time_label.pack(pady=10)

    pickup_label = Label(main_frame, text="Choose Pickup Location:", font=("Helvetica", 12))
    pickup_label.pack(pady=5)

    locations = ["Mount Maunganui", "bayfir", "Toiohomai", "Bethlehem", "Pyes pa", "Greeton"]
    pickup_location_cb = ttk.Combobox(main_frame, values=locations, textvariable=pickup_location, state='readonly')
    pickup_location_cb.set("Select Pickup Location")
    pickup_location_cb.pack(pady=5)

    confirm_button = Button(main_frame, text="Confirm Pickup Location", font=("Helvetica", 12), command=go_to_destination_page)
    confirm_button.pack(pady=(20, 5))

def go_to_destination_page():
    for widget in main_frame.winfo_children():
        widget.destroy()

    Label(main_frame, text=f"Selected Time: {selected_time.get()}, Date: {selected_date.get()}", font=("Helvetica", 12)).pack(pady=10)
    Label(main_frame, text=f"Pickup Location: {pickup_location.get()}", font=("Helvetica", 12)).pack(pady=10)

    destination_label = Label(main_frame, text="Choose Destination:", font=("Helvetica", 12))
    destination_label.pack(pady=5)

    destinations = ["Mount Maunganui", "bayfir", "Toiohomai", "Bethlehem", "Pyes pa", "Greeton"]
    destination_cb = ttk.Combobox(main_frame, values=destinations, textvariable=destination, state='readonly')
    destination_cb.set("Select Destination")
    destination_cb.pack(pady=5)

    confirm_button = Button(main_frame, text="Confirm Destination", font=("Helvetica", 12), command=confirm_destination)
    confirm_button.pack(pady=(20, 5))

def calculate_fare(pickup, destination):
    return fare_rates.get((pickup, destination)) or fare_rates.get("default")

def confirm_destination():
    pickup = pickup_location.get()
    dest = destination.get()
    fare = calculate_fare(pickup, dest)
    
    print(f"Pickup Location: {pickup}, Destination: {dest}, Fare: ${fare}") 

    Label(main_frame, text=f"Destination Confirmed: {dest}", font=("Helvetica", 12)).pack(pady=5)
    Label(main_frame, text=f"Estimated Fare: ${fare}", font=("Helvetica", 12, "bold")).pack(pady=10)

    confirm_booking_button = Button(main_frame, text="Confirm Booking", font=("Helvetica", 12), command=lambda: show_final_confirmation(pickup, dest, fare))
    confirm_booking_button.pack(pady=(20, 5))

def show_final_confirmation(pickup, destination, fare):
    for widget in main_frame.winfo_children():
        widget.destroy()

    Label(main_frame, text="Booking Confirmation", font=("Helvetica", 16, "bold")).pack(pady=10)
    Label(main_frame, text=f"Time: {selected_time.get()}", font=("Helvetica", 12)).pack(pady=5)
    Label(main_frame, text=f"Date: {selected_date.get()}", font=("Helvetica", 12)).pack(pady=5)
    Label(main_frame, text=f"Pickup Location: {pickup}", font=("Helvetica", 12)).pack(pady=5)
    Label(main_frame, text=f"Destination: {destination}", font=("Helvetica", 12)).pack(pady=5)
    Label(main_frame, text=f"Fare: ${fare}", font=("Helvetica", 12, "bold")).pack(pady=10)
    Label(main_frame, text="Thank you for booking with us!", font=("Helvetica", 12)).pack(pady=10)

    home_button = Button(main_frame, text="Home", font=("Helvetica", 12), command=go_home)
    home_button.pack(pady=(20, 5))

def go_home():
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    title_label = Label(main_frame, text="TAXI BOOKING", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)

    try:
        image = PhotoImage(file=image_path)
        imagelabel = Label(main_frame, image=image)
        imagelabel.image = image
        imagelabel.pack()
    except Exception as e:
        print(f"Error loading image: {e}")

    book_now_button = Button(main_frame, text="BOOK NOW", font=("Helvetica", 12), command=go_to_time_date_page)
    book_now_button.pack(pady=(20, 5))

book_now_button = Button(main_frame, text="BOOK NOW", font=("Helvetica", 12), command=go_to_time_date_page)
book_now_button.pack(pady=(20, 5))

root.mainloop()
