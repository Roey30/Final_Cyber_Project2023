"""

"""
# IMPORTS:
import io
import os
import shutil
from tkinter import messagebox, filedialog, ttk, FLAT, Spinbox
import tkinter as tk
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageOps
import socket
import ssl
import pickle

# CONSTANTS: 
# CONNECTIONS VARIABLES:
HOST_NAME = "127.0.0.1"
PORT = 8443
MSG_LEN = 1024
RESULT = 0

# CONNECTIONS PROTOCOL:
LOG_IN_CLIENT_PROTOCOL = 'LICP'
SIGN_UP_CLIENT_PROTOCOL = 'SICP'
PICTURES_TO_SERVER_PROTOCOL = 'ptsp'
PICTURES_TO_CLIENT_PROTOCOL = 'ptcp'
CLIENT_BACK_TO_START_PROTOCOL = 'CBTSP'
CLIENT_LOG_OUT_PROTOCOL = 'quit'

# LISTS OF VARIABLES:
STORAGE_USER_NAME = []
STORAGE_USER_PASSWORD = []
STORAGE_PICTURE = []
STORAGE_PICTURE_VER1 = []
STORAGE_PICTURE_VER2 = []
STORAGE_PATH_PICTURE = []
PANEL_STORAGE = []
UNDO_STACK = []

# USERNAME AND PASSWORD:
USER_NAME = ''
PASSWORD = ''

# IMAGE RELATED:
EDIT_IMAGE = ''
EDIT_IMAGE_PATH = ''
IMAGE_PIL = ''
IMG = ''
PANEL_EDITED_IMAGE = ''
IMAGE_AFTER_EDIT = ''
SELECTED_IMAGE_TO_EDIT = ''
NUMBER_PICTURE = 0
COUNT_PICTURE = 1
COUNT_PICTURE_VAR2 = 0
picture = ''
VERSION = ''
IMG_TK = ''

PANEL = None
ACCESS = False
IF_IMAGE_PRESSED = False

# BUTTONS:
UPLOAD_PICTURE_BUTTON_PICTURE_PAGE = ''
BUTTON_IMAGE = ''
RESET_BUTTON = ''
UPLOAD_EDIT_BUTTON = ''
DOWN_LOAD_PICTURE_BUTTON = ''
SELECT_IMAGE_BUTTON = ''
SIGN_UP_BUTTON = ''
NO_PICTURE_WAS_SELECTED_BUTTON = ''

# LABELS:
LIMIT_LABEL = ''
NAME_FIRST_LABEL = ''
NO_EDIT_LABEL = ''
SIGN_UP_TAKEN_LABEL = ''
NO_UNDO_LABEL = ''
IMAGE_INFO_LABEL = ''
SIGN_UP_WRONG_LABEL = ''
NO_PICTURE_SELECTED = ''

# FONTS AND COLORS(FOR LABELS AND BUTTONS):
LARGE_FONT = ("Times New Roman", 35, "bold")
COLOR = "#8370EE"
BACKGROUND_BUTTON_COLOR = "#4B0082"
BACKGROUND_COLOR = "#616161"

NUMBER_PAGE = 3


def exit_window():
    """

    :return:
    """
    global root
    print("GoodBye")
    try:
        msg = CLIENT_LOG_OUT_PROTOCOL
        conn.sendall(pickle.dumps(msg))
    except ssl.SSLError as err:
        print(f"Something went wrong with the server: {err}")
        conn.close()
    finally:
        root.quit()
        all_files = os.listdir(PHOTOS_SAVED_FILE)
        for file_name in all_files:
            file_path = os.path.join(PHOTOS_SAVED_FILE, file_name)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)


def exist_check():
    """

    :return:
    """
    if pickle.loads(conn.recv(MSG_LEN)) == 'True':
        return True
    else:
        return False


def signup_function(entry_user_name, entry_password, frame):
    """

    :param entry_user_name:
    :param entry_password:
    :param frame:
    :return:
    """
    global USER_NAME, PASSWORD, SIGN_UP_BUTTON, SIGN_UP_WRONG_LABEL, SIGN_UP_TAKEN_LABEL
    USER_NAME = entry_user_name.get()
    PASSWORD = entry_password.get()
    msg = SIGN_UP_CLIENT_PROTOCOL, USER_NAME, PASSWORD
    if SIGN_UP_WRONG_LABEL == '' and SIGN_UP_TAKEN_LABEL == '':
        SIGN_UP_WRONG_LABEL = tk.Label(frame, text="Something went wrong please try again", bg="black", fg="white",
                                       font=("Arial", 12, "bold"), padx=20, pady=20,
                                       bd=3, relief=tk.RAISED)
        SIGN_UP_TAKEN_LABEL = tk.Label(frame, text="This user name already used", bg="black", fg="white",
                                       font=("Arial", 12, "bold"), padx=20,
                                       pady=20, bd=3, relief=tk.RAISED)
    if USER_NAME == '' or PASSWORD == '':
        SIGN_UP_TAKEN_LABEL.place_forget()
        SIGN_UP_WRONG_LABEL.place(x=300, y=550, anchor=tk.CENTER, width=500, height=50)
        return
    else:
        conn.sendall(pickle.dumps(msg))
        if exist_check():
            SIGN_UP_WRONG_LABEL.place_forget()
            SIGN_UP_TAKEN_LABEL.place(x=300, y=550, anchor=tk.CENTER, width=500, height=50)
        else:
            SIGN_UP_WRONG_LABEL.place_forget()
            SIGN_UP_TAKEN_LABEL.destroy()
            tk.Label(frame, text="Successful Sign Up ", bg="black", fg="white", font=("Arial", 12, "bold"), padx=20,
                     pady=20,
                     bd=3, relief=tk.RAISED).place(x=300, y=550, anchor=tk.CENTER, width=300, height=50)
            SIGN_UP_BUTTON.config(state='disabled')
            print(f"Your username -> {USER_NAME}")
            print(f"Your the password -> {PASSWORD} <-")
            # sends the username and the password to server for storage them in the database
            print(f"msg: {msg}")
            STORAGE_USER_NAME.append(USER_NAME)
            STORAGE_USER_PASSWORD.append(PASSWORD)


def select_image(frame, SELECT_IMAGE_BUTTON_value):
    """

    :param frame:
    :param SELECT_IMAGE_BUTTON_value:
    :return:
    """
    global NUMBER_PICTURE, EDIT_IMAGE, PANEL_STORAGE, LIMIT_LABEL, NO_PICTURE_SELECTED
    LIMIT_LABEL = tk.Label(frame, text="You can upload up to four pictures", bg=COLOR, fg="white",
                           font=("Arial", 12, "bold"), padx=20, pady=20, bd=3,
                           relief=tk.RAISED)
    if NUMBER_PICTURE >= 0:
        if NO_PICTURE_SELECTED != '':
            NO_PICTURE_SELECTED.place_forget()
        if NO_UNDO_LABEL != '':
            NO_UNDO_LABEL.place_forget()
    if EDIT_IMAGE == '':
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                global PANEL
                image = Image.open(file_path)
                picture_name = os.path.basename(file_path)
                STORAGE_PATH_PICTURE.append((file_path, picture_name, 1))
                image = image.resize((200, 200), Image.LANCZOS)
                image = ImageTk.PhotoImage(image)
                if PANEL is None:
                    PANEL = tk.Label(frame, image=image, relief=FLAT, bd=4, bg="black")
                    PANEL.image = image
                    PANEL.place(x=120 + (240 * NUMBER_PICTURE), y=200, anchor=tk.CENTER)
                    PANEL_STORAGE.append(PANEL)
                    NUMBER_PICTURE += 1
                else:
                    PANEL.configure(image=image, relief=FLAT, bd=4, bg="black", )
                    PANEL.image = image
                PANEL = None
                if NUMBER_PICTURE == 4:
                    LIMIT_LABEL.place(x=500, y=500, anchor=tk.CENTER, width=300, height=50)
                    SELECT_IMAGE_BUTTON_value.config(state='disabled')
            except Exception as e:
                messagebox.showerror("Error", "Failed to open image\n{}".format(e))
    else:
        frame.master.switch_frame(frame.master.picture_page_frames[0], 2)


