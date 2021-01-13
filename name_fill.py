import glob
import os

def main(path, wildcard="*.dungeon"):
    """Sucht sich alle .dungeons und füllt sie auf die maximale indexgröße auf
        1.dungeon, 1000.dungeon -> 0001.dungeon, 1000.dungeon"""
    max_index = 0
    max_x = 0
    max_y = 0


    files = glob.glob(os.path.join(path, wildcard))
    file_names = [f[len(path) + 1:] for f in files]

    #Sucht den höchsten Namen raus
    for file in file_names:
        file_prefix = file[:-8]
        if int(file_prefix) > max_index:
            max_index = int(file_prefix)

    dec_places = len(str(max_index))

    for file in file_names:
        file_prefix = file[:-8]
        str_len = 8 + dec_places
        if len(file_prefix) < dec_places:
            new_name = os.path.join(path, file.zfill(str_len))
            old_name = os.path.join(path, file)
            os.rename(old_name, new_name)

    return



if __name__ == "__main__":
    main(".") #"." Referenz für das aktuelle verzeichnis und : für das übergeordnete