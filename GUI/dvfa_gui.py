import os
from functools import wraps
from timeit import default_timer as timer

import PySimpleGUI as sg

import DVFApy
from Utils import logger
from Utils import dvfa_generator
import Utils as utils


# Gui config
sg.ChangeLookAndFeel('GreenTan')
POPUPERRORTITLE = "Bad kitten!"

# Global variables
NAME_DVFA1 = "DVFA1"
NAME_DVFA2 = "DVFA2"
dvfa1: DVFApy.dvfa.DVFA = None
dvfa2: DVFApy.dvfa.DVFA = None
word: DVFApy.word.Word = None

# Error Messages
POPUPERRORTITLE = "Bad kitten!"
UNCECKED = "MUST CHECK SOMETHING"
TOOMANYCHECKED = "CHECK ONLY ONE"
NOTGENERATED = "Generate {} first!"

word_pane = [
    [sg.Text('WORD')],
    [sg.Button('Create', key="Create_WORD")],
    # Stupid invisible line for triggering an EVENT, after leading a file.
    [sg.Input(key='Load_WORD', enable_events=True, visible=False)],
    [sg.FileBrowse("Load", key='Load_WORD_path', file_types=(("CSV Files", "*.csv"),), target='Load_WORD')],
    [sg.Input(key='Save_WORD', enable_events=True, visible=False)],
    [sg.FileSaveAs(key='Save_WORD_path', file_types=(("CSV Files", "*.csv"),), target='Save_WORD')]
]

right_button_pane = [
    [sg.Text('DVFA actions:')],
    [sg.Button('Run on:', key='Run'), sg.Checkbox('{}'.format(NAME_DVFA1), key="run_{}".format(NAME_DVFA1)),
     sg.Checkbox('{}'.format(NAME_DVFA2), key="run_{}".format(NAME_DVFA2))],
    [sg.Button('Intersect into:', key='Intersect'),
     sg.Checkbox('{}'.format(NAME_DVFA1), key="Intersect_{}".format(NAME_DVFA1)),
     sg.Checkbox('{}'.format(NAME_DVFA2), key="Intersect_{}".format(NAME_DVFA2))],
    [sg.Button('Union into:', key='Union'), sg.Checkbox('{}'.format(NAME_DVFA1), key="Union_{}".format(NAME_DVFA1)),
     sg.Checkbox('{}'.format(NAME_DVFA2), key="Union_{}".format(NAME_DVFA2))],
]

left_dvfa_column = [
    [sg.Text('{}'.format(NAME_DVFA1))],
    [sg.Button('Generate', key="Generate_{}".format(NAME_DVFA1))],
    [sg.Input(key='Load_{}'.format(NAME_DVFA1), enable_events=True, visible=False)],
    [sg.FileBrowse("Load", key="Load_{}_path".format(NAME_DVFA1), file_types=(("PICKLE Files", "*.pickle"),),
                   target='Load_{}'.format(NAME_DVFA1))],
    [sg.Input(key='save_{}'.format(NAME_DVFA1), enable_events=True, visible=False)],
    [sg.FileSaveAs(key='Save_{}_path'.format(NAME_DVFA1), file_types=(("PICKLE Files", "*.pickle"),),
                   target='save_{}'.format(NAME_DVFA1))],
    [sg.Text('Actions:')],
    [sg.Button("Unwind", key='Unwind_{}'.format(NAME_DVFA1))],
    [sg.Button("Complement", key='Complement_{}'.format(NAME_DVFA1))],
]

right_dvfa_column = [
    [sg.Text('{}'.format(NAME_DVFA2))],
    [sg.Button('Generate', key="Generate_{}".format(NAME_DVFA2))],
    [sg.Input(key='Load_{}'.format(NAME_DVFA2), enable_events=True, visible=False)],
    [sg.FileBrowse("Load", key="Load_{}_path".format(NAME_DVFA2), file_types=(("PICKLE Files", "*.pickle"),),
                   target='Load_{}'.format(NAME_DVFA2))],
    [sg.Input(key='save_{}'.format(NAME_DVFA2), enable_events=True, visible=False)],
    [sg.FileSaveAs(key='Save_{}_path'.format(NAME_DVFA2), file_types=(("PICKLE Files", "*.pickle"),),
                   target='save_{}'.format(NAME_DVFA2))],
    [sg.Text('Actions:')],
    [sg.Button("Unwind", key='Unwind_{}'.format(NAME_DVFA2))],
    [sg.Button("Complement", key='Complement_{}'.format(NAME_DVFA2))],
]