def undo_selected_picture(SELECT_IMAGE_BUTTON_value, frame):
    """

    :param SELECT_IMAGE_BUTTON_value:
    :param frame:
    :return:
    """
    global STORAGE_PATH_PICTURE, PANEL_STORAGE, NUMBER_PICTURE, LIMIT_LABEL, NO_UNDO_LABEL
    NO_UNDO_LABEL = tk.Label(frame, text="Cant undo - No picture was selected", bg=COLOR, fg="white",
                             font=("Arial", 12, "bold"), padx=20, pady=20,
                             bd=3, relief=tk.RAISED)
    if NUMBER_PICTURE == 0:
        NO_UNDO_LABEL.place(x=840, y=665, anchor=tk.CENTER, width=280, height=20)
    else:
        NO_UNDO_LABEL.place_forget()
        if len(STORAGE_PATH_PICTURE) != 0 and len(PANEL_STORAGE) != 0:
            STORAGE_PATH_PICTURE.pop()
            PANEL_STORAGE.pop().place_forget()
            NUMBER_PICTURE -= 1
            LIMIT_LABEL.place_forget()
            SELECT_IMAGE_BUTTON_value.config(state='active')


def login_function(entry_user_name, entry_password, frame):
    """

    :param entry_user_name:
    :param entry_password:
    :param frame:
    :return:
    """
    # sends the username and the password to the sever for checking them in the database
    global ACCESS, USER_NAME
    try:
        ACCESS = False
        print(f'User name: {entry_user_name.get()}, Password: {entry_password.get()}')
        msg = LOG_IN_CLIENT_PROTOCOL, entry_user_name.get(), entry_password.get()
        print(f"The msg: {msg}")
        incorrect_label = tk.Label(frame, text="Your username or password is incorrect", bg="black", fg="white",
                                   font=("Arial", 12, "bold"), padx=20,
                                   pady=20, bd=3, relief=tk.RAISED)
        connected_label = tk.Label(frame, text="This user name is already connected", bg="black", fg="white",
                                   font=("Arial", 12, "bold"), padx=20,
                                   pady=20, bd=3, relief=tk.RAISED)
        conn.sendall(pickle.dumps(msg))
        access = pickle.loads(conn.recv(MSG_LEN))
        if access == 'True':
            print(f'Yes - access = {access}')
            USER_NAME = entry_user_name.get()
            frame.master.create_picture_page_frames()
            frame.master.switch_frame(frame.master.picture_page_frames[0], 3)
        elif access == 'Taken':
            print(f'No - access = {access}')
            incorrect_label.destroy()
            connected_label.place(x=300, y=550, anchor=tk.CENTER, width=500, height=50)
        elif access == 'False':
            print(f'No - access = {access}')
            connected_label.destroy()
            incorrect_label.place(x=300, y=550, anchor=tk.CENTER, width=500, height=50)
    except ssl.SSLError as err:
        print(f"Something went wrong with the server: {err}")
        conn.close()
        root.quit()


def marked_image(image, button_image, frame, path, picture_name, pic_ver, image_PIL):
    """

    :param image:
    :param button_image:
    :param frame:
    :param path:
    :param picture_name:
    :param pic_ver:
    :param image_PIL:
    :return:
    """
    global EDIT_IMAGE, BUTTON_IMAGE, IF_IMAGE_PRESSED, EDIT_IMAGE_PATH, \
        SELECTED_IMAGE_TO_EDIT, RESET_BUTTON, picture, NO_PICTURE_WAS_SELECTED_BUTTON, VERSION, IMAGE_PIL, PANEL_EDITED_IMAGE
    SELECTED_IMAGE_TO_EDIT = path
    EDIT_IMAGE = image
    VERSION = pic_ver
    picture = picture_name
    IMAGE_PIL = image_PIL
    if not IF_IMAGE_PRESSED and VERSION == 1:
        RESET_BUTTON = tk.Button(frame, text="Resets marked picture", bg=COLOR, fg="white",
                                 font=("Arial", 12, "bold"), padx=20, pady=20, bd=3,
                                 relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                                 command=lambda: reset_marked_image())
        BUTTON_IMAGE = button_image
        BUTTON_IMAGE.config(bd=4, bg="white")
        if NO_PICTURE_WAS_SELECTED_BUTTON != '':
            NO_PICTURE_WAS_SELECTED_BUTTON.place_forget()
        RESET_BUTTON.place(x=900, y=660, anchor=tk.CENTER, width=350, height=30)
        IF_IMAGE_PRESSED = True
    else:
        BUTTON_IMAGE.config(relief=FLAT, bd=4, bg="black")
        BUTTON_IMAGE = button_image
        BUTTON_IMAGE.config(bd=4, bg="white")
        if NO_PICTURE_WAS_SELECTED_BUTTON != '':
            NO_PICTURE_WAS_SELECTED_BUTTON.place_forget()


def reset_marked_image():
    """

    :return:
    """
    global BUTTON_IMAGE, EDIT_IMAGE, IF_IMAGE_PRESSED, picture
    if BUTTON_IMAGE is not None:
        EDIT_IMAGE = ''
        picture = ''
        BUTTON_IMAGE.config(relief=FLAT, bd=4, bg="black")
        IF_IMAGE_PRESSED = False
        RESET_BUTTON.destroy()


def print_pictures(picture_path, frame, what_picture_page):
    """

    :param picture_path:
    :param frame:
    :param what_picture_page:
    :return:
    """
    global PANEL, COUNT_PICTURE, EDIT_IMAGE_PATH, SELECTED_IMAGE_TO_EDIT, COUNT_PICTURE_VAR2, PANEL_EDITED_IMAGE
    print(f"The pic is: {picture_path}")
    image = picture_path[0]
    name = picture_path[1]
    pic_ver = picture_path[2]
    path = f"{image}"
    if what_picture_page:  # it's the picture self page
        if pic_ver >= 2:
            if image:
                image_PIL = Image.open(path)
                EDIT_IMAGE_PATH = path
                image = image_PIL.resize((200, 200), Image.LANCZOS)
                image = ImageTk.PhotoImage(image)
            if PANEL is None:
                button_image = tk.Button(frame, image=image, relief=FLAT, bd=4, bg="black",
                                         command=lambda: marked_image(image, button_image, frame, path, name, pic_ver,
                                                                      image_PIL))
                PANEL = button_image
                PANEL.place(x=120 + (240 * COUNT_PICTURE_VAR2), y=200, anchor=tk.CENTER)
                tk.Label(frame, text=f"{name}", bg="black", fg="white",
                         font=("Arial", 12, "bold"), padx=20, pady=20, bd=3,
                         relief=tk.RAISED). \
                    place(x=120 + (245 * COUNT_PICTURE_VAR2), y=330, anchor=tk.CENTER, width=240, height=40)
                COUNT_PICTURE_VAR2 += 1
            else:
                PANEL.configure(image=image)
                PANEL.image = image
            PANEL = None
    elif not what_picture_page:  # it's the picture page
        if pic_ver == 1:
            if image:
                image_PIL = Image.open(path)
                EDIT_IMAGE_PATH = path
                image = image_PIL.resize((200, 200), Image.LANCZOS)
                image = ImageTk.PhotoImage(image)
            if PANEL is None:
                button_image = tk.Button(frame, image=image, relief=FLAT, bd=4, bg="black",
                                         command=lambda: marked_image(image, button_image, frame, path, name, pic_ver,
                                                                      image_PIL))
                PANEL = button_image
                PANEL.place(x=120 + (240 * COUNT_PICTURE), y=200, anchor=tk.CENTER)
                tk.Label(frame, text=f"Name: {name}", bg="black", fg="white",
                         font=("Arial", 12, "bold"), padx=20, pady=20, bd=3,
                         relief=tk.RAISED). \
                    place(x=120 + (240 * COUNT_PICTURE), y=330, anchor=tk.CENTER, height=30, width=200)
                COUNT_PICTURE += 1
            else:
                PANEL.configure(image=image)
                PANEL.image = image
            PANEL = None


