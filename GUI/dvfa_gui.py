import os
import resource
import sys
from functools import wraps
from timeit import default_timer as timer

import PySimpleGUI as sg

import DVFApy
import Utils as utils
from Utils import dvfa_generator
from Utils import logger

about = """
This is The VDFA tool.

A tool for creating DVFAs, and performing operations on them.

Capabilities:
    DVFA section:
        1. Press "Generate" - to generate one of the optional DVFAs.
        2. Press "Load"     - to load a VDFA from disk.
        3. Press "Save as"  - to save a VDFA to disk.
        4. Unwind           - to unwind current DVFA, unwinded result will overwrite existing one.
        4. Complement       - to complement current DVFA, complemented result will overwrite existing one.
    
    WORD section:
        1. Press "Create"   - to create a WORD, a word contain numbers only, and will look like: 1,30,2,........
        2. Press "Load"     - to load a WORD from disk.
        3. Press "Save as"  - to save a WORD to disk.
    
    DVFA Actions section:
        1. Press "Run on"           - to Run a WORD on a DVFA.
            (note: WORD & DVFA's must be created before.)
        2. press "Intersect into"   - to intersect DVFA1 and DVFA2 into selected DVFA from checkbox.
        3. press "Union into"       - to union DVFA1 and DVFA2 into selected DVFA from checkbox.
    
    Settings:
        set RecursionLimit:
            This limit prevents any program from getting into infinite recursion, 
            Otherwise infinite recursion will lead to overflow of the C stack and crash the Python.
            The highest possible limit is platform-dependent. 
            This should be done with care because too-high limit can lead to crash.
           
            Default value is 0x1000.
            We found that the RECURSIONLIMITs upper bound for DVFAs with 45k states
            require a limit that is at least 0x3356
"""

# Gui config
sg.ChangeLookAndFeel('DefaultNoMoreNagging')

# Global variables
NAME_DVFA1 = "DVFA1"
NAME_DVFA2 = "DVFA2"
dvfa1: DVFApy.dvfa.DVFA = None
dvfa2: DVFApy.dvfa.DVFA = None
word: DVFApy.word.Word = None
MAX_REC_LIMIT = 0x1000

# Error Messages
POPUPERRORTITLE = "Bad Kitty!"
UNCECKED = "Check at least one option!"
TOOMANYCHECKED = "Check only one option!"
NOTGENERATED = "Generate {} first!"
HELPSTR = "About..."
SETTINGS_RECURSION_LIMIT = 'set RecursionLimit'

# Button Sizes
SMALLBUTTONSIZE = (10, 1)
LARGEBUTTONSIZE = (12, 1)

# ------ Menu Definition ------ #
menu_def = [['Setting', 'set RecursionLimit'],
            ['Help', 'About...'], ]

word_pane = [
    [sg.Button('Create', key="Create_WORD", size=SMALLBUTTONSIZE)],
    # Stupid invisible line for triggering an EVENT, after leading a file.
    [sg.Input(key='Load_WORD', enable_events=True, visible=False)],
    [sg.FileBrowse("Load", key='Load_WORD_path', size=SMALLBUTTONSIZE, file_types=(("CSV Files", "*.csv"),),
                   target='Load_WORD')],
    [sg.Input(key='Save_WORD', enable_events=True, visible=False)],
    [sg.FileSaveAs(key='Save_WORD_path', size=SMALLBUTTONSIZE, file_types=(("CSV Files", "*.csv"),),
                   target='Save_WORD')],
    [sg.Text(size=SMALLBUTTONSIZE)],
    [sg.Text(size=SMALLBUTTONSIZE)],
    [sg.Text(size=SMALLBUTTONSIZE)]
]

right_button_pane = [
    [sg.Button('Run on:', key='Run', size=LARGEBUTTONSIZE),
     sg.Checkbox('{}'.format(NAME_DVFA1), key="run_{}".format(NAME_DVFA1)),
     sg.Checkbox('{}'.format(NAME_DVFA2), key="run_{}".format(NAME_DVFA2))],
    [sg.Button('Intersect into:', key='Intersect', size=LARGEBUTTONSIZE),
     sg.Checkbox('{}'.format(NAME_DVFA1), key="Intersect_{}".format(NAME_DVFA1)),
     sg.Checkbox('{}'.format(NAME_DVFA2), key="Intersect_{}".format(NAME_DVFA2))],
    [sg.Button('Union into:', key='Union', size=LARGEBUTTONSIZE),
     sg.Checkbox('{}'.format(NAME_DVFA1), key="Union_{}".format(NAME_DVFA1)),
     sg.Checkbox('{}'.format(NAME_DVFA2), key="Union_{}".format(NAME_DVFA2))],
    [sg.Text(size=SMALLBUTTONSIZE)],
    [sg.Text(size=SMALLBUTTONSIZE)],
    [sg.Text(size=SMALLBUTTONSIZE)],

]

