#!/usr/bin/env python
#set up project references for convenience

# print(fu.GetCompList())
# comp = fu.GetCompList()[2]
import os

def insert_into_comp(combo, comp, type):
    #insert and connect all the required tools
    media1 = comp.FindTool("MediaIn1")
    finalInputs = media1.FindMainOutput(1).GetConnectedInputs()
    if type == 'sf6_c':
        comp.Lock()
        media2 = comp.AddTool("Loader", 2, 2)
        media2.SetInput("Clip",f"{os.environ.get('HOMEPATH')}/Videos/Combo_Images/{combo}.png")
        comp.Unlock()
        merge1 = comp.AddTool("Merge", 2, 0)
        merge1.ConnectInput("Background", media1)
        merge1.ConnectInput("Foreground", media2)
        out1 = comp.FindTool("MediaOut1")
        out1.ConnectInput("Input", merge1)
        #connect merge node to all outputs that media1 originally had
        # for input in finalInputs.values():
        #     input.ConnectTo()
        #     input.ConnectTo(merge1.FindMainOutput(1))

        media1Attrs = media1.GetAttrs()#<---- this is the treasure trove of info
        # if media1Attrs["TOOLI_Clip_Width"] in media1Attrs:
        clipWidth = media1Attrs["TOOLI_Clip_Width"]
        # elif media1Attrs["TOOLIT_Clip_Width"] in media1Attrs:
            # print(media1Attrs["TOOLIT_Clip_Width"])
            # clipWidth = media1Attrs["TOOLIT_Clip_Width"][1]
        # else:
        #     print(media1Attrs["TOOLI_ImageWidth"])
            
            # clipWidth = media1Attrs["TOOLI_ImageWidth"]
            
        # clipHeight = media1Attrs["TOOLI_ImageHeight"]
        # clipName = media1Attrs["TOOLS_Clip_Name"]
        media2Attrs = media2.GetAttrs()
        imageWidth = media2Attrs["TOOLIT_Clip_Width"][1]
        # imageHeight = media2Attrs["TOOLIT_Clip_Height"][1]
        # imageName = media2Attrs["TOOLST_Clip_Name"]

        # image divided by canvas is one image length, anchor is center of image and 0,0 is bottom left of canvas
        imageScale = 0.6
        alignLeft = imageWidth/2/clipWidth * imageScale
        x = alignLeft
        y = 0.84
        merge1.SetInput("Center", {1: x, 2: y, 3: 0.0})
        merge1.SetInput("Size", imageScale)
        
    if type == 'sf6_m':
        print('working2')
        mInput = comp.FindTool("Merge1")
        if mInput == None:
            mInput = media1
        finalInputs = mInput.FindMainOutput(1).GetConnectedInputs()
        comp.Lock()
        media3 = comp.AddTool("Loader", 3, 2)
        media3.SetInput("Clip",f"C:/Users/gorne/Videos/Combo_Images/{combo}.png")
        comp.Unlock()
        merge2 = comp.AddTool("Merge", 3, 0)
        
        merge2.ConnectInput("Background", mInput)
        merge2.ConnectInput("Foreground", media3)
        #connect merge node to all outputs that media1 originally had
        for input in finalInputs.values():
            input.ConnectTo()
            input.ConnectTo(merge2.FindMainOutput(1))

        media3Attrs = media3.GetAttrs()#<---- this is the treasure trove of info
        media1Attrs = media1.GetAttrs()#<---- this is the treasure trove of info
        clipWidth = media1Attrs["TOOLI_Clip_Width"]
        imageWidth = media3Attrs["TOOLIT_Clip_Width"][1]

        # image divided by canvas is one image length, anchor is center of image and 0,0 is bottom left of canvas
        imageScale = 0.7
        alignLeft = imageWidth/2/clipWidth * imageScale
        x = alignLeft
        y = 0.15
        merge2.SetInput("Center", {1: x, 2: y, 3: 0.0})
        merge2.SetInput("Size", imageScale)