def uploads_pictures_to_server(number_picture, frame, page):
    """

    :param number_picture:
    :param frame:
    :param page:
    :return:
    """
    global STORAGE_PATH_PICTURE, UPLOAD_PICTURE_BUTTON_PICTURE_PAGE, SELECT_IMAGE_BUTTON, \
        UPLOAD_EDIT_BUTTON, NO_PICTURE_SELECTED, NUMBER_PAGE
    try:
        if NUMBER_PICTURE == 0:
            NUMBER_PAGE = 3
        else:
            NUMBER_PAGE = 2
        if number_picture == 0:
            NO_PICTURE_SELECTED.place(x=600, y=665, anchor=tk.CENTER, width=250, height=20)
            return
        else:
            msg_pic_to_server = PICTURES_TO_SERVER_PROTOCOL, str(number_picture)
            not_thing = b'aaaa'
            conn.sendall(pickle.dumps(msg_pic_to_server))
            print(f"storage paths: {STORAGE_PATH_PICTURE} ")
            num_pic = 0
            pic = ''
            while True:
                while True:
                    if num_pic != len(STORAGE_PATH_PICTURE):
                        pic = STORAGE_PATH_PICTURE[num_pic]
                    msg_from_server = pickle.loads(conn.recv(MSG_LEN))
                    if msg_from_server == 'ok':
                        with open(pic[0], 'rb') as f:
                            image_data = f.read()
                        conn.sendall(image_data)
                        conn.sendall(not_thing)
                    if msg_from_server == 'got it':
                        conn.sendall(pickle.dumps(pic[1]))
                        conn.sendall((pickle.dumps(pic[2])))
                        num_pic += 1
                    elif msg_from_server == 'Finish':
                        STORAGE_PATH_PICTURE = []
                        if page == "picture_Page":
                            UPLOAD_PICTURE_BUTTON_PICTURE_PAGE.config(state='disabled')
                            SELECT_IMAGE_BUTTON.config(state='disabled')
                            NO_PICTURE_SELECTED.destroy()
                            tk.Label(frame, text="You have successfully uploaded the picture to the server", bg="black",
                                     fg="white",
                                     font=("Arial", 12, "bold"), padx=20,
                                     pady=20, bd=3, relief=tk.RAISED). \
                                place(x=600, y=665, anchor=tk.CENTER, width=450, height=20)
                        elif page == "Edit_Page":
                            UPLOAD_EDIT_BUTTON.config(state='disabled')
                            tk.Label(frame, text="You have successfully uploaded the picture to the server", bg="black",
                                     fg="white",
                                     font=("Arial", 12, "bold"), padx=20,
                                     pady=20, bd=3, relief=tk.RAISED). \
                                place(x=450, y=635, anchor='w', width=450, height=30)
                        return
    except ssl.SSLError as err:
        print(f"Something went wrong with the server: {err}")
        conn.close()
        root.quit()


def get_pictures_from_server():
    """

    :return:
    """
    try:
        msg_pic_to_client = PICTURES_TO_CLIENT_PROTOCOL
        conn.sendall(pickle.dumps(msg_pic_to_client))
        number_picture = conn.recv(MSG_LEN)
        number_picture = int(pickle.loads(number_picture))
        while number_picture > 0:
            image_data = b''
            conn.sendall(pickle.dumps('ok'))
            while True:
                data = conn.recv(4096)
                if data[-4:][:4] == b'aaaa':
                    conn.sendall(pickle.dumps("got it"))
                    picture_name = pickle.loads(conn.recv(MSG_LEN))
                    picture_version = pickle.loads(conn.recv(MSG_LEN))
                    image_data += data[:-4]
                    break
                else:
                    image_data += data

            # Convert the image data into an image object
            picture_name = picture_name.split('.')
            picture_name = picture_name[0]
            image = Image.open(io.BytesIO(image_data))

            image_path = f"{PHOTOS_SAVED_FILE}/{picture_name}.JPG"
            image.save(image_path, format='PNG')
            STORAGE_PICTURE.append((image_path, picture_name, picture_version))
            if picture_version == 1:
                STORAGE_PICTURE_VER1.append((image_path, picture_name, picture_version))
            else:
                STORAGE_PICTURE_VER2.append((image_path, picture_name, picture_version))
            number_picture -= 1
        return
    except ssl.SSLError as err:
        print(f"Some went wrong with the server: {err}")
        conn.close()
        root.quit()


def download_picture(picture_name):
    """

    :param picture_name:
    :return:
    """
    global SELECTED_IMAGE_TO_EDIT, NAME_FIRST_LABEL
    if picture_name == '':
        NAME_FIRST_LABEL.place(x=1075, y=650, anchor=tk.CENTER, width=250, height=50)
        return
    picture_name = picture_name.replace(' ', '_')
    folder_path = filedialog.askdirectory()
    # Check if a folder was selected
    if folder_path:
        NAME_FIRST_LABEL.place_forget()
        # Open your picture variable
        picture_image = Image.open(SELECTED_IMAGE_TO_EDIT)

        picture_image.save(f"{folder_path}/{picture_name}.jpg")


def client_back_to_start():
    """

    :return:
    """
    try:
        msg = CLIENT_BACK_TO_START_PROTOCOL
        conn.sendall(pickle.dumps(msg))
    except ssl.SSLError as err:
        print(f"Something went wrong with the server: {err}")
        conn.close()
        root.quit()


def switch_pictures_page(frame, pic_name, num):
    """

    :param frame:
    :param pic_name:
    :param num:
    :return:
    """
    global NO_PICTURE_WAS_SELECTED_BUTTON
    if NO_PICTURE_WAS_SELECTED_BUTTON == '':
        NO_PICTURE_WAS_SELECTED_BUTTON = tk.Label(frame, text="No picture was selected", bg="black", fg="white",
                                                  font=("Arial", 12, "bold"), padx=20,
                                                  pady=20, bd=3, relief=tk.RAISED)
    if num == 1:
        if pic_name == '':
            NO_PICTURE_WAS_SELECTED_BUTTON.place(x=1050, y=665, anchor=tk.CENTER, width=300, height=20)
        else:
            frame.master.switch_frame(frame.master.pictures_frame[pic_name], 3)
    elif num == 2:
        if pic_name == '':
            NO_PICTURE_WAS_SELECTED_BUTTON.place(x=1050, y=665, anchor=tk.CENTER, width=300, height=20)
        else:
            frame.master.switch_frame(EditPicturesPage, 1)


