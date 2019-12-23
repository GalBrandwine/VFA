import os

import PySimpleGUI as sg
import re
import hashlib

import DVFApy
from Utils import dvfa_generator
import Utils as utils

# Gui config
sg.ChangeLookAndFeel('GreenTan')
popup_error_title = "Bad kitten!"

# Global variables
dvfa1 = None
dvfa2 = None
word = None


def hash(fname, algo):
    if algo == 'MD5':
        hash = hashlib.md5()
    elif algo == 'SHA1':
        hash = hashlib.sha1()
    elif algo == 'SHA256':
        hash = hashlib.sha256()
    with open(fname) as handle:  # opening the file one line at a time for memory considerations
        for line in handle:
            hash.update(line.encode(encoding='utf-8'))
    return (hash.hexdigest())


# # ------ Menu Definition ------ #
# menu_def = [['File', ['Open', 'Save', 'Exit', 'Properties']],
#             ['Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
#             ['Help', 'About...'], ]

word_pane = [
    [sg.Text('WORD')],
    [sg.Button('Create', key="Create_WORD")],
    # Stupid invisible line for triggering an EVENT, after leading a file.
    [sg.Input(key='Load_WORD', enable_events=True, visible=False)],
    [sg.FileBrowse("Load", key='Load_WORD_path', file_types=(("CSV Files", "*.csv"),), target='Load_WORD')],
    [sg.Input(key='save_WORD', enable_events=True, visible=False)],
    [sg.FileSaveAs(key='Save_WORD_path', file_types=(("CSV Files", "*.csv"),), target='save_WORD')]
]

right_button_pane = [
    [sg.Text('DVFA actions')],
    [sg.Button('Run')],
    [sg.Button('Intersect')],
    [sg.Button('Union')]
]

left_dvfa_column = [
    [sg.Text('DVFA 1')],
    [sg.Button('Generate', key="Generate_DVFA1")],
    [sg.Input(key='Load_DVFA1', enable_events=True, visible=False)],
    [sg.FileBrowse("Load", key="Load_DVFA1_path", file_types=(("PICKLE Files", "*.pickle"),), target='Load_DVFA1')],
    [sg.Input(key='save_DVFA1', enable_events=True, visible=False)],
    [sg.FileSaveAs(key='Save_DVFA1_path', file_types=(("PICKLE Files", "*.pickle"),), target='save_DVFA1')]
    # [sg.Text('Load DVFA:'), sg.InputText(), sg.FileBrowse(),
    #  sg.Checkbox('MD5'), sg.Checkbox('SHA1')
    #  ]
]

right_dvfa_column = [
    [sg.Text('DVFA 2')],
    [sg.Button('Generate', key="Generate_DVFA2")],
    [sg.Input(key='Load_DVFA2', enable_events=True, visible=False)],
    [sg.FileBrowse("Load", key="Load_DVFA2_path", file_types=(("PICKLE Files", "*.pickle"),), target='Load_DVFA2')],
    [sg.Input(key='save_DVFA2', enable_events=True, visible=False)],
    [sg.FileSaveAs(key='Save_DVFA2_path', file_types=(("PICKLE Files", "*.pickle"),), target='save_DVFA2')]
]

layout = [
    [sg.Column(left_dvfa_column, background_color='#d3dfda'), sg.Column(right_dvfa_column, background_color='#d3dfda'),
     sg.Column(word_pane, background_color='#d3dfda')],
    [sg.Output(size=(80, 15)), sg.Column(right_button_pane, background_color='#d3dfda')],
    [sg.Submit(), sg.Cancel()]
]

window = sg.Window('DVFA tool', layout)


def generate_popup():
    generate_vdfa = [
        [sg.Checkbox('3PAL', key="3PAL"), sg.Checkbox('1_X_plus', key="1_X_plus")],
        [sg.Ok(), sg.Cancel()]
    ]
    sg_generate_popup = sg.Window('DVFA generator', generate_vdfa)
    res_event, res_values = sg_generate_popup.Read()
    sg_generate_popup.close()
    return res_event, res_values


def generate_dvfa(event: str, values: dict) -> DVFApy.dvfa.DVFA:
    # Check input:
    checked = len([value for value in values.values() if value is True])
    if checked > 1:
        sg.popup_error("MUST CHECK ONLY ONE", title=popup_error_title)
        return None
    elif checked is 0:
        sg.popup_error("MUST CHECK SOMETHING", title=popup_error_title)
        return None

    for key, value in values.items():
        if key == "3PAL" and value is True:
            # Generate 3PAL
            return dvfa_generator.create_3PAL_DVFA()
        if key == "1_X_plus":
            return dvfa_generator.create_1_x_plus_DVFA()


def create_word_popup() -> (str, dict):
    word_popup = [
        [sg.Text('Type new WORD:'), sg.InputText()],
        [sg.Ok(), sg.Cancel()]
    ]

    popup = sg.Window('Word creator', word_popup)
    res_event, res_values = popup.Read()
    popup.close()

    return res_event, res_values


def create_word(create_word_values: dict) -> DVFApy.word.Word:
    # This function do 2 things:
    # 1. makes a list of integers
    # 2. than creates a WORD from that list.
    return DVFApy.word.Word([int(d) for d in create_word_values[0]])


def run_popup() -> (str, dict):
    run_popup = [
        [sg.Checkbox('DVFA 1', key="DVFA_1"), sg.Checkbox('DVFA 2', key="DVFA_2")],
        [sg.Ok(), sg.Cancel()]
    ]

    popup = sg.Window('Word creator', run_popup)
    res_event, res_values = popup.Read()
    popup.close()
    return res_event, res_values


