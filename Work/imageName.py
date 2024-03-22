import os

filepath = "C:/Users/karen.vardanyan/Desktop/Truck1"

for image in os.listdir(filepath):
    file = os.path.join(filepath, image)

    if os.path.isfile(file) and image.endswith("_2_4_0.jpg"):
        new_name = image.replace("_2_4_0.jpg", ".jpg")
        os.rename(file, os.path.join(filepath, new_name))
