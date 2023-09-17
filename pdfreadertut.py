from tkinter import *
import PyPDF2
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
from pdftask import place_logo, display_txtbox, extract_img, place_icon, show_imgs, img_resize

pdf_content = []
all_imgs = []
img_idx = [0]
displayed_img = []

#carousel btn functions
def R_arrow(all_imgs,current_img, carousel_txt):
    if img_idx[-1]< len (all_imgs) - 1:
        new_idx = img_idx[-1] + 1
        img_idx.pop()
        img_idx.append(new_idx)
        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()
        new_img = all_imgs[img_idx[-1]]
        current_img = show_imgs(new_img)
        displayed_img.append(current_img)
        carousel_txt.set("image" + str(img_idx[-1]+ 1)+ " out of " +str(len(all_imgs)))


def L_arrow(all_imgs,current_img, carousel_txt):
    if img_idx[-1] >= 1:
        new_idx = img_idx[-1] - 1
        img_idx.pop()
        img_idx.append(new_idx)
        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()
        new_img = all_imgs[img_idx[-1]]
        current_img = show_imgs(new_img)
        displayed_img.append(current_img)
        carousel_txt.set("image" + str(img_idx[-1]+ 1)+ " out of " +str(len(all_imgs)))


def copy_txt(content):
    root.clipboard_clear()
    root.clipboard_append(content[-1])

def save_all(images):
    counter = 1
    for i in images:
        if i.mode != "RGB":
            i = i.convert("RGB")
        i.save("img"+ str(counter)+".png", format="png")
        counter +=1

def save_img(i):
    if i.mode != "RGB":
        i = i.convert("RGB")
    i.save("img.png", format="png")


#main window specs
root= Tk()
root.geometry('+%d+%d'%(350,10))


##header - logo and button placement
header = Frame(root,width=600, height=300)
header.grid(columnspan=3, rowspan=2, row=0)





##main content - extraction of content
ext_content = Frame(root, width=800, height=175, bg="#64495B")
ext_content.grid(columnspan=3, rowspan=2, row=4)




#open pdf 
def open_file():
    #clear img array for new image list
    for i in img_idx:
        img_idx.pop()
    img_idx.append(0)
    
    
    load_text.set("loading...")
    file = askopenfile(parent=root, mode='rb', title="Choose a file", filetype=[("Pdf file", "*.pdf")])
    if file:
        read_pdf = PyPDF2.PdfReader(file)
        page = read_pdf.pages[0]
        page_content = page.extract_text()
        #page_content = page_content.encode('cp1252')
        page_content = page_content.replace('\u2122', "'") 
        pdf_content.append(page_content)
        
        #clear images on loading of new pdf
        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()

        for i in range(0,len(all_imgs)):
            all_imgs.pop()


        #img extraction
        images = extract_img(page)

        for i in images:
            all_imgs.append(i)

        img = images[img_idx[-1]]
        curr_img = show_imgs(img)
        displayed_img.append(curr_img)


        #textbox for content
        display_txtbox(page_content, 4, 0, root)
        load_text.set("Browse")

    ##img carousel
    img_row = Frame(root,width=800, height=70, bg="#b8b8b8")
    img_row.grid(columnspan=3, rowspan=1, row=2)
    carousel_txt = StringVar()
    carousel = Label(root, textvariable= carousel_txt, font=("roboto",10))
    carousel_txt.set("image" + str(img_idx[-1]+ 1)+" out of "+str(len(all_imgs)))
    carousel.grid(row=2, column=1)
    place_icon('arrow_l.png', 2, 0, E, lambda:L_arrow(all_imgs,displayed_img, carousel_txt))
    place_icon('arrow_r.png', 2, 2, W, lambda:R_arrow(all_imgs,displayed_img, carousel_txt))
    ##button divider
    btn_row = Frame(root,width=800, height=70, bg="#c8c8c8")
    btn_row.grid(columnspan=3, rowspan=1, row=3)
    ##buttons
    copyTxt_btn = Button(root, text="copy text",font=("roboto",10),height=1, width=15, command=lambda:copy_txt(pdf_content))
    savePics_btn = Button(root, text="save all images",font=("roboto",10),height=1, width=15, command=lambda:save_all(all_imgs))
    savePic_btn = Button(root, text="save image",font=("roboto",10),height=1, width=15, command=lambda:save_img(all_imgs[img_idx[-1]]))

    copyTxt_btn.grid(row=3, column=0)
    savePics_btn.grid(row=3, column=1)
    savePic_btn.grid(row=3, column=2)



#instructions
directions = Label(root, text='Select a PDF file for review', font='Roboto')
directions.grid(column=2, row=0)

#load button
load_text = StringVar()
load_btn = Button(root, textvariable=load_text, font="Roboto", bg="#331E2C", fg="#64495B", height=2, width=15, command=lambda:open_file())
load_text.set("Browse")
load_btn.grid(column=2, row=1, sticky=NE, padx=50)

#logo 
place_logo('fakepdflogo.png',0, 0)



#bottom panel
canvas = Canvas(root,width=600, height=150)
canvas.grid(columnspan=3)

root.mainloop()