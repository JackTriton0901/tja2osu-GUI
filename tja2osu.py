import os

def TimingPoint(off, command, goed, vol):
    offs = int(off)
    if command < 0:
        return f"{offs},{round(command,12)},4,1,0,{vol},0,{goed}\n"
    elif command > 0:
        return f"{offs},{round(command,12)},4,1,0,{vol},1,{goed}\n"
    
def don(off):
    return f"256,192,{off},1,0,0:0:0:0:\n"

def ka(off):
    return f"256,192,{off},1,2,0:0:0:0:\n"

def Bdon(off):
    return f"256,192,{off},1,4,0:0:0:0:\n"

def Bka(off):
    return f"256,192,{off},1,12,0:0:0:0:\n"

def slide(last, off, big=False):
    global ChangingPoints
    ren = range(len(ChangingPoints))
    r = len(ChangingPoints)
    if ChangingPoints[r-1][0] < last:
        beats = ChangingPoints[r-1][1]
        scr = ChangingPoints[r-1][2]
    else:
        for i in ren:
            if ChangingPoints[i][0] > last:
                beats = ChangingPoints[i-1][1]
                scr = ChangingPoints[i-1][2]
                break
            elif ChangingPoints[i][0] == last:
                beats = ChangingPoints[i][1]
                scr = ChangingPoints[i][2]
                break       
    curve = 100 * (off - last) * beats * 1.4 * scr / 60000
    curin = 256 + int(curve)
    laster = int(last)
    if big:
        return f"256,192,{laster},2,1,L|{curin}:192,1,{round(curve,12)}\n"
    else:
        return f"256,192,{laster},2,0,L|{curin}:192,1,{round(curve,12)}\n"

def spin(last, off):
    return f"256,192,{last},12,0,{off}\n"

def cleanlist(start:list, dat:list):
    ger = sorted(dat)
    seen = []
    sorted_list = [x for x in ger if x not in seen and not seen.append(x)]
    sorted_list.insert(0, data_s)
    return sorted_list

audio = "audio.mp3"
title = ""
version = ""
timec = 0.0
timep = 0.0
gogo = 0
bpm = 0
bpm_k = 0
shou = 0
offset = 0
off_k = 0
songvol = 100
measure = 4/4
changed = False
glock = False
crop = []
delay_list=[]
delay_list1=[]
lasted = 0
tear = 0
scroll = 1.0
get = ""
ChangingPoints = []
data_s = []

general_k = [
    "osu file format v14",
    "",
    "",
    "[General]",
    "AudioFilename: audio.mp3",
    "AudioLeadIn: 0",
    "PreviewTime: -1",
    "Countdown: 0",
    "SampleSet: Normal",
    "StackLeniency: 0.7",
    "Mode: 1",
    "LetterboxInBreaks: 0",
    "WidescreenStoryboard: 0",
    "",
    "[Editor]",
    "DistanceSpacing: 0.8", #15
    "BeatDivisor: 7",
    "GridSize: 32",
    "TimelineZoom: 1",
    "",
    "[Metadata]", #20
    "Title:", #21
    "TitleUnicode:", #22
    "Artist:", #23
    "ArtistUnicode:", #24
    "Creator:", #25
    "Version:", #26
    "Source:",
    "Tags:",
    "BeatmapID:0",
    "BeatmapSetID:-1",
    "",
    "[Difficulty]",
    "HPDrainRate:5",
    "CircleSize:5",
    "OverallDifficulty:7.5",
    "ApproachRate:5",
    "SliderMultiplier:1.4",
    "SliderTickRate:1",
    "",
    "[Events]",
    "//Background and Video events",
    "//Break Periods",
    "//Storyboard Layer 0 (Background)",
    "//Storyboard Layer 1 (Fail)",
    "//Storyboard Layer 2 (Pass)",
    "//Storyboard Layer 3 (Foreground)",
    "//Storyboard Layer 4 (Overlay)",
    "//Storyboard Sound Samples",
    ""
    ]
