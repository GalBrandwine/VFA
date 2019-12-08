import PySimpleGUI as sg
import re
import hashlib

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

right_button_pane = [

    [sg.Text('DVFA actions')],
    [sg.Button('Intersect')],
    [sg.Button('Union')]
]

left_dvfa_column = [

    [sg.Text('DVFA 1')],
    [sg.Text('Load DVFA1:'), sg.InputText(), sg.FileBrowse()],
    [sg.Button('Generate DVFA1')],
    [sg.FileSaveAs("Save DVFA1")]
    # [sg.Text('Load DVFA:'), sg.InputText(), sg.FileBrowse(),
    #  sg.Checkbox('MD5'), sg.Checkbox('SHA1')
    #  ]
]
right_dvfa_column = [

    [sg.Text('DVFA 2')],
    [sg.Text('Load DVFA2:'), sg.InputText(), sg.FileBrowse()],
    [sg.Button('Generate DVFA2')],
    [sg.FileSaveAs("Save DVFA2")]
]
layout = [
    [sg.Column(left_dvfa_column, background_color='#d3dfda'), sg.Column(right_dvfa_column, background_color='#d3dfda'),
     sg.Column(right_button_pane, background_color='#d3dfda')],
    [sg.Output(size=(88, 20))],
    [sg.Submit(), sg.Cancel()]
]

window = sg.Window('DVFA tool', layout)


# generate_popup = sg.Window('Enter a number example', generate_vdfa)
def generate_popup():
    generate_vdfa = [
        [sg.Checkbox('3PAL')],
        [sg.Ok(), sg.Cancel()]
    ]
    sg_generate_popup = sg.Window('DVFA generator', generate_vdfa)
    res_event, res_values = sg_generate_popup.Read()
    sg_generate_popup.close()
    return res_event, res_values


def generate_dvfa(event, values):
    # Check input:
    checked_counter = 0
    checked_index = -1
    for key, value in values.items():
        checked_counter = (checked_counter + 1) if value is True else checked_counter
        checked_index = key

    if checked_counter is 0 or checked_counter > 1:
        sg.popup_error("MUST CHECK SOMETHING")
        return

    if checked_index is 0:
        # Generate 3PAL
        return dvfa_generator.create_3PAL_DVFA()

    return None


while True:  # The Event Loop
    event, values = window.read()
    print(event, values)  # debug

    if event in (None, 'Exit', 'Cancel'):
        break

    # Generate button pressed
    if event == 'Generate DVFA1':
        gen_event, gen_values = generate_popup()
        # print(gen_event, gen_values)  # debug
        if gen_event == "Ok":
            dvfa1 = generate_dvfa(gen_event, gen_values)
            print(" DVFA 1 Generated: {}".format(dvfa1))

    if event == 'Generate DVFA2':
        gen_event, gen_values = generate_popup()
        # print(gen_event, gen_values)  # debug
        if gen_event == "Ok":
            dvfa2 = generate_dvfa(gen_event, gen_values)
            print(" DVFA 2 Generated: {}".format(dvfa2))
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
