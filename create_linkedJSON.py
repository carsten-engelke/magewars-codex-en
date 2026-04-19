import json
print("reading link titles...")
# add links for earch term (collected in item["title_link"] list) into item["text"] in the format of: <a href='?q=Term'>Term</a>
with open("db_en.json", encoding="UTF-8") as db:
    jsondb = json.load(db)
    linklist = list()
    for item in jsondb:
        for link in item["title_link"]:
            linklist.append(link)
    linklist.sort(key=len, reverse=True)
    #print(linklist)
    for item in jsondb:
        i = 0
        j = 0
        #print("todo:" + item["text"])
        for linktitle in linklist:
            splittext = item["text"].split(linktitle) #splitting text, removing Term 
            newtext = item["text"] # save text here, modify in newtext, save back later.
            echo = False
            #if item["title"] == "Schwarm":
            #    echo = True
            if len(splittext) > 1: # term was found
                i = 0
                if echo: print(" -> TERM found:" + linktitle)
                newtext = ""
                addTitlePrefix = False
                for text in splittext:
                    if echo: print("  -> " + text)
                    foundvalidlink = False
                    foundinvalidlink = False
                    if len(text) > 0:
                        if i == 0:
                            if item["text"].startswith(linktitle): # if text starts with Term -> Valid link it
                                foundvalidlink = True
                        else: # not first line
                            addTitlePrefix = True
                            if text.find("<a href") != -1: #found link beginning
                                if text.find("</a>") != -1: # found link beginning + end
                                    if text.find("'>") != .1: # found link beginning + middle + end
                                        if text.find("<a href") < text.find("</a>") and text.find("<a href") < text.find("'>"): # title is not inside link url
                                            foundvalidlink = True
                                            if echo: print("   FOUND BEGINNING + MIDDLE + END, -> BEG < MID < END")
                                    else: # found link beginning + end but no middle
                                        if text.find("<a href") < text.find("</a>"): # title is not inside link url
                                            foundvalidlink = True
                                            if echo: print("   FOUND BEGINNING + END, but no middle -> BEG < END")
                                else: # found link beginning but no end 
                                    if text.find("'>") != .1: # found link beginning and middle
                                        if text.find("<a href") < text.find("'>"): # title is not inside link url
                                            foundvalidlink = True
                                            if echo: print("   FOUND BEGINNING + MIDDLE -> BEG < MID")
                                    else: # found link beginning but no end and no middle
                                        foundvalidlink = True
                                        if echo: print("   FOUND BEGINNING, but no middle or end")
                            else: # found no link beginning (maybe it is in last text?
                                if text.find("'>") == -1 and text.find("</a>") == -1: # NO BEG NO MID NO END -> untouched text
                                    foundvalidlink = True
                                    if echo: print("   FOUND NO BEGINNING + NO MIDDLE + NO END")
                    if foundvalidlink:
                        if echo: print("  VALID LINK")
                        text = "<a href='?q=" + linktitle + "'>" + linktitle + "</a>" + text
                    else:
                        if echo: print("  INVALID LINK")
                        if addTitlePrefix: text = linktitle + text
                    newtext +=text
                    i+=1
                if echo: print("   -> FINALLY:" + item["text"] + " -> " + newtext)
            item["text"] = newtext # save back new text
    with open("autolinked-db_en.json", mode="w", encoding="UTF-8") as newdb:
        json.dump(sorted(jsondb, key=lambda x: x["title"]), newdb, indent=4, ensure_ascii=False)
print("Auto-linked database stored to: autolinked-db_en.json")
