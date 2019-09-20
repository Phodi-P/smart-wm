from __future__ import print_function, unicode_literals
from PyInquirer import prompt, Token, style_from_dict, Separator

from PIL import Image

from functools import partial

from pyfiglet import Figlet

import random, os, sys, multiprocessing

import Visibility, Paste, CLI

global preferedPositions
global pickTheMostVisiblePosition
global visibilityThreshold
global logoPath
global inputPath
global outputPath
global processCount

##### Defaults Settings #####
preferedPositions = [(50, 100, "Center Bottom"), (0, 100, "Left Bottom"), (100, 100, "Right Bottom")]
pickTheMostVisiblePosition = True
visibilityThreshold = 60
logoPath = './logo.png'
inputPath = './input/'
outputPath = './output/'
processCount = 5


####################


def update():
    print('update')


class Settings:
    pass


def processImage(path, progress_list, settings):
    logoPath = settings.logoPath
    io_path = (settings.inputPath, settings.outputPath)
    result = Paste.pasteLogo(path, io_path, logoPath, settings.preferedPositions, settings.pickTheMostVisiblePosition,
                             settings.visibilityThreshold, progress_list, printStatus=True)
    if result is not None:
        progress_list[0].append((path, 'Done'))
    else:
        progress_list[0].append((path, 'Failed'))


def print_about():
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    about_dir = os.path.join(base_path, 'about.txt')

    try:
        about = open(about_dir, 'r')
        print(about.read())
    except Exception:
        pass


def mainMenu():
    settings = None
    f = Figlet(font='smslant')

    while (True):
        os.system('cls')
        print(f.renderText('Smart Watermark'))
        print('==========Welcome==========')
        answer = prompt(CLI.question, style=CLI.style)
        print('===========================\n\n')
        if answer["menu"] == 'settings':
            print('==========Path Settings==========')
            answers_path = prompt(CLI.questions_path, style=CLI.style)
            print('=================================\n\n')
            print('==========Performance Settings==========')
            answers_performance = prompt(CLI.questions_performance, style=CLI.style)
            print('========================================\n\n')
            print('==========Position Settings==========')
            answer_position = None
            answer_position_local = prompt(CLI.questions_position, style=CLI.style)
            if answer_position_local["defaultPos"] == True:
                answer_position = {
                    'positions': [(50, 100, 'Bot Middle'), (0, 100, 'Bot Left'), (100, 100, 'Bot Right')]}
            else:
                while (True):

                    answer_position_local = prompt(CLI.questions_position_select, style=CLI.style)
                    if (len(answer_position_local["positions"]) > 0):
                        answer_position = answer_position_local
                        break
                    else:
                        print('At least one position must be choose')
            print('========================================\n\n')

            # Applying settings
            preferedPositions = answer_position["positions"]
            pickTheMostVisiblePosition = answers_performance["mostVisible"]
            visibilityThreshold = int(answers_performance["threshold"])
            logoPath = answers_path["logoPath"]
            inputPath = answers_path["inputPath"]
            outputPath = answers_path["outputPath"]
            processCount = int(answers_performance["processCount"])

            settings = Settings()
            settings.preferedPositions = preferedPositions
            settings.pickTheMostVisiblePosition = pickTheMostVisiblePosition
            settings.visibilityThreshold = visibilityThreshold
            settings.logoPath = logoPath
            settings.inputPath = inputPath
            settings.outputPath = outputPath
            settings.processCount = processCount
        if answer["menu"] == 'about':
            print_about()
            print('\n\n')

            print('Press any key to CONTINUE')
            input()
        if answer["menu"] == 'exit':
            os.system('cls')
            sys.exit(0)
        if answer["menu"] == 'start':
            return settings


if __name__ == "__main__":
    multiprocessing.freeze_support()

    while (True):

        settings = mainMenu()
        if settings == None:
            settings = Settings()
            settings.preferedPositions = preferedPositions
            settings.pickTheMostVisiblePosition = pickTheMostVisiblePosition
            settings.visibilityThreshold = visibilityThreshold
            settings.logoPath = logoPath
            settings.inputPath = inputPath
            settings.outputPath = outputPath
            settings.processCount = processCount

        # Check for paths
        if not os.path.exists(inputPath):
            os.makedirs(inputPath)
        if not os.path.exists(outputPath + '/fix_manually'):
            os.makedirs(outputPath + '/fix_manually')
        if not os.path.exists(logoPath):
            raise Exception('Logo image not found')

        # Load logo
        logo = Image.open(logoPath)

        io_path = (inputPath, outputPath)

        # Counting files to process
        mustProcess = []
        for path in os.listdir(inputPath):
            if path.endswith('.jpg') or path.endswith('.png'):
                mustProcess.append(path)
        if len(mustProcess) == 0:
            raise Exception('No input image found')

        print('==========Starting watermarking processes==========')

        progress_list = (multiprocessing.Manager().list(), len(mustProcess))

        with multiprocessing.Pool(processes=processCount) as pool:
            arg = partial(processImage, progress_list=progress_list, settings=settings)

            pool.imap_unordered(arg, mustProcess)

            pool.close()
            pool.join()

        # Report the number of images Done and Failed
        Done = [i for i in progress_list[0] if i[1] == "Done"]
        Fail = [i for i in progress_list[0] if i[1] == "Failed"]
        print('----------Report----------')
        print('Done:' + str(len(Done)))
        print('Failed: ' + str(len(Fail)))
        print('--------------------------')
        print('===================================================\n\n')

        print('Press any key to CONTINUE')
        input()
