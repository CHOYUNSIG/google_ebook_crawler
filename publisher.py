from PIL import Image
import os

root = os.getcwd()

img_0 = Image.open(root + '/img/0.jpg')
print("1 page loaded.")
img_list = list()

count = 1
while(True) :
    try : 
        with Image.open(root + '/img/' + str(count) + '.jpg').convert('RGB') as img:
            img_list.append(img)
        count = count + 1
        print(str(count) + " pages loadad.")
    except :
        break

print("Saving pdf..")
img_0.save('pdf/pub.pdf', save_all=True, append_images=img_list)
print("Done.")

exit()