def check_picture_name(path_name, name, frame):
    """

    :param path_name:
    :param name:
    :param frame:
    :return:
    """
    global DOWN_LOAD_PICTURE_BUTTON, UPLOAD_EDIT_BUTTON, IMAGE_AFTER_EDIT
    if path_name == '':
        no_path = tk.Label(frame, text="Please enter path name to download", bg="black", fg="white",
                           font=("Arial", 12, "bold"), padx=20,
                           pady=20, bd=3, relief=tk.RAISED)
        no_path.place(x=1050, y=630, anchor=tk.CENTER, width=300, height=20)
        DOWN_LOAD_PICTURE_BUTTON.config(stat='disabled')
    else:
        DOWN_LOAD_PICTURE_BUTTON.config(stat='active')
    if name != '' and len(UNDO_STACK) != 0:
        path_edit = SELECTED_IMAGE_TO_EDIT.split('.JPG')[0]
        IMAGE_AFTER_EDIT.save(f"{path_edit}_{name.replace(' ', '_')}.JPG")
        UPLOAD_EDIT_BUTTON.config(stat='active')
    else:
        no_name = tk.Label(frame, text="Please enter picture name to upload", bg="black", fg="white",
                           font=("Arial", 12, "bold"), padx=20,
                           pady=20, bd=3, relief=tk.RAISED)
        no_name.place(x=1050, y=650, anchor=tk.CENTER, width=300, height=20)
        UPLOAD_EDIT_BUTTON.config(stat='disabled')


# Define the image editing functions
def grayscale():
    """

    :return:
    """
    global IMG, UNDO_STACK
    UNDO_STACK.append(IMG)
    IMG = IMG.convert('L')
    update_image()


def blur(radius):
    """

    :param radius:
    :return:
    """
    global IMG, UNDO_STACK
    if radius == '':
        return
    UNDO_STACK.append(IMG)
    IMG = IMG.filter(ImageFilter.GaussianBlur(radius=radius))
    update_image()


def rotate(angle):
    """

    :param angle:
    :return:
    """
    global IMG, UNDO_STACK
    if angle == '':
        return
    angle = float(angle)
    if type(angle) == float:
        angle = int(angle)
    UNDO_STACK.append(IMG)
    IMG = IMG.rotate(angle)
    update_image()


def detail():
    """

    :return:
    """
    global IMG, UNDO_STACK
    UNDO_STACK.append(IMG)
    IMG = IMG.filter(ImageFilter.DETAIL)
    update_image()


def mirror():
    """

    :return:
    """
    global IMG, UNDO_STACK
    UNDO_STACK.append(IMG)
    IMG = ImageOps.mirror(IMG)
    update_image()


def flip():
    """

    :return:
    """
    global IMG, UNDO_STACK
    UNDO_STACK.append(IMG)
    IMG = ImageOps.flip(IMG)
    update_image()


def brightness(level):
    """

    :param level:
    :return:
    """
    global IMG, UNDO_STACK
    if level == '':
        return
    UNDO_STACK.append(IMG)
    enhancer = ImageEnhance.Brightness(IMG)
    IMG = enhancer.enhance(float(level))
    update_image()


def contrast(level):
    """

    :param level:
    :return:
    """
    global IMG, UNDO_STACK
    if level == '':
        return
    UNDO_STACK.append(IMG)
    enhancer = ImageEnhance.Contrast(IMG)
    IMG = enhancer.enhance(float(level))
    update_image()


def black_white():
    """

    :return:
    """
    global IMG, UNDO_STACK
    UNDO_STACK.append(IMG)
    IMG = IMG.convert('1')
    update_image()


def invert_effect():
    """

    :return:
    """
    global IMG, UNDO_STACK
    UNDO_STACK.append(IMG)
    IMG = ImageOps.invert(IMG)
    update_image()


# Define the function to undo the last image editing function
def undo():
    """

    :return:
    """
    global IMG, UNDO_STACK
    if len(UNDO_STACK) > 0:
        IMG = UNDO_STACK.pop()
        update_image()


# Define the function to update the image in the GUI
def update_image():
    """

    :return:
    """
    global IMG_TK, IMG, NO_EDIT_LABEL, IMAGE_AFTER_EDIT
    IMG_TK = ImageTk.PhotoImage(IMG)
    PANEL_EDITED_IMAGE.config(image=IMG_TK)
    IMAGE_INFO_LABEL.config(text="Image format: {}\nImage mode: {}\nFile name: {}".format(IMG.format, IMG.mode, format(
        os.path.basename(EDIT_IMAGE_PATH))))
    IMAGE_AFTER_EDIT = IMG
    if len(UNDO_STACK) == 0:
        NO_EDIT_LABEL.place(x=825, y=550, anchor=tk.CENTER, width=250, height=25)
        UPLOAD_EDIT_BUTTON.config(state='disabled')
    else:
        NO_EDIT_LABEL.place_forget()


