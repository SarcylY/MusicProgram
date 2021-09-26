import re

from Music.MusicStructures import Note, Accidental

_default_song_input_path: str = "./data/SongListData.txt"
_default_song_output_path: str = "./data/SongListOutput.txt"


def create_song_list_output(input_file: str = _default_song_input_path,
                            output_file: str = _default_song_output_path):
    """
    Converts the song list data into csv
    """
    file = open(input_file, "r")
    output = open(output_file, "w")
    if not file.readable():
        raise FileNotFoundError("Song list data not found.")
    if not output.writable():
        raise FileNotFoundError("Song List Output not writable")
    for line in file.readlines():
        final_line = re.sub("( = Note\\()|(_)", ",", line).replace(")", "").replace(" ", "").replace("\'", "")
        output.write(final_line)
    file.close()
    output.close()


def parse_song_list_output(output_file: str = _default_song_output_path):
    """
    Creates a dictionary containing all the song lists (names) and all the notes required
    The dictionary will be of format {name_of_song: [Array of notes]}
    """
    file = open(output_file, "r")
    if not file.readable():
        raise FileNotFoundError("Output data not found.")
    output_dict = {}
    for line in file.readlines():
        if len(line.strip()) == 0:
            continue
        csv_data = line.strip().split(",")
        if len(csv_data) != 6:
            print("Warning: line " + line + " does not have appropriate num items: " + str(len(csv_data))
                  + " (6 expected). Skipping.")
            continue
        if csv_data[0] not in output_dict:
            output_dict[csv_data[0]] = []
        if len(output_dict[csv_data[0]]) + 1 != int(csv_data[1]):
            print("Warning: line " + line + " has incorrect number " + csv_data[1]
                  + " (expected " + str(len(output_dict[csv_data[0]]) + 1) + ") . Continuing...")
        if len(csv_data[2]) != 1 or len(csv_data[3]) != 1:
            if len(csv_data[2]) == 0 or len(csv_data[3]) == 0:
                print("Warning: line " + line + " has 3rd/4th data Length 0. skipping.")
                continue
            else:
                print("Warning: line " + line + " has 3rd/4th data non length 1. Attempting to continue.")
        output_dict[csv_data[0]].append(Note(csv_data[2][0],
                                             Accidental.get_accidental(csv_data[3][0]),
                                             int(csv_data[4]),
                                             float(csv_data[5])))
    return output_dict


if __name__ == "__main__":
    create_song_list_output()
    result = parse_song_list_output()
