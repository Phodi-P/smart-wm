from __future__ import print_function, unicode_literals
from PyInquirer import prompt,Token,style_from_dict,Separator

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

question = [
    {
        'type': 'list',
        'name': 'menu',
        'message': 'Menu:',
        'choices' : [
            {
                'name' : 'Start watermarking process',
                'value' : 'start'
            },
            {
                'name' : 'Settings',
                'value' : 'settings'
            },
            {
                'name' : 'About',
                'value' : 'about'
            },
            {
                'name' : 'Exit',
                'value' : 'exit'
            }
            ],
        'default' : 0
    }
]

questions_path = [
    {
        'type': 'input',
        'name': 'logoPath',
        'message': 'Path to logo:',
        'default' : './logo.png'
    },
    {
        'type': 'input',
        'name': 'inputPath',
        'message': 'Path to input folder:',
        'default' : './input/'
    },
    {
        'type': 'input',
        'name': 'outputPath',
        'message': 'Path to output folder:',
        'default' : './output/'
    }
]

questions_performance = [
    {
        'type': 'input',
        'name': 'threshold',
        'message': 'Please set Visibility threshold <choose 1-100> (This will determine if the logo will be placed or not):',
        'default' : '55',
        'validate' : (lambda answer: (int(answer) <= 100 and int(answer) >= 1))
    },
    {
        'type': 'confirm',
        'name': 'mostVisible',
        'message': 'Use the most visible position? (This will make process slower):',
        'default' : True
    },
    {
        'type': 'input',
        'name': 'processCount',
        'message': 'How many processes do you want to use? <choose 1-10> (This will make process faster but use more resources):',
        'default' : '5',
        'validate' : (lambda answer: (int(answer) <= 10 and int(answer) >= 1))
    }
]
use_default_pos = False
questions_position = [
    {
        'type': 'confirm',
        'name': 'defaultPos',
        'message': 'Use the default positions? (Bot Left, Bot Middle, Bot Right):',
        'default' : True
    }
]
questions_position_select = [
        {
        'type': 'checkbox',
        'name': 'positions',
        'message': 'Select possible positions to place watermark:',
        'choices' : [
            Separator('-----Top-----'),
            {
                'name' : 'Top Left',
                'value' : (0,0,'Top Left')
            },
            {
                'name' : 'Top Middle',
                'value' : (50,0,'Top Middle')
            },
            {
                'name' : 'Top Right',
                'value' : (100,0,'Top Rigt')
            },
            Separator('-----Mid-----'),
            {
                'name' : 'Mid Left',
                'value' : (0,50,'Mid Left')
            },
            {
                'name' : 'Mid Middle',
                'value' : (50,50,'Top Middle')
            },
            {
                'name' : 'Mid Right',
                'value' : (100,50,'Top Right')
            },
            Separator('-----Bot-----'),
            {
                'name' : 'Bot Left',
                'value' : (0,100,'Bot Left')
            },
            {
                'name' : 'Bot Middle',
                'value' : (50,100,'Bot Middle')
            },
            {
                'name' : 'Bot Right',
                'value' : (100,100,'Bot Right')
            }
        ],
        'validate': (lambda answer: (len(answer) > 0))
    }
]