def run_on_word(event: str, values: dict):
    if event == "Ok":
        message = ""

        # Check input
        if all(value is False for value in values.values()):
            sg.popup_error("MUST CHECK SOMETHING", title=popup_error_title)
            return

        for key, value in values.items():
            if key == "DVFA_1" and value is True:
                try:
                    is_word_accepted = DVFApy.run.Run(dvfa1, word).run()
                    message = (message + "DVFA1") + " " + ("accepted" if is_word_accepted is True else "denied")

                except AttributeError as err:
                    message = message + " Generate DVFA1 first! "

            if key == "DVFA_2" and value is True:
                try:
                    is_word_accepted = DVFApy.run.Run(dvfa2, word).run()
                    message = (message + "DVFA2") + " " + ("accepted" if is_word_accepted is True else "denied")
                    print(is_word_accepted)
                except AttributeError as err:
                    message = message + " Generate DVFA2 first! "
        print(message)


def create_word_from_csv(path) -> DVFApy.word.Word:
    global word
    word = utils.word_loader.load(path)
    print("Word loaded: {}".format(word))


def save_word(given_path: str):
    path, name = os.path.split(given_path)
    utils.word_saver.save(word, path, name)


def save_dvfa(dvfa: DVFApy, given_path: str):
    path, name = os.path.split(given_path)
    utils.dvfa_saver.save(dvfa, path, name)


def load_dvfa(given_path) -> DVFApy.dvfa.DVFA:
    loaded_dvfa = utils.dvfa_loader.load(given_path)
    return loaded_dvfa


while True:  # The Event Loop
    event, values = window.read()
    print(event, values)  # debug
    print('\n')

    if event in (None, 'Exit', 'Cancel'):
        break

    # Generate button pressed
    if event == 'Generate_DVFA1':
        gen_event, gen_values = generate_popup()
        # print(gen_event, gen_values)  # debug
        if gen_event == "Ok":
            dvfa1 = generate_dvfa(gen_event, gen_values)
            if isinstance(dvfa1, DVFApy.dvfa.DVFA):
                print(" DVFA 1 Generated: {}".format(dvfa1))
            else:
                print("DVFA 1 not generated!")

    if event == 'Generate_DVFA2':
        gen_event, gen_values = generate_popup()
        # print(gen_event, gen_values)  # debug
        if gen_event == "Ok":
            dvfa2 = generate_dvfa(gen_event, gen_values)
            if isinstance(dvfa2, DVFApy.dvfa.DVFA):
                print(" DVFA 2 Generated: {}".format(dvfa2))
            else:
                print("DVFA 2 not generated!")
    # Save DVFA1
    if event == 'save_DVFA1':
        if dvfa1 is None:
            sg.popup_error("DVFA1 Not created yet!", title=popup_error_title, )
        given_path = values['Save_DVFA1_path']
        save_dvfa(dvfa1, given_path)
    # Save DVFA2
    if event == 'save_DVFA2':
        if dvfa2 is None:
            sg.popup_error("DVFA2 Not created yet!", title=popup_error_title, )
        given_path = values['Save_DVFA2_path']
        save_dvfa(dvfa2, given_path)
    # Load DVFA1
    if event == 'Load_DVFA1':
        given_path = values['Load_DVFA1_path']
        dvfa1 = load_dvfa(given_path)
    # Load DVFA2
    if event == 'Load_DVFA2':
        given_path = values['Load_DVFA2_path']
        dvfa2 = load_dvfa(given_path)
    # Create word button pressed
    if event == "Create_WORD":
        create_word_event, create_word_values = create_word_popup()
        if create_word_event == "Ok":
            word = create_word(create_word_values)
            print("Word generated = {}, length:{}".format(word.word, word.get_word_length()))
    # Save word to path
    if event == "save_WORD":
        given_path = values['Save_WORD_path']
        save_word(given_path)
    # Load word from path
    if event == "Load_WORD":
        given_path = values['Load_WORD_path']
        if len(given_path) is 0:
            sg.popup_error("Press BROWSE and choose a file!", title=popup_error_title, )
        else:
            create_word_from_csv(given_path)

    # Run button pressed
    if event == "Run":
        if isinstance(word, DVFApy.word.Word):
            run_event, run_values = run_popup()
            run_on_word(run_event, run_values)
        else:
            sg.popup_error("First create a WORD!", title=popup_error_title, )

    if event == 'Submit':
        file1 = file2 = isitago = None
        # print(values[0],values[3])
        if values[0] and values[3]:
            file1 = re.findall('.+:\/.+\.+.', values[0])
            file2 = re.findall('.+:\/.+\.+.', values[3])
            isitago = 1
            if not file1 and file1 is not None:
                print('Error: File 1 path not valid.')
                isitago = 0
            elif not file2 and file2 is not None:
                print('Error: File 2 path not valid.')
                isitago = 0
            elif values[1] is not True and values[2] is not True and values[4] is not True:
                print('Error: Choose at least one type of Encryption Algorithm')
            elif isitago == 1:
                print('Info: Filepaths correctly defined.')
                algos = []  # algos to compare
                if values[1] == True: algos.append('MD5')
                if values[2] == True: algos.append('SHA1')
                if values[4] == True: algos.append('SHA256')
                filepaths = []  # files
                filepaths.append(values[0])
                filepaths.append(values[3])
                print('Info: File Comparison using:', algos)
                for algo in algos:
                    print(algo, ':')
                    print(filepaths[0], ':', hash(filepaths[0], algo))
                    print(filepaths[1], ':', hash(filepaths[1], algo))
                    if hash(filepaths[0], algo) == hash(filepaths[1], algo):
                        print('Files match for ', algo)
                    else:
                        print('Files do NOT match for ', algo)
        else:
            print('Please choose 2 files.')
window.close()
