import numpy as np
import sys
from PIL import Image
import os
import contextlib


combo_string = '> lp lk mp 236mp 6k 6k'

spacer_size = 40

image_paths = os.listdir(f'{sys.path[0]}/combo_gen/images')

images =[ Image.open(f'{sys.path[0]}/combo_gen/images/{i}').convert("RGBA") for i in image_paths ]
spacer = Image.new('RGBA', (spacer_size, images[0].height), (0, 0, 0, 0))
images.append(spacer)
inputs = ['_','a','k','hk','lk','mk','p','hp','lp','mp','*','2','1','3','4','5','6','7','8','9','classic','dynamic','modern','sf6b','sf6','h','l','m','s','.']
buttons = {inputs[i]:images[i] for i in range(len(inputs))}

def input_processor(s: str):
    #**check for only a-z/num chars and casefold, convert spaces to .**
    # s = s.strip().casefold().replace(' ', '.')
    s = s.replace(' ', '.')
    #figure out what the intent of each input was
    #if s is followed by p, it is modern special
    #if k/p is not proceeded by an l/m/h, it is a generic button
    #if l/m/h is not followed by a k/p, it is a modern input
    sequence = []
    
    #label the input type by looking for the first button
    #if l/m/h is not followed by a kick or punch its modern, otherwise its classic
    #type classic = 0, modern = 1, invalid string = 2
    type = None
    for i,c in enumerate(s):
        if c.isdigit():
            continue
        if (i < (len(s)-1)):
            if (((c == 'l') or (c == 'm') or (c == 'h')) and not ((s[i+1] == 'p') or (s[i+1] =='k'))):
                type = 1
                s = s.replace('sp', 's')
                break
            type = 0
        type = 0
        
    if type == 0:
        for i,c in enumerate(s):
            if c.isdigit():
                sequence.append(c)
                continue
            #if this button is a strength modifier, add this and the next button
            if ((c == 'l') or (c == 'm') or (c == 'h')) and (i < len(s)-1):
                print(s[i]+s[i+1])
                sequence.append(s[i]+s[i+1])
                continue
            #if the last button isnt a strength modifier add this as generic button
            if not ((s[i-1] == 'l') or (s[i-1] == 'm') or (s[i-1] == 'h')):
                print(c)
                sequence.append(c)
                
    if type == 1:
        sequence = [*s]
    print(sequence)

    visual_sequence = [buttons[i] for i in sequence]
    #type classic = 0, modern = 1, invalid string = 2
    label = None
    if type == 0:
        label = 'sf6_c'
    if type == 1:
        label = 'sf6_m'
    return visual_sequence, label

def create_combo(combo_string:str = combo_string, dir:str=f'{os.environ["HOMEPATH"]}/videos/Combo_Images/'):
    """Provide a combo in numpad notation and an image will be created displaying the inputs.
    Returns the the type of combo that was found. Supports:
    sf6_c
    sf6_m
    
    You may provide a directory where you'd like it saved instead.
    
    Default: %USERPROFILE%/videos/Combo_Images/'"""
    #silence console outputs for production use - lazy way
    with contextlib.redirect_stdout(None):

        #clean and convert the string for use as a filename then
        #check if this combo already exists and create a directory if there is none
        combo_string = combo_string.strip().casefold().replace('>', '_').replace('sp', 's').replace('auto', 'a')
        filepath = f'{dir}{combo_string}.png'
        if os.path.exists(filepath):
            _, label = input_processor(combo_string)
            return label
        if not os.path.exists(dir):
            os.makedirs(dir)
        
        #determine what combo has been given, assemble it into an image, and return the combo type
        combo, label = input_processor(combo_string)
        print(combo)
        #save picture compilation
        try:
            combo = np.hstack([i for i in combo])
            final_image = Image.fromarray(combo)
            final_image.save(filepath)
        except:
            print("Valid combo not entered")
        print(filepath)
        return label
    
# final_image.show()