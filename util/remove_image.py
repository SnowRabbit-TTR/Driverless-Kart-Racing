import os

COURSE_ID = "s1n"
MODE = "train"
IMAGE_DIR = os.path.join("image", COURSE_ID, MODE)

def remove_image(image_dir):
    file_list = os.listdir(image_dir)
    if len(file_list) > 0:
        rm_command = "rm {}/*".format(image_dir)
        os.system(rm_command)
        print("{} files are removed.".format(len(file_list)))
    else:
        print("There is no file to remove.")

if __name__ == "__main__":
    remove_image(IMAGE_DIR)