general = general_k
def convertio(filein, artist, creator, fileout):
    global title, general, data_s, ChangingPoints, general_k, crop, delay_list, delay_list1, get, timec, scroll, version, bpm_k, glock, timep, lasted, tear, bpm, shou, offset, off_k, changed, measure, songvol, gogo
    artist = artist
    creator = creator
    with open(filein)as inp:
        data = []
        data_k = []
        humen = []
        block = []
        line = inp.readline()
        while line:
            while line.rstrip() != "#START":
                block = line.split(":")
                if block[0] == "TITLE":
                    title = block[1].rstrip()
                elif block[0] == "BPM":
                    bpm = float(block[1].rstrip())
                    bpm_k = bpm
                    shou = 60000/bpm*4
                    timec = float(60000/bpm)
                    timep = timec
                elif block[0] == "OFFSET":
                    offset = -1000 * float(block[1].rstrip())
                    off_k = offset
                elif block[0] == "SONGVOL":
                    songvol = int(block[1].rstrip())
                elif block[0] == "COURSE":
                    if block[1].rstrip() == "Easy" or block[1].rstrip() == "0":
                        version = "Kantan"
                    elif block[1].rstrip() == "Normal" or block[1].rstrip() == "1":
                        version = "Futsuu"
                    elif block[1].rstrip() == "Hard" or block[1].rstrip() == "2":
                        version = "Muzukashii"
                    elif block[1].rstrip() == "Oni" or block[1].rstrip() == "3":
                        version = "Oni"
                    elif block[1].rstrip() == "Edit" or block[1].rstrip() == "4":
                        version = "Inner Oni"
                    else:
                        version = block[1].rstrip()
                line = inp.readline()
            ChangingPoints.append([offset, bpm, scroll])
            line = inp.readline()
            data_s=[offset, timep, gogo, songvol]
            while line.rstrip() != "#END":
                if line[0] == "#":
                    block = line.split(" ")
                    if block[0].rstrip() == "#BPMCHANGE":
                        if changed:
                            data_k.append([get.rstrip(","), offset, timep, gogo, songvol, bpm, scroll])
                            changed = False
                        else:
                            changed = True
                        glock = True
                        bpm = float(block[1].rstrip())
                        timep = float(60000/bpm)
                        shou = 60000/bpm*4*measure
                    elif block[0].rstrip() == "#GOGOSTART":
                        glock = True
                        gogo = 1
                    elif block[0].rstrip() == "#GOGOEND":
                        glock = True
                        gogo = 0
                    elif block[0].rstrip() == "#MEASURE":
                        try:
                            got = block[1].rstrip().split("/")
                            measure = int(got[0])/int(got[1])
                            shou = 60000/bpm*4*measure
                        except:
                            measure = 4/4
                            shou = 60000/bpm*4*measure
                    elif block[0].rstrip() == "#SCROLL":
                        if changed:
                            data_k.append([get.rstrip(","), offset, timep, gogo, songvol, bpm, scroll])
                            changed = False
                        else:
                            changed = True
                        glock = True
                        scroll = float(block[1].rstrip())
                        timep = -1 * 100 / float(block[1].rstrip())
                    elif block[0].rstrip() == "#DELAY":
                        delay_list.append(int(offset))
                        delay_list1.append(1000*float(block[1].rstrip()))
                        offset += 1000*float(block[1].rstrip())
                elif line.startswith("//") is False:
                    if glock:
                        data_k.append([get.rstrip(","), offset, timep, gogo, songvol, bpm, scroll])
                        changed = False
                        glock = False
                    if line.rstrip("\n") == ",":
                        line = "0,"
                    get += line.rstrip("\n")
                    cot = line.rstrip("\n")
                    if get.endswith(","):
                        humen.append
                        tem = len(get.rstrip(","))
                        if data_k != []:
                            for i in data_k:
                                trans = i[1] + shou * len(i[0]) / tem
                                data.append([trans, i[2], i[3], i[4]])
                                if ChangingPoints[-1][0] == trans:
                                    ChangingPoints = ChangingPoints[:-1]
                                ChangingPoints.append([trans, i[5], i[6]])
                        yerd = offset
                        for i in get.rstrip(","):
                            if int(yerd) in delay_list:
                                yerd += delay_list1[delay_list.index(int(yerd))]
                            humen.append([yerd, i])
                            yerd += shou / tem
                        offset += shou
                        delay_list = []
                        delay_list1 = []
                        get = ""
                        data_k = []
                line = inp.readline()
            data = cleanlist(data_s, data)
            if os.path.exists(os.path.join(fileout, f"{artist} - {title}({creator})[{version}].osu")):
                os.remove(os.path.join(fileout, f"{artist} - {title}({creator})[{version}].osu"))
            with open(os.path.join(fileout, f"{artist} - {title}({creator})[{version}].osu"), mode = "a+", encoding = "utf-8") as output:
                general[21] += title
                general[22] += title
                general[23] += artist
                general[24] += artist
                general[25] += creator
                general[26] += version
                for i in general:
                    output.write(i+"\n")
                general[21] = "Title:"
                general[22] = "TitleUnicode:"
                general[23] = "Artist:"
                general[24] = "ArtistUnicode:"
                general[25] = "Creator:"
                general[26] = "Version:"
                output.write("[TimingPoints]\n")
                for i in data:
                    drx = TimingPoint(i[0],i[1],i[2],i[3])
                    output.write(drx)
                output.write("\n\n[HitObjects]\n")
                while humen != []:
                    i = humen.pop(0)
                    fret = ""
                    off = i[0]
                    tare = int(i[1])
                    if tare == 1:
                        fret = don(int(off))
                    elif tare == 2:
                        fret = ka(int(off))
                    elif tare == 3:
                        fret = Bdon(int(off))
                    elif tare == 4:
                        fret = Bka(int(off))
                    elif tare == 5:
                        lasted = off
                        tear = 1
                    elif tare == 6:
                        lasted = off
                        tear = 3
                    elif tare in (7, 9):
                        lasted = off
                        tear = 2
                    elif tare == 8:
                        if tear == 1:
                            fret = slide(lasted,off)
                        elif tear == 3:
                            fret = slide(lasted,off,True)
                        elif tear == 2:
                            fret = spin(int(lasted),int(off))
                        lasted= 0
                        tear = 0
                    if fret != "":
                        output.write(fret)
            offset = off_k
            bpm = bpm_k
            shou = 60000/bpm*4
            timep = timec
            ChangePoints = []
            data = []
            line = inp.readline()
