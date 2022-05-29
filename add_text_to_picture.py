from PIL import Image, ImageDraw, ImageFont
import os
import csv

def senior_name_img(filename, destination):
    #load image
    try:
        img = Image.open(filename)
    except:
        print("Error opening image:", filename)
        return
    filename = filename.split("/")[1]
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
        print(filename, "did not work")

def baby_name_img(filename, destination, csv_file):
    #load image
    try:
        img = Image.open(filename)
    except:
        print("Error opening image:", filename)
        return

    filename = filename.split("/")[1]
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

def main():
    dict = {}
    with open("Test Baby.csv", "r") as file:
        csv_file = csv.reader(file)
        for lines in csv_file:
            dict[lines[0].lower()] = lines[1]

    directory_name = "input"
    destination_dir = "output"
    for f in os.listdir(directory_name):
        if(f.endswith(".jpg") or f.endswith(".JPG") or f.endswith(".jpeg") or f.endswith(".JPEG")):
            baby_name_img(directory_name + "/" + f, destination_dir, dict)
        else:
            print(f)

if __name__ == "__main__":
    main()