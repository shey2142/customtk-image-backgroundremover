try:
    import customtkinter
    import customtkinter as ctk
    import time
    import os
    import shutil
    from tkinter import filedialog
    from rembg import remove
    from PIL import Image
    import ctypes
    import platform
except:
    pass

my_list = []

def hide_folder(folder_path):
    if platform.system() == 'Windows':
        FILE_ATTRIBUTE_HIDDEN = 0x02
        ctypes.windll.kernel32.SetFileAttributesW(folder_path, FILE_ATTRIBUTE_HIDDEN)
    else:
        parent_dir, folder_name = os.path.split(folder_path)
        hidden_folder_name = '.' + folder_name
        hidden_folder_path = os.path.join(parent_dir, hidden_folder_name)
        os.rename(folder_path, hidden_folder_path)

def unhide_folder(folder_path):
    if platform.system() == 'Windows':
        FILE_ATTRIBUTE_NORMAL = 0x80
        ctypes.windll.kernel32.SetFileAttributesW(folder_path, FILE_ATTRIBUTE_NORMAL)
    else:
        parent_dir, folder_name = os.path.split(folder_path)
        if folder_name.startswith('.'):
            visible_folder_name = folder_name[1:]
            visible_folder_path = os.path.join(parent_dir, visible_folder_name)
            os.rename(folder_path, visible_folder_path)

def open_file_dialog():
    global my_list
    dir_path = "./"
    folder_name = "src"
    target_folder_path = os.path.join(dir_path, folder_name)
    file_paths = filedialog.askopenfilenames(
        title="Select Files", 
        filetypes=[("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*")]
    )
    if file_paths:
        if not os.path.exists(target_folder_path):
            os.mkdir(target_folder_path)
            hide_folder(target_folder_path)  # Hide the folder after creation
        for file_path in file_paths:
            my_list.append(os.path.basename(file_path))
            shutil.copy(file_path, target_folder_path)
        update_list()

def get_path(event):
    dropped_files = event.data.strip().split()
    valid_extensions = {'.png', '.jpg', '.jpeg'}
    dir_path = "./"
    folder_name = "src"
    target_folder_path = os.path.join(dir_path, folder_name)
    if not os.path.exists(target_folder_path):
        os.mkdir(target_folder_path)
        hide_folder(target_folder_path)  # Hide the folder after creation
    for dropped_file in dropped_files:
        dropped_file = dropped_file.strip()
        if dropped_file.startswith("{") and dropped_file.endswith("}"):
            dropped_file = dropped_file[1:-1]
        _, file_extension = os.path.splitext(dropped_file)
        if file_extension.lower() in valid_extensions:
            try:
                shutil.copy(dropped_file, target_folder_path)
                my_list.append(os.path.basename(dropped_file))
            except Exception as e:
                print(f"Failed to copy {dropped_file}: {e}")
        else:
            print(f"Invalid file type: {file_extension}. Only PNG and JPG files are allowed.")
    update_list()

def update_list():
    for widget in frame_list.winfo_children():
        widget.destroy()
    for i, file_name in enumerate(my_list):
        ctk.CTkLabel(master=frame_list, text=f"{i + 1} - {file_name}", font=("Arial", 8)).grid(row=i + 1, column=0, padx=10, pady=0.2)
    label_1.configure(text="Press start to remove background")

def clear_list():
    global my_list
    my_list.clear()
    update_list()
    if os.path.exists("./src"):
        shutil.rmtree("./src")
    label_1.configure(text="Upload PNG or JPG file please")

def remove_background(input_path, output_path):
    input_image = Image.open(input_path)
    output_image = remove(input_image)
    output_image.save(output_path)

def process_images_in_dir(input_dir, output_dir):
    unhide_folder(input_dir)  # Unhide the folder before processing
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                base, ext = os.path.splitext(filename)
                output_file_path = os.path.join(output_dir, f"{base}_no_bg.png")
                remove_background(file_path, output_file_path)
                print(f"Processed {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    hide_folder(input_dir)  # Re-hide the folder after processing

def start():
    input_dir = './src/' 
    output_dir = './output'
    try:
        if not os.path.exists(input_dir):
            label_1.configure(text="No file selected", text_color="white")
        else:
            process_images_in_dir(input_dir, output_dir)
            label_1.configure(text="Your files are ready in the output directory", font = ("Arial", 11))
            global my_list
            my_list.clear()
            update_list()
            
    except:
        pass
root = customtkinter.CTk()
root.geometry("350x150")
root.resizable(False, False)
root.title("Image Background Remover")

label_1 = customtkinter.CTkLabel(master=root, text="Upload PNG or JPG file please", text_color="white", font=("Arial", 12))
label_1.place(relx=0.7, rely=0.76, anchor=customtkinter.CENTER)
button1 = customtkinter.CTkButton(master=root, text="Open", command=open_file_dialog, width=70, height=70, border_spacing=4)
button1.place(relx=0.58, rely=0.36, anchor=customtkinter.CENTER)

button = customtkinter.CTkButton(master=root, text="Start", command=start, width=70, height=70, font=("arial", 12), border_spacing=2)
button.place(relx=0.82, rely=0.36, anchor=customtkinter.CENTER)

frame_list = customtkinter.CTkScrollableFrame(master=root, width=110, height=100, corner_radius=3)
frame_list.place(relx=0.03, rely=0.2)

button_cancel = customtkinter.CTkButton(master=root, text="Cancel", command=clear_list, width=100, height=20, font=("arial", 12), fg_color="#C70039")
button_cancel.place(relx=0.2, rely=0.1, anchor=customtkinter.CENTER)

root.mainloop()