layout = [
    [sg.Column(left_dvfa_column, background_color='#d3dfda'), sg.Column(right_dvfa_column, background_color='#d3dfda'),
     sg.Column(word_pane, background_color='#d3dfda')],
    [sg.Output(size=(80, 15)), sg.Column(right_button_pane, background_color='#d3dfda')],
    [sg.Exit()]
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


def generate_popup():
    generate_vdfa = [
        [sg.Checkbox('3PAL', key="3PAL"), sg.Checkbox('1_X_plus', key="1_X_plus")],
        [sg.Checkbox('WordLongerThanOne', key="WordLongerThanOne"), sg.Checkbox('1_2', key="1_2")],
        [sg.Checkbox('herring', key="herring")],
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
        [sg.Text('Type new WORD:'), sg.InputText()],
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
    if dvfa is None:
        sg.popup_error(NOTGENERATED.format(dvfa_name), title=POPUPERRORTITLE, )
        return
    path, name = os.path.split(given_path)
    utils.dvfa_saver.save(dvfa, path, name)


def load_dvfa(given_path) -> DVFApy.dvfa.DVFA:
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
        message = "Intersected into {}: {}".format(NAME_DVFA1, dvfa1.name)
        logger.log_print(message)
        return
    if values["Intersect_{}".format(NAME_DVFA2)] is True:
        dvfa2 = DVFApy.dvfa.DVFA.intersect(dvfa1, dvfa2)
        message = "Intersected into {}: {}".format(NAME_DVFA2, dvfa2.name)
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
        message = "United into {}: {}".format(NAME_DVFA1, dvfa1.name)
        logger.log_print(message)
        return
    if values["Union_{}".format(NAME_DVFA2)] is True:
        dvfa2 = DVFApy.dvfa.DVFA.union(dvfa1, dvfa2)
        message = "United into {}: {}".format(NAME_DVFA2, dvfa2.name)
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
        logger.log_print("unwinded: {}: {}".format(NAME_DVFA1, dvfa1.name))
    elif event == "Unwind_{}".format(NAME_DVFA2):
        # Check logic:
        if dvfa2 is None:
            message = NOTGENERATED.format(NAME_DVFA2)
            sg.popup_error(message, title=POPUPERRORTITLE)
            return
        # Execute Logic
        dvfa2, _ = DVFApy.dvfa.DVFA.unwind(dvfa2)
        logger.log_print("unwinded: {}: {}".format(NAME_DVFA2, dvfa2.name))


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
        logger.log_print("Complement_: {}: {}".format(NAME_DVFA1, dvfa1.name))
    elif event == "Complement_{}".format(NAME_DVFA2):
        # Check logic:
        if dvfa2 is None:
            message = NOTGENERATED.format(NAME_DVFA2)
            sg.popup_error(message, title=POPUPERRORTITLE)
            return
        # Execute Logic
        dvfa2 = DVFApy.dvfa.DVFA.complement(dvfa2)
        logger.log_print("Complement_: {}: {}".format(NAME_DVFA2, dvfa2.name))


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
                logger.log_print(" {} Generated: {}".format(NAME_DVFA1, dvfa1.name))
            else:
                logger.log_print("{} not generated!".format(NAME_DVFA1))

    if event == 'Generate_{}'.format(NAME_DVFA2):
        gen_event, gen_values = generate_popup()
        if gen_event == "Ok":
            dvfa2 = generate_dvfa(gen_event, gen_values)
            if isinstance(dvfa2, DVFApy.dvfa.DVFA):
                logger.log_print(" {} Generated: {}".format(NAME_DVFA2, dvfa2.name))
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

    # Load DVFA2
    if event == 'Load_{}'.format(NAME_DVFA2):
        given_path = values['Load_{}_path'.format(NAME_DVFA2)]
        dvfa2 = load_dvfa(given_path)

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


while True:  # The Event Loop
    event, values = window.read()
    logger.log_print(event, values)  # debug
    logger.log_print('\n')

    if event in (None, 'Exit', 'Cancel'):
        break

    event_handler(event, values)

window.close()