class MainWindow(tk.Tk):
    """

    """

    def __init__(self):
        super().__init__()
        self._frame = None
        self.picture_page_frames = []
        self.pictures_frame = {}

        self.switch_frame(StartPage, 1)

    def create_picture_page_frames(self):
        """

        :return:
        """
        self.picture_page_frames = []
        number_of_frames = 1
        global PANEL, STORAGE_PICTURE, COUNT_PICTURE, \
            BUTTON_IMAGE, EDIT_IMAGE, IF_IMAGE_PRESSED, STORAGE_PICTURE_VER2, STORAGE_PICTURE_VER1
        STORAGE_PICTURE = []
        STORAGE_PICTURE_VER1 = []
        STORAGE_PICTURE_VER2 = []
        get_pictures_from_server()
        self.create_pictures_page()

        print(f"The storage pictures is: {STORAGE_PICTURE}")
        number_of_1_pic = 0
        for pic in STORAGE_PICTURE:
            if pic[2] == 1:
                number_of_1_pic += 1

        number_of_frames = number_of_frames + int((number_of_1_pic - 1) / 5)

        for i in range(number_of_frames):  # creating 3 instances of picturesPage1
            frame = PicturesPage(self)
            self.picture_page_frames.append(frame)

        # adding navigation buttons to each picturesPage1 frame
        for i in range(number_of_frames):
            COUNT_PICTURE = 0
            tk.Label(self.picture_page_frames[i], text=f"Picture Page - {i + 1}", bg=BACKGROUND_COLOR, fg="white",
                     font=LARGE_FONT). \
                place(x=600, y=20, anchor=tk.CENTER, width=1200, height=80)
            prev_btn = tk.Button(self.picture_page_frames[i], text="Prev page", bg=COLOR, fg="white",
                                 font=("Arial", 12, "bold"), padx=20, pady=20, bd=3,
                                 relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                                 command=lambda idx=i: (
                                     self.switch_frame(self.picture_page_frames[idx - 1], 3), reset_marked_image()))
            start_btn = tk.Button(self.picture_page_frames[i], text="Pictures Page - 1", bg=COLOR, fg="white",
                                  font=("Arial", 12, "bold"), padx=20, pady=20, bd=3,
                                  relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                                  command=lambda: (
                                      self.switch_frame(self.picture_page_frames[0], 3), reset_marked_image()))
            next_btn = tk.Button(self.picture_page_frames[i], text="Next page", bg=COLOR, fg="white",
                                 font=("Arial", 12, "bold"), padx=20, pady=20, bd=3,
                                 relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                                 command=lambda idx=i: (
                                     self.switch_frame(
                                         self.picture_page_frames[(idx + 1) % len(self.picture_page_frames)], 3),
                                     reset_marked_image()))

            prev_btn.place(x=100, y=662.5, anchor=tk.CENTER, width=160, height=25)
            start_btn.place(x=260, y=662.5, anchor=tk.CENTER, width=160, height=25)
            next_btn.place(x=420, y=662.5, anchor=tk.CENTER, width=160, height=25)
            if len(STORAGE_PICTURE_VER1) != 0:
                number_of_1_pic = 0
                for number_in_pictures in range(1, (len(STORAGE_PICTURE_VER1) + 1) - i * 5):
                    if STORAGE_PICTURE_VER1[i * 5 + (number_in_pictures - 1)][2] == 1:
                        print_pictures(STORAGE_PICTURE_VER1[i * 5 + (number_in_pictures - 1)],
                                       self.picture_page_frames[i], False)
                        BUTTON_IMAGE = None
                        IF_IMAGE_PRESSED = False
                        EDIT_IMAGE = ''
                        PANEL = None
                        number_of_1_pic += 1
                        if number_of_1_pic % 5 == 0:
                            break
            else:
                tk.Label(self.picture_page_frames[i], text="There are no pictures in the storage", bg="black",
                         fg="white", font=("Arial", 18, "bold"), padx=20,
                         pady=20,
                         bd=3, relief=tk.RAISED). \
                    place(x=600, y=350, anchor=tk.CENTER, width=450, height=60)

            if i == len(self.picture_page_frames) - 1:
                next_btn.config(state='disabled')

            if i == 0:
                prev_btn.config(state='disabled')
                start_btn.config(state='disabled')

    def create_pictures_page(self):
        """

        :return:
        """
        for pic in STORAGE_PICTURE:
            frame = PictureSelfPage(self, pic[1])
            self.pictures_frame[pic[1]] = frame

    def switch_frame(self, frame_class, number):
        """

        :param frame_class:
        :param number:
        :return:
        """
        if number == 1:
            new_frame = frame_class(self)
        else:
            if number == 2:
                self.picture_page_frames = []
                self.create_picture_page_frames()
                frame_class = self.picture_page_frames[0]
            new_frame = frame_class
        if number == CLIENT_BACK_TO_START_PROTOCOL:
            client_back_to_start()
            new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.pack_forget()
        self._frame = new_frame
        self._frame.pack(fill="both", expand=True)


class StartPage(tk.Frame):
    """

    """

    def __init__(self, master):
        super().__init__(master)
        self.configure(bg=BACKGROUND_COLOR)
        tk.Label(self, text="Start Page - Managing and Editing Pictures", font=LARGE_FONT, fg="White", padx=20, pady=20,
                 bd=3, bg=BACKGROUND_COLOR). \
            place(x=600, y=50, anchor=tk.CENTER, width=1200, height=150)
        tk.Button(self, text="Sign - Up", bg=COLOR, fg="white", font=("Arial", 12, "bold"), padx=20,
                  pady=20, bd=3,
                  relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                  command=lambda: master.switch_frame(SignUpPage, 1)). \
            place(x=200, y=700, anchor=tk.CENTER, width=400, height=50)
        tk.Button(self, text="Log - In", bg=COLOR, fg="white", font=("Arial", 12, "bold"), padx=20,
                  pady=20, bd=3, relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                  command=lambda: master.switch_frame(LogInPage, 1)). \
            place(x=600, y=700, anchor=tk.CENTER, width=400, height=50)
        tk.Button(self, text='GoodBye - Exit', bg=COLOR, fg="white", font=("Arial", 12, "bold"), padx=20, pady=20,
                  bd=3, relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                  command=lambda: exit_window()). \
            place(x=1000, y=700, anchor=tk.CENTER, width=400, height=50)


class SignUpPage(tk.Frame):
    """

    """

    def __init__(self, master):
        super().__init__(master)
        global SIGN_UP_BUTTON
        self.configure(bg=BACKGROUND_COLOR)
        tk.Label(self, text="Sign - Up Page", font=LARGE_FONT, fg="White", padx=20, pady=20, bd=3,
                 bg=BACKGROUND_COLOR). \
            place(x=600, y=100, anchor=tk.CENTER, width=1200, height=150)
        tk.Label(self, text=f"Please enter User Name: ", bg="black", fg="white", font=("Arial", 12, "bold"), padx=20,
                 pady=20,
                 bd=3, relief=tk.RAISED). \
            place(x=100, y=300, anchor=tk.CENTER, width=200, height=40)
        entry_user_name = ttk.Entry(self, font=("Arial", 12, "bold"))
        entry_user_name. \
            place(x=300, y=300, anchor=tk.CENTER, width=200, height=30)
        tk.Label(self, text=f"Please enter Password: ", bg="black", fg="white", font=("Arial", 12, "bold"), padx=20,
                 pady=20,
                 bd=3, relief=tk.RAISED). \
            place(x=100, y=400, anchor=tk.CENTER, width=200, height=40)
        entry_password = ttk.Entry(self, font=("Arial", 12, "bold"), show='*')
        entry_password. \
            place(x=300, y=400, anchor=tk.CENTER, width=200, height=30)
        SIGN_UP_BUTTON = tk.Button(self, text="Sign Up", bg=COLOR, fg="white", font=("Arial", 12, "bold"), padx=20,
                                   pady=20, bd=3,
                                   relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                                   command=lambda: signup_function(entry_user_name, entry_password, self))
        SIGN_UP_BUTTON.place(x=600, y=700, anchor=tk.CENTER, width=400, height=50)
        tk.Button(self, text="Start Page", bg=COLOR, fg="white", font=("Arial", 12, "bold"), padx=20, pady=20,
                  bd=3, relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                  command=lambda: master.switch_frame(StartPage, CLIENT_BACK_TO_START_PROTOCOL)). \
            place(x=200, y=700, anchor=tk.CENTER, width=400, height=50)


class LogInPage(tk.Frame):
    """

    """

    def __init__(self, master):
        super().__init__(master)
        self.configure(bg=BACKGROUND_COLOR)
        tk.Label(self, text="Log - In Page", font=LARGE_FONT, fg="White", padx=20, pady=20, bd=3,
                 bg=BACKGROUND_COLOR). \
            place(x=600, y=100, anchor=tk.CENTER, width=1200, height=150)
        tk.Label(self, text=f"Please enter User Name:", bg="black", fg="white", font=("Arial", 12, "bold"), padx=20,
                 pady=20, bd=3, relief=tk.RAISED). \
            place(x=100, y=300, anchor=tk.CENTER, width=200, height=40)
        entry_user_name = ttk.Entry(self, font=("Arial", 14, "bold"))
        entry_user_name. \
            place(x=300, y=300, anchor=tk.CENTER, width=200, height=30)
        tk.Label(self, text=f"Please enter Password:", bg="black", fg="white", font=("Arial", 12, "bold"), padx=20,
                 pady=20, bd=3, relief=tk.RAISED). \
            place(x=100, y=400, anchor=tk.CENTER, width=200, height=40)
        entry_password = ttk.Entry(self, font=("Arial", 14, "bold"), show="*")
        entry_password. \
            place(x=300, y=400, anchor=tk.CENTER, width=200, height=30)
        tk.Button(self, text="Log - In", bg=COLOR, fg="white", font=("Arial", 12, "bold"), padx=20,
                  pady=20, bd=3, relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                  command=lambda: login_function(entry_user_name, entry_password, self)). \
            place(x=600, y=700, anchor=tk.CENTER, width=400, height=50)
        tk.Button(self, text="Start Page", bg=COLOR, fg="white", font=("Arial", 12, "bold"), padx=20, pady=20,
                  bd=3, relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                  command=lambda: master.switch_frame(StartPage, CLIENT_BACK_TO_START_PROTOCOL)). \
            place(x=200, y=700, anchor=tk.CENTER, width=400, height=50)


