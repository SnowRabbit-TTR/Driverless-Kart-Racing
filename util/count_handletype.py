import os

def count_handle(image_dir):
    image_files = os.listdir(image_dir)
    l_count = r_count = u_count = 0
    all_num = 0
    for image in image_files:
        handle = image.split("_")[2].split(".")[0]
        all_num += 1
        if handle[2] == "1":
            l_count += 1
        if handle[3] == "1":
            r_count += 1
        if handle[2] == "0" and handle[3] == "0":
            u_count += 1
    print("l : r : u = {0} : {1} : {2}".format(l_count, r_count, u_count))

if __name__ == "__main__":
    image_dir = os.path.join("image", "s1n", "train")
    count_handle(image_dir)
