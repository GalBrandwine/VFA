import PySimpleGUI as sg
import re
import hashlib

import DVFApy
from Utils import dvfa_generator

sg.ChangeLookAndFeel('GreenTan')

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
    [sg.Button('Create')],
    [sg.Button("Load"), sg.FileBrowse(key='Load_WORD_path')],
    [sg.Save(key="save_WORD"), sg.FileSaveAs(key='Save_WORD_path')]
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
    [sg.Button('Load', key="Load_DVFA1"), sg.FileBrowse(key="Load_DVFA1_path")],
    [sg.Save(key="save_DVFA1"), sg.FileSaveAs(key="Save_DVFA1_path")]
    # [sg.Text('Load DVFA:'), sg.InputText(), sg.FileBrowse(),
    #  sg.Checkbox('MD5'), sg.Checkbox('SHA1')
    #  ]
]

right_dvfa_column = [
    [sg.Text('DVFA 2')],
    [sg.Button('Generate', key="Generate_DVFA2")],
    [sg.Button('Load', key="Load_DVFA2"), sg.FileBrowse(key="Load_DVFA2_path")],
    [sg.Save(key="save_DVFA2"), sg.FileSaveAs(key="Save_DVFA2_path")]
    # [sg.Text('Load DVFA:'), sg.InputText(), sg.FileBrowse(),
    #  sg.Checkbox('MD5'), sg.Checkbox('SHA1')
    #  ]
]

layout = [
    [sg.Column(left_dvfa_column, background_color='#d3dfda'), sg.Column(right_dvfa_column, background_color='#d3dfda'),
     sg.Column(word_pane, background_color='#d3dfda')],
    [sg.Output(size=(150, 20)), sg.Column(right_button_pane, background_color='#d3dfda')],
    [sg.Submit(), sg.Cancel()]
]

window = sg.Window('DVFA tool', layout)


def generate_popup():
    generate_vdfa = [
        [sg.Checkbox('3PAL',key="3PAL")],
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
        sg.popup_error("MUST CHECK ONLY ONE")
        return None
    elif checked is 0:
        sg.popup_error("MUST CHECK SOMETHING")
        return None

    for key, value in values.items():
        if key == "3PAL" and value is True:
            # Generate 3PAL
            return dvfa_generator.create_3PAL_DVFA()


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
        [sg.Checkbox('DVFA 1'), sg.Checkbox('DVFA 2')],
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
            sg.popup_error("MUST CHECK SOMETHING")
            return

        for key, value in values.items():
            if key is 0 and value is True:
                try:
                    is_word_accepted = DVFApy.run.Run(dvfa1, word).run()
                    message = (message + "DVFA1") + " " + ("accepted" if is_word_accepted is True else "denied")

                except AttributeError as err:
                    message = message + " Generate DVFA1 first! "

            if key is 1 and value is True:
                try:
                    is_word_accepted = DVFApy.run.Run(dvfa2, word).run()
                    message = (message + "DVFA2") + " " + ("accepted" if is_word_accepted is True else "denied")
                    print(is_word_accepted)
                except AttributeError as err:
                    message = message + " Generate DVFA2 first! "
        print(message)


def create_word_from_csv(path):
    pass


while True:  # The Event Loop
    event, values = window.read()
    print(event, values)  # debug

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

    # Create word button pressed
    if event == "Create WORD":
        create_word_event, create_word_values = create_word_popup()
        if create_word_event == "Ok":
            word = create_word(create_word_values)
            print("Word generated = {}, length:{}".format(word.word, word.get_word_length()))
    # Load word from path
    if event == "Load word":
        create_word_from_csv(None)
    # Run button pressed
    if event == "Run":
        if isinstance(word, DVFApy.word.Word):
            run_event, run_values = run_popup()
            run_on_word(run_event, run_values)
        else:
            print("Please create a WORD!")

    if event == 'Save WORD':
        pass
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