class PicturesPage(tk.Frame):
    """

    """

    def __init__(self, master):
        super().__init__(master)
        global PANEL, COUNT_PICTURE, \
            BUTTON_IMAGE, EDIT_IMAGE, IF_IMAGE_PRESSED
        self.configure(bg=BACKGROUND_COLOR)
        tk.Label(self, text=f"Hello, {USER_NAME}", bg="black", fg="white", font=("Arial", 12, "bold"), padx=20,
                 pady=20,
                 bd=3, relief=tk.RAISED). \
            place(x=600, y=75, anchor=tk.CENTER, width=200, height=20)
        tk.Button(self, text="Exit - Start Page", bg=COLOR, fg="white", font=("Arial", 12, "bold"), padx=20, pady=20,
                  bd=3, relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                  command=lambda: master.switch_frame(StartPage, CLIENT_BACK_TO_START_PROTOCOL)). \
            place(x=150, y=700, anchor=tk.CENTER, width=300, height=50)
        tk.Button(self, text="Upload pictures", bg=COLOR, fg="white", font=("Arial", 12, "bold"), padx=20, pady=20,
                  bd=3, relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                  command=lambda: master.switch_frame(UploadPicturesPage, 1)). \
            place(x=450, y=700, anchor=tk.CENTER, width=300, height=50)
        tk.Button(self, text="Edit pictures", bg=COLOR, fg="white", font=("Arial", 12, "bold"), padx=20, pady=20,
                  bd=3, relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                  command=lambda: switch_pictures_page(self, picture, 2)). \
            place(x=750, y=700, anchor=tk.CENTER, width=300, height=50)
        refresh_button = tk.Button(self, text="Refresh pictures", bg=COLOR, fg="white", font=("Arial", 12, "bold"),
                                   padx=20, activebackground=BACKGROUND_BUTTON_COLOR, pady=20, bd=3,
                                   relief=tk.RAISED,
                                   command=lambda: master.switch_frame(master.picture_page_frames[0], 2))
        refresh_button.place(x=260, y=637.5, anchor=tk.CENTER, width=320, height=25)
        tk.Button(self, text="The picture's page", bg=COLOR, fg="white", font=("Arial", 12, "bold"), padx=20,
                  pady=20, bd=3, relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                  command=lambda: switch_pictures_page(self, picture, 1)). \
            place(x=1050, y=700, anchor=tk.CENTER, width=300, height=50)


class PictureSelfPage(tk.Frame):
    """

    """

    def __init__(self, master, pic_name):
        super().__init__(master)
        global picture, EDIT_IMAGE, RESET_BUTTON, STORAGE_PICTURE, BUTTON_IMAGE, \
            IF_IMAGE_PRESSED, EDIT_IMAGE, PANEL, COUNT_PICTURE, COUNT_PICTURE_VAR2
        self.configure(bg=BACKGROUND_COLOR)
        tk.Label(self, text=f"picture - {pic_name} - Page", bg=BACKGROUND_COLOR, fg="white", font=LARGE_FONT, padx=20,
                 pady=20,
                 bd=3, relief=tk.RAISED). \
            place(x=600, y=20, anchor=tk.CENTER, width=1200, height=80)
        tk.Button(self, text="Go to Start Page", bg=COLOR, fg="white", font=("Arial", 12, "bold"), padx=20, pady=20,
                  bd=3, relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                  command=lambda: master.switch_frame(StartPage, CLIENT_BACK_TO_START_PROTOCOL)). \
            place(x=150, y=700, anchor=tk.CENTER, width=300, height=50)
        tk.Button(self, text="Back to pictures Page", bg=COLOR, fg="white", font=("Arial", 12, "bold"), padx=20,
                  pady=20, bd=3, relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                  command=lambda: (master.switch_frame(master.picture_page_frames[0], 3), reset_marked_image())). \
            place(x=450, y=700, anchor=tk.CENTER, width=300, height=50)
        picture_name = ttk.Entry(self, font=("Arial", 12, "bold"))
        picture_name.place(x=500, y=600, anchor=tk.CENTER, width=400, height=30)
        down_load_picture = tk.Button(self, text="Download the picture", bg=COLOR, fg="white",
                                      font=("Arial", 12, "bold"), padx=20, pady=20, bd=3, relief=tk.RAISED,
                                      activebackground=BACKGROUND_BUTTON_COLOR,
                                      command=lambda: download_picture(picture_name.get()))
        down_load_picture.place(x=750, y=700, anchor=tk.CENTER, width=300, height=50)
        RESET_BUTTON = tk.Button(self, text="Resets marked picture", bg=COLOR, fg="white", font=("Arial", 12, "bold"),
                                 padx=20, pady=20, bd=3, relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                                 command=lambda: reset_marked_image())
        RESET_BUTTON.place(x=1050, y=700, anchor=tk.CENTER, width=300, height=50)
        tk.Label(self, text="Enter the name of the path you want", bg="black", fg="white", font=("Arial", 12, "bold"),
                 padx=20, pady=20, bd=3, relief=tk.RAISED). \
            place(x=150, y=600, anchor=tk.CENTER, width=300, height=30)
        COUNT_PICTURE = 0
        COUNT_PICTURE_VAR2 = 0
        number_of_pic_var2 = 0
        no_picture_ver2 = tk.Label(self, text="There are no other pictures under that picture", bg="black",
                                   fg="white", font=("Arial", 12, "bold"),
                                   padx=20, pady=20, bd=3, relief=tk.RAISED)
        for pic in STORAGE_PICTURE_VER2:
            name = pic[1].split('-')
            if name[0] == pic_name:
                number_of_pic_var2 += 1
        if number_of_pic_var2 != 0:
            no_picture_ver2.place_forget()
            for pic in STORAGE_PICTURE_VER2:
                name = pic[1].split('-')
                if name[0] == pic_name:
                    print_pictures(pic, self, True)
                    BUTTON_IMAGE = ''
                    IF_IMAGE_PRESSED = False
                    EDIT_IMAGE = ''
                    PANEL = None
        else:
            no_picture_ver2.place(x=600, y=100, anchor=tk.CENTER, width=400, height=60)