left_dvfa_column = [
    [sg.Button('Generate', key="Generate_{}".format(NAME_DVFA1), size=SMALLBUTTONSIZE)],
    [sg.Input(key='Load_{}'.format(NAME_DVFA1), enable_events=True, visible=False)],
    [sg.FileBrowse("Load", key="Load_{}_path".format(NAME_DVFA1), size=SMALLBUTTONSIZE,
                   file_types=(("PICKLE Files", "*.pickle"),),
                   target='Load_{}'.format(NAME_DVFA1))],
    [sg.Input(key='save_{}'.format(NAME_DVFA1), enable_events=True, visible=False)],
    [sg.FileSaveAs(key='Save_{}_path'.format(NAME_DVFA1), size=SMALLBUTTONSIZE,
                   file_types=(("PICKLE Files", "*.pickle"),),
                   target='save_{}'.format(NAME_DVFA1))],
    [sg.Text('Actions:')],
    [sg.Button("Unwind", key='Unwind_{}'.format(NAME_DVFA1), size=SMALLBUTTONSIZE)],
    [sg.Button("Complement", key='Complement_{}'.format(NAME_DVFA1), size=SMALLBUTTONSIZE)]
]

right_dvfa_column = [
    [sg.Button('Generate', size=SMALLBUTTONSIZE, key="Generate_{}".format(NAME_DVFA2))],
    [sg.Input(key='Load_{}'.format(NAME_DVFA2), enable_events=True, visible=False)],
    [sg.FileBrowse("Load", key="Load_{}_path".format(NAME_DVFA2), size=SMALLBUTTONSIZE,
                   file_types=(("PICKLE Files", "*.pickle"),),
                   target='Load_{}'.format(NAME_DVFA2))],
    [sg.Input(key='save_{}'.format(NAME_DVFA2), enable_events=True, visible=False)],
    [sg.FileSaveAs(key='Save_{}_path'.format(NAME_DVFA2), size=SMALLBUTTONSIZE,
                   file_types=(("PICKLE Files", "*.pickle"),),
                   target='save_{}'.format(NAME_DVFA2))],
    [sg.Text('Actions:')],
    [sg.Button("Unwind", key='Unwind_{}'.format(NAME_DVFA2), size=SMALLBUTTONSIZE)],
    [sg.Button("Complement", key='Complement_{}'.format(NAME_DVFA2), size=SMALLBUTTONSIZE)]
]

layout = [
    [
        sg.Menu(menu_def, tearoff=True),
        sg.Frame(NAME_DVFA1, left_dvfa_column),
        sg.Frame(NAME_DVFA2, right_dvfa_column),
        sg.Frame('Word', word_pane),
        sg.Frame('DVFA Actions', right_button_pane)
    ],
    [
        sg.Output(size=(100, 15)),
    ],
    [sg.Text("DVFA tool by Alon Ben-yosef & Gal Brandwine " + chr(169))]
]

window = sg.Window('DVFA tool', layout)


def timeit_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = timer()
        func_return_val = func(*args, **kwargs)
        end = timer()
        # logger.log_print('Run time: {0:<10}.{1:<8} : {2:<8} sec'.format(func.__module__, func.__name__, end - start))
        logger.log_print('Run time: {0:<8} sec'.format(end - start))
        # logger.log_print('Run time: {0:<8} sec'.format(end - start))
        return func_return_val

    return wrapper


def set_recursion_limit_popup() -> None:
    global MAX_REC_LIMIT
    recursion_limit_popup = [
        [sg.Slider(range=(0x1000, 0x10000), orientation='h', size=(34, 20), default_value=sys.getrecursionlimit())],
        [sg.Ok(), sg.Cancel()]
    ]

    popup = sg.Window('Recursion Limit setting', recursion_limit_popup)
    res_event, res_values = popup.Read()
    if res_event == 'Ok':
        MAX_REC_LIMIT = int(res_values[0])
        resource.setrlimit(resource.RLIMIT_STACK, [0x100 * MAX_REC_LIMIT, resource.RLIM_INFINITY])
        sys.setrecursionlimit(MAX_REC_LIMIT)

    popup.close()


