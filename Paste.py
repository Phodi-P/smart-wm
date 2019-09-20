from PIL import Image
from colorama import init, Fore, Back, Style
import os
import Visibility

init(autoreset=True)

def getPasteOffset(bg, fg, pos, contain=True):
    """This function get offset for pasting the logo and also return sides for using with getVisibility()"""
    #Get images size
    bg_size = bg.size
    fg_size = fg.size

    #Calculatin offsets
    offset = [int(+pos[0]*(bg_size[0]/100)),int(pos[1]*(bg_size[1]/100))]

    offset[0] -= int(fg_size[0]/2)
    offset[1] -= int(fg_size[1]/2)

    #Calculating sides
    bg_sides = {"left" : 0, "right" : bg_size[0], "top" : 0, "bottom" : bg_size[1]}
    fg_sides = {"left" : offset[0], "right" : offset[0]+int(fg_size[0])
                , "top" : offset[1], "bottom" : offset[1]+int(fg_size[1]), "size" : fg_size, "relative_pos" : pos}

    #Constrainst fg inside bg
    if(contain):
        if fg_sides["left"] < bg_sides["left"]:
            # print('Adjusting left side')
            offset[0] += (bg_sides["left"]-fg_sides["left"])
            fg_sides["left"] += (bg_sides["left"]-fg_sides["left"])
            fg_sides["right"] += (bg_sides["left"]-fg_sides["left"])

        if fg_sides["right"] > bg_sides["right"]:
            # print('Adjusting right side')
            offset[0] += bg_sides["right"]-fg_sides["right"]
            fg_sides["left"] += bg_sides["right"]-fg_sides["right"]
            fg_sides["right"] += bg_sides["right"]-fg_sides["right"]
            

        if fg_sides["top"] < bg_sides["top"]:
            # print('Adjusting top side')
            offset[1] += (bg_sides["top"]-fg_sides["top"])
            fg_sides["top"] += (bg_sides["top"]-fg_sides["top"])
            fg_sides["bottom"] += (bg_sides["top"]-fg_sides["top"])

        if fg_sides["bottom"] > bg_sides["bottom"]:
            # print('Adjusting bottom side')
            offset[1] += bg_sides["bottom"]-fg_sides["bottom"]
            fg_sides["top"] += bg_sides["bottom"]-fg_sides["bottom"]
            fg_sides["bottom"] += bg_sides["bottom"]-fg_sides["bottom"]

    return [offset,fg_sides]

def pasteRelative(bg, fg, pos, contain=True):
    data = getPasteOffset(bg, fg, pos, contain=contain)

    offset = data[0]
    fg_sides = data[1]

    #Past fg on bg
    bg.paste(fg,offset,fg)

    return fg_sides

def pasteLogo(img_path, io_path, logoPath, logoBrightness, preferedPositions, pickTheMostVisiblePosition, visibilityThreshold, progress_list, printStatus = False):

    img = Image.open(os.path.join(io_path[0],img_path))
    logo = Image.open(logoPath)

    logo_sides = None

    pasted = False
    visibilities = []
    for pos in preferedPositions:
        visibility = Visibility.getVisibility(img,logoBrightness,getPasteOffset(img,logo,pos)[1])
        if pickTheMostVisiblePosition:
                visibilities.append(visibility)
        else:
            if visibility >= visibilityThreshold:
                logo_sides = pasteRelative(img,logo,pos)
                if printStatus:
                    print(Back.WHITE + Fore.BLACK +'[{}/{}]'.format(len(progress_list[0]),progress_list[1]),end='\t')
                    print(Fore.GREEN + pos[2]+' is chosen for '+ img_path)
                pasted = True
                break
    if pickTheMostVisiblePosition:
        maxVisibility = max(visibilities)
        if maxVisibility >= visibilityThreshold:
            logo_sides = pasteRelative(img,logo,preferedPositions[visibilities.index(maxVisibility)])
            if printStatus:
                print(Back.WHITE + Fore.BLACK + '[{}/{}]'.format(len(progress_list[0]),progress_list[1]),end='\t')
                print(Fore.GREEN + preferedPositions[visibilities.index(maxVisibility)][2]+' is chosen for '+ img_path)
            pasted = True
    if pasted:
        img.save(os.path.join(io_path[1],img_path), quality=95)
        del img
    else:
        img.save(os.path.join(io_path[1],'fix_manually',img_path), quality=95)
        if printStatus:
            print(Back.WHITE + Fore.BLACK + '[{}/{}]'.format(len(progress_list[0]),progress_list[1]),end='\t')
            print(Style.RESET_ALL,end="")
            print(Fore.RED +'Cannot find suitable location for '+ img_path)
            print(Style.RESET_ALL,end="")
        del img
    return logo_sides