class EditPicturesPage(tk.Frame):
    """

    """

    def __init__(self, master):
        super().__init__(master)
        global EDIT_IMAGE, PANEL, EDIT_IMAGE_PATH, UPLOAD_EDIT_BUTTON, picture, NUMBER_PAGE, IMAGE_INFO_LABEL, \
            DOWN_LOAD_PICTURE_BUTTON, VERSION, IMAGE_PIL, IMG, IMAGE_AFTER_EDIT, PANEL_EDITED_IMAGE, NO_EDIT_LABEL, NAME_FIRST_LABEL
        self.configure(bg=BACKGROUND_COLOR)
        if NUMBER_PICTURE == 0:
            NUMBER_PAGE = 3
        else:
            NUMBER_PAGE = 2
        tk.Label(self, text="Edit pictures Page", font=LARGE_FONT, bg=BACKGROUND_COLOR, fg="white", padx=20,
                 pady=20, bd=3). \
            place(x=600, y=20, anchor=tk.CENTER, width=1200, height=80)
        IMG = IMAGE_PIL.resize((200, 200), Image.LANCZOS)
        picture_path_name = tk.Entry(self, font="Verdana")
        picture_name = tk.Entry(self, font="Verdana")
        tk.Label(self, text=f"The picture's name is: {picture}", bg=BACKGROUND_COLOR, fg="white",
                 font=("Arial", 12, "bold", "underline"), padx=20, pady=20, bd=3). \
            place(x=600, y=90, anchor=tk.CENTER, width=1200, height=40)
        UPLOAD_EDIT_BUTTON = tk.Button(self, text="Upload the picture", bg=COLOR, fg="white",
                                       font=("Arial", 12, "bold"), padx=20, pady=20, bd=3,
                                       activebackground=BACKGROUND_BUTTON_COLOR, state='disabled',
                                       command=lambda: (STORAGE_PATH_PICTURE.append((
                                           f"{SELECTED_IMAGE_TO_EDIT.split('.JPG')[0]}_{picture_name.get().replace(' ', '_')}.JPG",
                                           f"{picture}-{picture_name.get().replace(' ', '_')}",
                                           int(VERSION) + 1)),
                                                        print(f"path storage: {STORAGE_PATH_PICTURE}"),
                                                        uploads_pictures_to_server(1, self, "Edit_Page"),
                                                        NAME_FIRST_LABEL.place_forget()))
        DOWN_LOAD_PICTURE_BUTTON = tk.Button(self, text="Download the picture", bg=COLOR, fg="white",
                                             font=("Arial", 12, "bold"), padx=20, pady=20, bd=3, relief=tk.RAISED,
                                             activebackground=BACKGROUND_BUTTON_COLOR,
                                             command=lambda: download_picture(picture_path_name.get()))
        Are_You_Sure_button_edit_page = tk.Button(self, text="Are you done with the picture?",
                                                  bg=COLOR, fg="white", font=("Arial", 12, "bold"), padx=20, pady=20,
                                                  bd=3, relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                                                  command=lambda: (check_picture_name(picture_path_name.get(),
                                                                                      picture_name.get(), self)))
        Are_You_Sure_button_edit_page.place(x=1050, y=700, anchor=tk.CENTER, width=300, height=50)
        DOWN_LOAD_PICTURE_BUTTON.place(x=750, y=700, anchor=tk.CENTER, width=300, height=50)
        UPLOAD_EDIT_BUTTON.place(x=450, y=700, anchor=tk.CENTER, width=300, height=50)
        tk.Label(self, text="Enter the name of the path you want for downloading:", bg="black", fg="white",
                 font=("Arial", 12, "bold"), padx=20,
                 pady=20, bd=3, relief=tk.RAISED). \
            place(x=225, y=590, anchor=tk.CENTER, width=450, height=30)
        picture_path_name.place(x=600, y=590, anchor=tk.CENTER, width=300, height=30)
        tk.Label(self, text="Enter the name of the picture you want for uploading:", bg="black", fg="white",
                 font=("Arial", 12, "bold"), padx=20,
                 pady=20, bd=3, relief=tk.RAISED). \
            place(x=225, y=635, anchor=tk.CENTER, width=450, height=30)
        picture_name.place(x=600, y=635, anchor=tk.CENTER, width=300, height=30)
        tk.Button(self, text="Back to pictures Page", bg=COLOR, fg="white", font=("Arial", 12, "bold"), padx=20,
                  pady=20, bd=3, relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                  command=lambda: (
                      master.switch_frame(master.picture_page_frames[0], NUMBER_PAGE), reset_marked_image())). \
            place(x=150, y=700, anchor=tk.CENTER, width=300, height=50)
        NAME_FIRST_LABEL = tk.Label(self, text='You need to enter name first', bg="black", fg="white",
                                    font=("Arial", 12, "bold"), padx=20, pady=20, bd=3, relief=tk.RAISED)
        if PANEL is None:
            PANEL = tk.Label(self, image=EDIT_IMAGE, relief=FLAT)
            PANEL_EDITED_IMAGE = PANEL
            PANEL.image = EDIT_IMAGE
            PANEL.place(x=200, y=300, anchor=tk.CENTER)
        else:
            PANEL.configure(image=EDIT_IMAGE)
            PANEL.image = EDIT_IMAGE
        PANEL = None
        grayscale_button = tk.Button(self, text="Grayscale", bg=COLOR, fg="white", font=("Arial", 12, "bold"), padx=20,
                                     pady=20, bd=3, relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                                     command=grayscale)
        grayscale_button.place(x=575, y=450, anchor=tk.CENTER, width=200, height=25)

        blur_label = tk.Label(self, text="Blur radius:")
        blur_label.place(x=1075, y=200, anchor=tk.CENTER, width=200, height=25)
        blur_spinbox = Spinbox(self, from_=0, to=10, increment=0.1, format="%.2f", width=8)
        blur_spinbox.place(x=1075, y=250, anchor=tk.CENTER, width=200, height=25)
        blur_button = tk.Button(self, text="Blur", bg=COLOR, fg="white", font=("Arial", 12, "bold"), padx=20, pady=20,
                                bd=3, relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                                command=lambda: blur(float(blur_spinbox.get())))
        blur_button.place(x=1075, y=300, anchor=tk.CENTER, width=200, height=25)

        rotate_label = tk.Label(self, text="Rotation angle:")
        rotate_label.place(x=1075, y=350, anchor=tk.CENTER, width=200, height=25)
        rotate_entry = tk.Entry(self)
        rotate_entry.place(x=1075, y=400, anchor=tk.CENTER, width=200, height=25)
        rotate_button = tk.Button(self, text="Rotate", bg=COLOR, fg="white", font=("Arial", 12, "bold"), padx=20,
                                  pady=20, bd=3, relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                                  command=lambda: rotate((rotate_entry.get())))
        rotate_button.place(x=1075, y=450, anchor=tk.CENTER, width=200, height=25)

        brightness_label = tk.Label(self, text="Brightness level:")
        brightness_label.place(x=825, y=200, anchor=tk.CENTER, width=200, height=25)
        brightness_spinbox = Spinbox(self, from_=0, to=10, increment=0.1, format="%.2f", width=8)
        brightness_spinbox.place(x=825, y=250, anchor=tk.CENTER, width=200, height=25)
        brightness_button = tk.Button(self, text="Brightness", bg=COLOR, fg="white", font=("Arial", 12, "bold"),
                                      padx=20, pady=20, bd=3, relief=tk.RAISED,
                                      activebackground=BACKGROUND_BUTTON_COLOR,
                                      command=lambda: brightness(brightness_spinbox.get()))
        brightness_button.place(x=825, y=300, anchor=tk.CENTER, width=200, height=25)

        contrast_label = tk.Label(self, text="Contrast level:")
        contrast_label.place(x=825, y=350, anchor=tk.CENTER, width=200, height=25)
        contrast_spinbox = Spinbox(self, from_=0, to=10, increment=0.1, format="%.2f", width=8)
        contrast_spinbox.place(x=825, y=400, anchor=tk.CENTER, width=200, height=25)
        contrast_button = tk.Button(self, text="Contrast", bg=COLOR, fg="white", font=("Arial", 12, "bold"), padx=20,
                                    pady=20, bd=3, relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                                    command=lambda: contrast(contrast_spinbox.get()))
        contrast_button.place(x=825, y=450, anchor=tk.CENTER, width=200, height=25)

        bw_button = tk.Button(self, text="Black and white", bg=COLOR, fg="white", font=("Arial", 12, "bold"), padx=20,
                              pady=20, bd=3, relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                              command=lambda: black_white())
        bw_button.place(x=575, y=200, anchor=tk.CENTER, width=200, height=25)

        invert_button = tk.Button(self, text="Apply Invert Effect", bg=COLOR, fg="white", font=("Arial", 12, "bold"),
                                  padx=20,
                                  pady=20, bd=3, relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                                  command=lambda: invert_effect())
        invert_button.place(x=575, y=250, anchor=tk.CENTER, width=200, height=25)

        mirror_button = tk.Button(self, text="Mirror", bg=COLOR, fg="white", font=("Arial", 12, "bold"), padx=20,
                                  pady=20, bd=3, relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                                  command=lambda: mirror())
        mirror_button.place(x=575, y=300, anchor=tk.CENTER, width=200, height=25)
        flip_button = tk.Button(self, text="Flip", bg=COLOR, fg="white", font=("Arial", 12, "bold"), padx=20,
                                pady=20, bd=3, relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                                command=lambda: flip())
        flip_button.place(x=575, y=350, anchor=tk.CENTER, width=200, height=25)
        detail_button = tk.Button(self, text="Detail", bg=COLOR, fg="white", font=("Arial", 12, "bold"), padx=20,
                                  pady=20, bd=3, relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                                  command=lambda: detail())
        detail_button.place(x=575, y=400, anchor=tk.CENTER, width=200, height=25)

        # Create the button to undo the last image editing function
        undo_button = tk.Button(self, text="Undo", bg=COLOR, fg="white", font=("Arial", 12, "bold"), padx=20, pady=20,
                                bd=3, relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR, command=undo)
        undo_button.place(x=825, y=500, anchor=tk.CENTER, width=200, height=25)

        IMAGE_INFO_LABEL = tk.Label(self,
                                    text="Image format: {}\nImage mode: {}\nFile name: {}".format(IMG.format, IMG.mode,
                                                                                                  format(
                                                                                                      os.path.basename(
                                                                                                          EDIT_IMAGE_PATH))))
        IMAGE_INFO_LABEL.place(x=1075, y=500, anchor=tk.CENTER, width=200, height=50)

        NO_EDIT_LABEL = tk.Label(self, text="No change has been done", bg="black", fg="white",
                                 font=("Arial", 12, "bold"), padx=20, pady=20,
                                 bd=3, relief=tk.RAISED)
        NO_EDIT_LABEL.place(x=835, y=550, anchor=tk.CENTER, width=220, height=25)