def about_popup() -> None:
    about_the_tool_popup = [
        [sg.Text(about)],
        [sg.Ok(), sg.Cancel()]
    ]

    popup = sg.Window('About', about_the_tool_popup)
    popup.Read()
    popup.close()


def generate_popup():
    generate_vdfa = [
        [sg.Checkbox('3PAL', key="3PAL"), sg.Checkbox('1_X_plus', key="1_X_plus")],
        [sg.Checkbox('WordLongerThanOne', key="WordLongerThanOne"), sg.Checkbox('1_2', key="1_2")],
        [sg.Checkbox('Herring', key="herring")],
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
        sg.popup_error(TOOMANYCHECKED, title=POPUPERRORTITLE)
        return None
    elif checked is 0:
        sg.popup_error(UNCECKED, title=POPUPERRORTITLE)
        return None

    for key, value in values.items():
        if key == "3PAL" and value is True:
            # Generate 3PAL
            return dvfa_generator.create_3PAL_DVFA()
        if key == "1_X_plus" and value is True:
            return dvfa_generator.create_1_x_plus_DVFA()
        if key == "WordLongerThanOne" and value is True:
            return dvfa_generator.create_word_longer_than_1()
        if key == "1_2" and value is True:
            return dvfa_generator.create_1_2()
        if key == "herring" and value is True:
            return dvfa_generator.create_herring_DVFA()


def create_word_popup() -> (str, dict):
    word_popup = [
        [sg.Text('Type new Word:'), sg.InputText()],
        [sg.Ok(), sg.Cancel()]
    ]

    popup = sg.Window('Word creator', word_popup)
    res_event, res_values = popup.Read()
    popup.close()

    return res_event, res_values


def create_word(create_word_values: dict) -> None:
    global word
    # This function do 2 things:
    # 1. makes a list of integers
    # 2. than creates a WORD from that list.
    input_string: str = create_word_values[0]
    splited = input_string.split(",")
    try:
        word = DVFApy.word.Word([int(d) for d in splited])
        logger.log_print("Word generated = {}, length:{}".format(word.word, word.get_word_length()))
    except ValueError as e:
        sg.PopupError(e, title=POPUPERRORTITLE)


@timeit_wrapper
def run_on_word(event: str, values: dict):
    if isinstance(word, DVFApy.word.Word) is False:
        sg.popup_error("First create a WORD!", title=POPUPERRORTITLE, )
        return

    # if event == "Ok":
    message = ""
    err_popup = False
    # Check input
    if values['run_{}'.format(NAME_DVFA1)] is False and values['run_{}'.format(NAME_DVFA2)] is False:
        message = UNCECKED
        sg.popup_error(message, title=POPUPERRORTITLE)
        return

    for key, value in values.items():
        if key == "run_{}".format(NAME_DVFA1) and value is True:
            try:
                is_word_accepted = DVFApy.run.Run(dvfa1, word).run()
                message = (message + "{}".format(NAME_DVFA1)) + " " + (
                    "accepted " if is_word_accepted is True else "denied ")
            except AttributeError as err:
                message = message + " " + NOTGENERATED.format(NAME_DVFA1)
                sg.popup_error(message, title=POPUPERRORTITLE)
                return
        if key == "run_{}".format(NAME_DVFA2) and value is True:
            try:
                is_word_accepted = DVFApy.run.Run(dvfa2, word).run()
                message = (message + "{}".format(NAME_DVFA2)) + " " + (
                    "accepted " if is_word_accepted is True else "denied ")
            except AttributeError as err:
                message = message + " " + NOTGENERATED.format(NAME_DVFA2)
                sg.popup_error(message, title=POPUPERRORTITLE)
                return
    logger.log_print(message)


def create_word_from_csv(path) -> None:
    global word

    if len(path) is 0:
        sg.popup_error("Press BROWSE and choose a file!", title=POPUPERRORTITLE, )
        return

    word = utils.word_loader.load(path)
    logger.log_print("Word loaded: {}".format(word))


def Save_WORD(path: str):
    if word is None:
        sg.popup_error(NOTGENERATED.format("word"), title=POPUPERRORTITLE, )
        return
    if len(path) is 0:
        sg.popup_error("Path is Empty", title=POPUPERRORTITLE, )
        return
    path, name = os.path.split(path)
    utils.word_saver.save(word, path, name)


def save_dvfa(dvfa_name: str, dvfa: DVFApy, given_path: str):
    if len(given_path) is 0:
        sg.popup_error("Path is Empty", title=POPUPERRORTITLE, )
        return
    if dvfa is None:
        sg.popup_error(NOTGENERATED.format(dvfa_name), title=POPUPERRORTITLE, )
        return
    path, name = os.path.split(given_path)
    utils.dvfa_saver.save(dvfa, path, name)


def load_dvfa(given_path) -> DVFApy.dvfa.DVFA:
    if len(given_path) is 0:
        sg.popup_error("Path is Empty", title=POPUPERRORTITLE, )
        return
    loaded_dvfa = utils.dvfa_loader.load(given_path)
    return loaded_dvfa


@timeit_wrapper
def intersect(event, values):
    global dvfa1
    global dvfa2

    message = ""

    # Check input:
    checked = 0
    if values['Intersect_{}'.format(NAME_DVFA1)] is True:
        checked = checked + 1
    if values['Intersect_{}'.format(NAME_DVFA2)] is True:
        checked = checked + 1

    if checked > 1:
        sg.popup_error(TOOMANYCHECKED, title=POPUPERRORTITLE)
        return
    elif checked is 0:
        sg.popup_error(UNCECKED, title=POPUPERRORTITLE)
        return

    # Check logic:
    if dvfa1 is None or dvfa2 is None:
        message = NOTGENERATED.format("dvfa1 and dvfa2")
        sg.popup_error(message, title=POPUPERRORTITLE)
        return

    # Execute Logic
    if values["Intersect_{}".format(NAME_DVFA1)] is True:
        dvfa1 = DVFApy.dvfa.DVFA.intersect(dvfa1, dvfa2)
        message = "Intersected into {}: {}".format(NAME_DVFA1, dvfa1.print())
        logger.log_print(message)
        return
    if values["Intersect_{}".format(NAME_DVFA2)] is True:
        dvfa2 = DVFApy.dvfa.DVFA.intersect(dvfa1, dvfa2)
        message = "Intersected into {}: {}".format(NAME_DVFA2, dvfa2.print())
        logger.log_print(message)
        return
    else:
        message = TOOMANYCHECKED
        sg.popup_error(message, title=POPUPERRORTITLE)


@timeit_wrapper
def union(event, values):
    global dvfa1
    global dvfa2

    message = ""

    # Check input:
    checked = 0
    if values['Union_{}'.format(NAME_DVFA1)] is True:
        checked = checked + 1
    if values['Union_{}'.format(NAME_DVFA2)] is True:
        checked = checked + 1

    if checked > 1:
        sg.popup_error(TOOMANYCHECKED, title=POPUPERRORTITLE)
        return
    elif checked is 0:
        sg.popup_error(UNCECKED, title=POPUPERRORTITLE)
        return

    # Check logic:
    if dvfa1 is None or dvfa2 is None:
        message = NOTGENERATED.format("dvfa1 and dvfa2")
        sg.popup_error(message, title=POPUPERRORTITLE)
        return

    # Execute Logic
    if values["Union_{}".format(NAME_DVFA1)] is True:
        dvfa1 = DVFApy.dvfa.DVFA.union(dvfa1, dvfa2)
        message = "United into {}: {}".format(NAME_DVFA1, dvfa1.print())
        logger.log_print(message)
        return
    if values["Union_{}".format(NAME_DVFA2)] is True:
        dvfa2 = DVFApy.dvfa.DVFA.union(dvfa1, dvfa2)
        message = "United into {}: {}".format(NAME_DVFA2, dvfa2.print())
        logger.log_print(message)
        return
    else:
        message = TOOMANYCHECKED
        sg.popup_error(message, title=POPUPERRORTITLE)


@timeit_wrapper
def unwind(event):
    global dvfa1
    global dvfa2

    if event == "Unwind_{}".format(NAME_DVFA1):
        # Check logic:
        if dvfa1 is None:
            message = NOTGENERATED.format(NAME_DVFA1)
            sg.popup_error(message, title=POPUPERRORTITLE)
            return
        # Execute Logic
        dvfa1, _ = DVFApy.dvfa.DVFA.unwind(dvfa1)
        logger.log_print("Unwinded: {}: {}".format(NAME_DVFA1, dvfa1.print()))
    elif event == "Unwind_{}".format(NAME_DVFA2):
        # Check logic:
        if dvfa2 is None:
            message = NOTGENERATED.format(NAME_DVFA2)
            sg.popup_error(message, title=POPUPERRORTITLE)
            return
        # Execute Logic
        dvfa2, _ = DVFApy.dvfa.DVFA.unwind(dvfa2)
        logger.log_print("Unwinded: {}: {}".format(NAME_DVFA2, dvfa2.print()))


@timeit_wrapper
def complement(event):
    global dvfa1
    global dvfa2

    if event == "Complement_{}".format(NAME_DVFA1):
        # Check logic:
        if dvfa1 is None:
            message = NOTGENERATED.format(NAME_DVFA1)
            sg.popup_error(message, title=POPUPERRORTITLE)
            return
        # Execute Logic
        dvfa1 = DVFApy.dvfa.DVFA.complement(dvfa1)
        logger.log_print("Complement: {}: {}".format(NAME_DVFA1, dvfa1.print()))
    elif event == "Complement_{}".format(NAME_DVFA2):
        # Check logic:
        if dvfa2 is None:
            message = NOTGENERATED.format(NAME_DVFA2)
            sg.popup_error(message, title=POPUPERRORTITLE)
            return
        # Execute Logic
        dvfa2 = DVFApy.dvfa.DVFA.complement(dvfa2)
        logger.log_print("Complement: {}: {}".format(NAME_DVFA2, dvfa2.print()))


def event_handler(event, values):
    global word
    global dvfa1
    global dvfa2

    # Generate button pressed
    if event == 'Generate_{}'.format(NAME_DVFA1):
        gen_event, gen_values = generate_popup()
        if gen_event == "Ok":
            dvfa1 = generate_dvfa(gen_event, gen_values)
            if isinstance(dvfa1, DVFApy.dvfa.DVFA):
                logger.log_print(" {} Generated: {}".format(NAME_DVFA1, dvfa1.print()))
            else:
                logger.log_print("{} not generated!".format(NAME_DVFA1))

    if event == 'Generate_{}'.format(NAME_DVFA2):
        gen_event, gen_values = generate_popup()
        if gen_event == "Ok":
            dvfa2 = generate_dvfa(gen_event, gen_values)
            if isinstance(dvfa2, DVFApy.dvfa.DVFA):
                logger.log_print(" {} Generated: {}".format(NAME_DVFA2, dvfa2.print()))

            else:
                logger.log_print("{} not generated!".format(NAME_DVFA2))

    # Save DVFA1
    if event == 'save_{}'.format(NAME_DVFA1):
        given_path = values['Save_{}_path'.format(NAME_DVFA1)]
        save_dvfa(NAME_DVFA1, dvfa1, given_path)

    # Save DVFA2
    if event == 'save_{}'.format(NAME_DVFA2):
        given_path = values['Save_{}_path'.format(NAME_DVFA2)]
        save_dvfa(NAME_DVFA2, dvfa2, given_path)

    # Load DVFA1
    if event == 'Load_{}'.format(NAME_DVFA1):
        given_path = values['Load_{}_path'.format(NAME_DVFA1)]
        dvfa1 = load_dvfa(given_path)
        logger.log_print(" {} Loaded: {}".format(NAME_DVFA1, dvfa1.print()))

    # Load DVFA2
    if event == 'Load_{}'.format(NAME_DVFA2):
        given_path = values['Load_{}_path'.format(NAME_DVFA2)]
        dvfa2 = load_dvfa(given_path)
        logger.log_print(" {} Loaded: {}".format(NAME_DVFA2, dvfa2.print()))

    # Create word button pressed
    if event == "Create_WORD":
        create_word_event, create_word_values = create_word_popup()
        if create_word_event == "Ok":
            create_word(create_word_values)

    # Save word to path
    if event == "Save_WORD":
        Save_WORD(values['Save_WORD_path'])
    # Load word from path
    if event == "Load_WORD":
        create_word_from_csv(values['Load_WORD_path'])

    # Run button pressed
    if event == "Run":
        run_on_word(event, values)

    # Intersect:
    if event == "Intersect":
        intersect(event, values)
    # Union:
    if event == "Union":
        union(event, values)

    # Unwind
    if event == "Unwind_{}".format(NAME_DVFA1):
        unwind(event)
    if event == "Unwind_{}".format(NAME_DVFA2):
        unwind(event)

    # Complement
    if event == "Complement_{}".format(NAME_DVFA1):
        complement(event)
    if event == "Complement_{}".format(NAME_DVFA2):
        complement(event)

    if event == HELPSTR:
        about_popup()
    if event == SETTINGS_RECURSION_LIMIT:
        set_recursion_limit_popup()


while True:  # The Event Loop
    event, values = window.read()
    # logger.log_print(event, values)  # debug

    if event in (None, 'Exit', 'Cancel'):
        break

    event_handler(event, values)

window.close()
