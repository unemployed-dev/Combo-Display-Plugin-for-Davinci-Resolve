# Sample Workflow Integration script

import sys
sys.path.append('.\combo_gen')
import combo_gen.combo_gen as combo_gen
import combo_gen.fusion_interface as fi
import re
import time

#set up project references for convenience

resolve = app.GetResolve()
fusion = resolve.Fusion()
projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()
mediaPool = project.GetMediaPool()
storage = resolve.GetMediaStorage()
rootFolder = mediaPool.GetRootFolder()
timeLine = project.GetCurrentTimeline()
ui = fusion.UIManager
dispatcher = bmd.UIDispatcher(ui)
template = f'{sys.path[0]}/combo_gen/template.comp'

# some element IDs
winID = "Combo Display"	# should be unique for single instancing

# check for existing instance
win = ui.FindWindow(winID)
if win:
    win.Show()
    win.Raise()
    exit()
    
# otherwise, we set up a new window, with HTML header (using the Examples logo.png)
logoPath = fusion.MapPath(r"AllData:../Support/Developer/Workflow Integrations/Examples/SamplePlugin/img/logo.png")
header = '<html><body><h2 style="vertical-align:middle;">'
header = header + '<img src="' + logoPath + '"/>&nbsp;&nbsp;&nbsp;'
header = header + '</b>Combo Display Tool - by John Greggor</b>'
header = header + '</h1></body></html>'

# define the window UI layout
win = dispatcher.AddWindow({
        "ID" : winID,
        "WindowTitle" : "Combo Display",
        "Geometry" : [ 100,100,400,300 ],
    },
    ui.VGroup([
        ui.Label({ 'Text': header, 'Weight': 0.1, 'Font': ui.Font({ 'Family': "Times New Roman" }) }),
        ui.Label({ 'Text': "Inserts combo inputs onto the clip under your playhead."
            , 'Weight': 0, 'Font': ui.Font({ 'Family': "Times New Roman", 'PixelSize': 12 }) }),
        ui.VGap(1),
        ui.HGroup([
            ui.Button({ 'ID': "Insert",  'Text': "Insert" }),
            ui.HGap(5),
            ui.LineEdit({
                "ID": "Combo",
                "PlaceholderText": "Enter a combo using numpad notation.",
                "Weight":1.5,
                "MinimumSize":[250, 24],
            }),
        ]),
        # ui.VGap(0, 2),
        ui.Button({ "ID": "Auto-Insert", "Text": "Auto-Insert\n\n Looks for combo notation in the clip name, then in its filename.\n"
                "To be found notation must come after the characters \"cc,\"\n"
                "eg. \"My cool bnb cc,2hp 236hp.mp4\"\n"
                   "If nothing appears, no combo was found."}),
        ui.Button({ "ID": "Auto-Insert for Whole Timeline", "Text": "Auto-Insert for Whole Timeline"}),
        
    ])
 )

def FindComboString(clip):
    #search the clip name, then the source filename for a combo string. If none is found then return.
    clip = timeLine.GetCurrentVideoItem()
    comboString = re.findall(r"cc,.*", clip.GetName())
    if not comboString:
        comboString = re.findall(r"cc,.*", clip.GetMediaPoolItem().GetClipProperty('File Name'))
    if not comboString:
        return None
    comboString = re.sub(r'\.\w*$','', comboString[0])[3:]
    return comboString

# Event handlers
def OnClose(ev):
    dispatcher.ExitLoop()

def OnInsert(ev):
    comboString = win.Find('Combo').Text
    type = combo_gen.create_combo(comboString)
    print("test1")
    comp = timeLine.GetCurrentVideoItem().GetFusionCompByIndex(1)
    if comp == None:
        comp = timeLine.GetCurrentVideoItem().ImportFusionComp(template)
    print(type)
    fi.insert_into_comp(comboString, comp, type)
    print(f'Inserting {comboString}')
 
def OnAutoInsert(ev):
    '''Finds combo notation in the file or clip name, then inserts that into clip'''
    clip = timeLine.GetCurrentVideoItem()
    comp = clip.GetFusionCompByIndex(1)
    if comp == None:
        comp = timeLine.GetCurrentVideoItem().ImportFusionComp(template)
    comboString = FindComboString(clip)
    if not comboString:
        print("Couldn't find combo to auto-insert")
        return

    print(comboString)
    type = combo_gen.create_combo(comboString)
    fi.insert_into_comp(comboString, comp, type)
    print(f'Inserting {comboString}')
 
def OnAutoInsertFWTL(ev):
    '''EXPERIMENTAL: Does the same thing as OnAutoInsert, but for every clip in the timeline'''
    clips = timeLine.GetItemListInTrack('Video',1)
    print(clips)
    
    for clip in clips:
        comp = clip.GetFusionCompByIndex(1)
        if comp == None:
            comp = timeLine.GetCurrentVideoItem().ImportFusionComp(template)
        comboString = FindComboString(clip)
        if not comboString:
            print("Couldn't find combo to auto-insert")
            continue
        print(comboString)
        type = combo_gen.create_combo(comboString)
        fi.insert_into_comp(comboString, comp, type)
        print(f'Inserting {comboString}')
    dispatcher.ExitLoop()
 
def OnClear(ev):
    pass

# assign event handlers
win.On[winID].Close     = OnClose
win.On['Insert'].Clicked = OnInsert
win.On['Auto-Insert'].Clicked  = OnAutoInsert
win.On["Auto-Insert for Whole Timeline"].Clicked = OnAutoInsertFWTL



# Main dispatcher loop
win.Show()
dispatcher.RunLoop()

