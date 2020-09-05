import matplotlib.pyplot as plt
import cv2
import imutils
import pytesseract as pt
from tkinter import *
from tkinter import messagebox


# ploting the images
def plot_img(img1, img2, title1="", title2=""):
    fig = plt.figure(figsize=[5, 5])
    # axis 1
    ax1 = fig.add_subplot(121)
    ax1.imshow(img1, cmap="gray")
    ax1.set(xticks=[], yticks=[], title=title1)

    # axis 2
    ax2 = fig.add_subplot(122)
    ax2.imshow(img2, cmap="gray")
    ax2.set(xticks=[], yticks=[], title=title2)


# read the image using numpy

print("\n1.car-1\n2.car-2\n3.car-3")
a = int(input("Enter the choice of car : "))
if a == 1:
    path = "./image/a.jpg"
elif a == 2:
    path = "./image/b.jpg"
else:
    path = "./image/c.jpg"

image = cv2.imread(path)

# resizing the image
image = imutils.resize(image, width=500)
cv2.imshow("original image", image)

# delaying the next image till this image gets closed
cv2.waitKey(8000) #delaying till 5 sec
cv2.destroyAllWindows()

plot_img(image, image, title1="original1", title2="original1")
# image color to gray
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
plot_img(image, gray, title1="original1", title2="gray")
cv2.imshow('gray image', gray)
cv2.waitKey(8000)
cv2.destroyAllWindows()
#  Noise removal with iterative bilateral filters(which removes the noise while filtering the edges)
blur = cv2.bilateralFilter(gray, 11, 90, 90)
plot_img(gray, blur, title1="gray", title2="Blur")
cv2.imshow("blurred  image:", blur)
cv2.waitKey(8000)
cv2.destroyAllWindows()

# blurring the edges of grayscale image
edges = cv2.Canny(blur, 30, 200)
plot_img(blur, edges, title1="Blur", title2="Edges")
cv2.imshow("canny  image:", edges)
cv2.waitKey(8000)
cv2.destroyAllWindows()

# Finding the contours based edges
cnts, new = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# coping the image as secondary
image_copy = image.copy()

# Drawing all the contours edges of the original image
_ = cv2.drawContours(image_copy, cnts, -1, (255, 0, 255), 2)
plot_img(edges, image_copy, title1="Edges", title2="Contours")
cv2.imshow("contours  image:", image_copy)
cv2.waitKey(8000)
cv2.destroyAllWindows()
print("number of iteration of draw counter has passed: ", len(cnts))



# sort the contours keeping the minimum area as 30
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
image_reduce_cnts = image.copy()
_ = cv2.drawContours(image_reduce_cnts, cnts, -1, (255, 0, 255), 2)
plot_img(image_copy, image_reduce_cnts , title1="Contours", title2="Reduced")
cv2.imshow("reduced  image:" , image_reduce_cnts)
cv2.waitKey(8000)
cv2.destroyAllWindows()

print("number of iteration passed by reducing the edges : ", len(cnts))

plate = None
for c in cnts:
    perimeter = cv2.arcLength(c, True)
    edges_count = cv2.approxPolyDP(c, 0.02 * perimeter , True)
    if len(edges_count) == 4 :
        x, y, w, h = cv2.boundingRect(c)
        plate = image[y:y + h, x:x + w]
        break
cv2.imwrite("plate.png", plate)
plot_img(plate, plate, title1="plate", title2="plate")
cv2.imshow("Number Plate Image : ", plate)
cv2.waitKey(8000)
cv2.destroyAllWindows()

pt.pytesseract.tesseract_cmd = r'C:\Users\admin\AppData\Local\Tesseract.exe'
no_plate = pt.image_to_string(plate, lang='eng')
print("the number plate of car is: ", no_plate)


def convert():
    c_entry = input_entry.get()
    if c_entry == 'HR26DK8337':
        string_display = "Name : harish\nAddress : ministori visual tech in bangalore in vijayanagar\nPhone no : 9582645123"
        label2 = Label(root)
        label2["text"] = string_display
        label2.grid(row=1 , column=1)
        cv2.imshow("original image", image)
        messagebox.showinfo("Car number plate Detector", "Successfully Number plate has been analysed : "+no_plate)
    if c_entry == 'KLOLCC 5995':
        string_display = "Name : chandran\nAddress : manthon niyali megalaya-552326\nPhone no : 9529876123"
        label2 = Label(root)
        label2["text"] = string_display
        label2.grid(row=1 , column=1)
        cv2.imshow("original image", image)
        messagebox.showinfo("Car number plate Detector", "Successfully Number plate has been analysed : "+no_plate)
    if c_entry == 'DZI7 YXR':
        string_display = "Name : vijaya\nAddress : kadoor village nprayya nagar haydrabad\nPhone no : 92954611233"
        label2 = Label(root)
        label2["text"] = string_display
        label2.grid(row=1 , column=1)
        cv2.imshow("original image", image)
        messagebox.showinfo("Car number plate Detector", "Successfully Number plate has been analysed : "+no_plate)



# creating Tk window
root = Tk()

# setting geometry of tk window
root.geometry('500x350+100+200')

#title of project
root.title('Car Number Plate Detector - (owner file address)')

# Back ground colour
root.config(bg="dark orange")

# Lay out widgets
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)

inputNumber = StringVar()
var = StringVar()
input_label = Label(root, text="car plate number", font=("times new roman", 20, "bold"), bg="white", fg="green", background="#09A3BA", foreground="#FFF").place(x=150,y=40)
input_entry = Entry(root, textvariable=inputNumber, font=("times new roman", 15), bg="lightgray")
input_entry.grid(row=1, columnspan=2)

result_button = Button(root, text="Details", command=convert, font=("times new roman", 20, "bold"), bg="cyan")
result_button.grid(row=3, column=1)

root.mainloop()