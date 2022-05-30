from PIL import Image, ImageDraw, ImageFont
import os
import csv
import tkinter as tk
from tkinter import messagebox, ttk, filedialog

def senior_name_img(filename, destination):
    #load image
    try:
        img = Image.open(filename)
    except:
        print("Error opening image:", filename)
        return
    filename = filename.split("/")[-1]
    img_width = img.size[0]
    img_height = img.size[1]

    # get arguments
    name = filename.split("_")
    name[-1] = name[-1].split(".")[0]
    last = name[0]
    last = last[0].upper() + last[1:]
    first = name[1]
    first = first[0].upper() + first[1:]
    name = first + " " + last
    # name = input("Type name: ")
    col = "black"
    color = (255, 255, 255) if col == "white" else (0, 0, 0)

    #calculate position of name so it's centered
    font_size = int((img_width+img_height)/35)
    myFont = ImageFont.truetype('br.ttf', font_size)

    name_size = myFont.getsize(name)
    x = (img_width - name_size[0]) / 2
    y = img_height - name_size[1] - img_height/25
    pos = (int(x), int(y))

    #write and save image with text
    text_img = ImageDraw.Draw(img)

    text_img.rectangle(((x-5, y-5), (x+name_size[0]+5, y+name_size[1]+5)), fill=(255,255,255))
    text_img.text(xy=pos, text=name, font=myFont, fill=color)

    folder = destination + "/"
    try:
        img.save(folder + filename[:filename.find(".")] + "_text.jpg", quality=95)
    except OSError:
        print("Saving " + filename +  " did not work")

def baby_name_img(filename, destination, csv_file):
    #load image
    try:
        img = Image.open(filename)
    except:
        print("Error opening image:", filename)
        return

    filename = filename.split("/")[-1]
    img_width = img.size[0]
    img_height = img.size[1]

    # get arguments
    name = filename.split("_")
    name[-1] = name[-1].split(".")[0]
    last = name[0]
    first = name[1]
    name = (first + " " + last).lower()
    try:
        name = csv_file[name]
    except:
        print("Name not found in csv file: ", (first + " " + last).lower())
        return

    col = "black"
    color = (255, 255, 255) if col == "white" else (0, 0, 0)

    #calculate position of name so it's centered
    font_size = int((img_width+img_height)/20)
    myFont = ImageFont.truetype('br.ttf', font_size)

    name_size = myFont.getsize(name)
    x = (img_width - name_size[0]) / 2
    y = img_height - name_size[1] - img_height/25
    pos = (int(x), int(y))

    #write and save image with text
    text_img = ImageDraw.Draw(img)

    text_img.rectangle(((x-5, y-5), (x+name_size[0]+5, y+name_size[1]+5)), fill=(255,255,255))
    text_img.text(xy=pos, text=name, font=myFont, fill=color)

    folder = destination + "/"
    try:
        img.save(folder + filename[:filename.find(".")] + "_text.jpg", quality=95)
    except:
        print(filename, "did not work")
        return

def run_loop(directory_name, destination_dir, csv_file, baby_or_senior):
    if(directory_name == "" or destination_dir == "" or baby_or_senior == ""):
        tk.messagebox.showinfo("Error", "Please fill in all required fields.")
        return
    if(baby_or_senior == "b" and csv_file == ""):
        tk.messagebox.showinfo("Error", "To select Baby, you must provide a path to a csv file.")
        return

    if(baby_or_senior == "b"):
        dict = {}
        with open(csv_file, "r") as file:
            baby_numbers = csv.reader(file)
            for lines in baby_numbers:
                dict[lines[0].lower()] = lines[1]

    for f in os.listdir(directory_name):
        if(f.endswith(".jpg") or f.endswith(".JPG") or f.endswith(".jpeg") or f.endswith(".JPEG")):
            if baby_or_senior == "b":
                baby_name_img(directory_name + "/" + f, destination_dir, dict)
            else:
                senior_name_img(directory_name + "/" + f, destination_dir)
        else:
            print(f + " is not a jpg file")

def folder_select(root, stringvar):
    filename = filedialog.askdirectory()
    selected = ttk.Label(root, text=filename)
    selected.pack()
    stringvar.set(filename)

def file_select(root, stringvar):
    filename = filedialog.askopenfilename()
    selected = ttk.Label(root, text=filename)
    selected.pack()
    stringvar.set(filename)

def main():
    #establish the tkinter window
    root = tk.Tk()
    root.title("Add Text to Picture")
    window_width = 450
    window_height = 450
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coord = int(screen_width/2 - window_width/2)
    y_coord = int(screen_height/2 - window_height/2)
    root.geometry(f"{window_width}x{window_height}+{x_coord}+{y_coord}")

    #store directories/csv
    directory_name = tk.StringVar()
    destination_dir = tk.StringVar()
    csv_file = tk.StringVar()
    baby_or_senior = tk.StringVar()

    #create the widgets
    #input
    input_label = ttk.Label(root, text="Choose the input folder here:")
    input_label.pack(fill='x', expand=True)

    input_entry = ttk.Button(root, text="Select Folder", command=lambda: folder_select(root, directory_name))
    input_entry.pack(fill='x', expand=True)

    #output
    destination_label = ttk.Label(root, text="Paste the path to the destination folder here:")
    destination_label.pack(fill='x', expand=True)

    destination_entry = ttk.Button(root, text="Select Folder", command=lambda: folder_select(root, destination_dir))
    destination_entry.pack(fill='x', expand=True)

    #csv
    csv_label = ttk.Label(root, text="Paste the path to the csv file here:")
    csv_label.pack(fill='x', expand=True)

    csv_entry = ttk.Button(root, text="Select File", command=lambda: file_select(root, csv_file))
    csv_entry.pack(fill='x', expand=True)

    #baby or senior
    baby_or_senior_label = ttk.Label(root, text="Baby or Senior?")
    baby_or_senior_label.pack(fill='x', expand=True)

    baby = ttk.Radiobutton(root, text="Baby", value="b", variable=baby_or_senior)
    baby.pack(fill='x', expand=True)
    senior = ttk.Radiobutton(root, text="Senior", value="s", variable=baby_or_senior)
    senior.pack(fill='x', expand=True)

    #submit button
    submit = ttk.Button(root, text="Submit", command=lambda: run_loop(directory_name.get(), destination_dir.get(), csv_file.get(), baby_or_senior.get()))
    submit.pack(fill='x', expand=True, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()