class UploadPicturesPage(tk.Frame):
    """

    """

    def __init__(self, master):
        super().__init__(master)
        global NUMBER_PICTURE, STORAGE_PATH_PICTURE, UPLOAD_PICTURE_BUTTON_PICTURE_PAGE, SELECT_IMAGE_BUTTON, EDIT_IMAGE, \
            PANEL_STORAGE, NO_PICTURE_SELECTED, NUMBER_PAGE
        self.configure(bg=BACKGROUND_COLOR)

        NO_PICTURE_SELECTED = tk.Label(self, text="No picture was selected", bg=COLOR, fg="white",
                                       font=("Arial", 12, "bold"), padx=20, pady=20,
                                       bd=3, relief=tk.RAISED)
        tk.Label(self, text="Upload pictures Page", bg=BACKGROUND_COLOR, fg="white", font=LARGE_FONT, padx=20,
                 pady=20, bd=3). \
            place(x=600, y=20, anchor=tk.CENTER, width=1200, height=80)
        tk.Label(self, text="You can upload up to four pictures", bg="black", fg="white", font=("Arial", 12, "bold"),
                 padx=20, pady=20, bd=3, relief=tk.RAISED). \
            place(x=180, y=662.5, anchor=tk.CENTER, width=300, height=25)
        SELECT_IMAGE_BUTTON = tk.Button(self, text="Select Image", bg=COLOR, fg="white", font=("Arial", 12, "bold"),
                                        padx=20, pady=20, bd=3, relief=tk.RAISED,
                                        activebackground=BACKGROUND_BUTTON_COLOR,
                                        command=lambda: select_image(self, SELECT_IMAGE_BUTTON))
        UPLOAD_PICTURE_BUTTON_PICTURE_PAGE = tk.Button(self, text="Upload", bg=COLOR, fg="white",
                                                       font=("Arial", 12, "bold"), padx=20, pady=20, bd=3,
                                                       relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                                                       command=lambda: (uploads_pictures_to_server
                                                                        (NUMBER_PICTURE, self,
                                                                         "picture_Page")))
        undo_upload_button = tk.Button(self, text="Undo recent pic", bg=COLOR, fg="white",
                                       font=("Arial", 12, "bold"), padx=20, pady=20, bd=3,
                                       relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                                       command=lambda: undo_selected_picture(SELECT_IMAGE_BUTTON, self))
        tk.Button(self, text="Pictures page", bg=COLOR, fg="white", font=("Arial", 12, "bold"), padx=20, pady=20,
                  bd=3, relief=tk.RAISED, activebackground=BACKGROUND_BUTTON_COLOR,
                  command=lambda: master.switch_frame(master.picture_page_frames[0], 3)). \
            place(x=150, y=700, anchor=tk.CENTER, width=300, height=50)

        NUMBER_PICTURE = 0
        undo_upload_button.place(x=1050, y=700, anchor=tk.CENTER, width=300, height=50)
        UPLOAD_PICTURE_BUTTON_PICTURE_PAGE.place(x=450, y=700, anchor=tk.CENTER, width=300, height=50)
        SELECT_IMAGE_BUTTON.place(x=750, y=700, anchor=tk.CENTER, width=300, height=50)


def running_gui():
    """

    :return:
    """
    global root
    root.title("pictures for your day")
    root.minsize(1200, 800)
    root.mainloop()


if __name__ == '__main__':

    PHOTOS_SAVED_FILE = 'PhotosFromServer'
    # Check if folder exists
    if not os.path.exists(PHOTOS_SAVED_FILE):
        # Create folder if it does not exist
        os.makedirs(PHOTOS_SAVED_FILE)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    root = MainWindow()
    context = ssl.create_default_context()

    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    my_socket = socket.socket()
    conn = context.wrap_socket(my_socket, server_hostname=HOST_NAME)
    try:
        RESULT = conn.connect_ex((HOST_NAME, PORT))
        print("Connected to Server: ", conn.getsockname())
        running_gui()
    except socket.error as socket_err:
        print(f"Something came up: {socket_err}")
    finally:
        RESULT = my_socket.connect_ex((HOST_NAME, PORT))
        if RESULT == 0:
            exit_window()
        conn.close()
        quit()
