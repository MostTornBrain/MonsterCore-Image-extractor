"""
Extract all the monster images from the Monster Core pdf so that can be matched
with other external data, such as Obsidian notes, or used as tokens in Foundry.

This assumes you have a purchased copy of the PDF from Paizo, which can be 
purchased here:   https://paizo.com/products/btq02ex5?Pathfinder-Monster-Core

Please support Paizo's work!

-------------------------------------------------------------------------------
NOTE:
This is heavily based on https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/examples/extract-images/extract-from-pages.py
License: GNU GPL V3
(c) 2018 Jorj X. McKie
-------------------------------------------------------------------------------

Prerequisites
-------------
This requires PyMuPDF, version 1.18.18 or later.  (python3 -m pip install PyMuPDF)


Usage
-----
python3 monster-images.py input.pdf

Description
-----------
This script will extract all the monster images from the Monster Core PDF and save them
as individual png images into the folder "MonsterCoreImages/".  The extracted images will be 
cross-referenced with the supplied MonsterCore.csv file to generate the proper file names for
each monster as used in Foundry.

The PDF xref numbers are accurate for the current initially released Monster Core PDF as of
March 2024.  This csv file name need updates in the future is the PDF is ever revised by Paizo.
"""

import os
import sys
import time
import csv

import fitz

csv_file_path = 'MonsterCore.csv'
monsterMap = {}

# Load the Monster Core xref list so we know what images to save
with open(csv_file_path, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        monsterMap[row[0]] = row[1]

print(fitz.__doc__)

if not tuple(map(int, fitz.version[0].split("."))) >= (1, 18, 18):
    raise SystemExit("require PyMuPDF v1.18.18+")

dimlimit = 0  # 100  # each image side must be greater than this
relsize = 0  # 0.05  # image : image size ratio must be larger than this (5%)
abssize = 0  # 2048  # absolute image size limit 2 KB: ignore if smaller
imgdir = "MonsterCoreImages"  # found images are stored in this subfolder

if not os.path.exists(imgdir):  # make subfolder if necessary
    os.mkdir(imgdir)


def recoverpix(doc, item):
    xref = item[0]  # xref of PDF image
    smask = item[1]  # xref of its /SMask

    # special case: /SMask or /Mask exists
    if smask > 0:
        pix0 = fitz.Pixmap(doc.extract_image(xref)["image"])
        if pix0.alpha:  # catch irregular situation
            pix0 = fitz.Pixmap(pix0, 0)  # remove alpha channel
        mask = fitz.Pixmap(doc.extract_image(smask)["image"])

        try:
            pix = fitz.Pixmap(pix0, mask)
        except:  # fallback to original base image in case of problems
            pix = fitz.Pixmap(doc.extract_image(xref)["image"])

        if pix0.n > 3:
            ext = "pam"
        else:
            ext = "png"

        return {  # create dictionary expected by caller
            "ext": ext,
            "colorspace": pix.colorspace.n,
            "image": pix.tobytes(ext),
        }

    # special case: /ColorSpace definition exists
    # to be sure, we convert these cases to RGB PNG images
    if "/ColorSpace" in doc.xref_object(xref, compressed=True):
        pix = fitz.Pixmap(doc, xref)
        pix = fitz.Pixmap(fitz.csRGB, pix)
        return {  # create dictionary expected by caller
            "ext": "png",
            "colorspace": 3,
            "image": pix.tobytes("png"),
        }
    return doc.extract_image(xref)


fname = sys.argv[1] if len(sys.argv) == 2 else None
if not fname:
    raise SystemExit("You must supply the filename of your Monster Core PDF!")

t0 = time.time()
doc = fitz.open(fname)

page_count = doc.page_count  # number of pages

xreflist = []
imglist = []
skipped = 0
for pno in range(page_count):
    print(
        "Extract Images",  # show our progress
        pno + 1,
        page_count,
        "*** Scanning Pages ***",
    )

    il = doc.get_page_images(pno)
    imglist.extend([x[0] for x in il])
    for img in il:
        # print("Image is: ", img)
        xref = img[0]
        if xref in xreflist:
            continue
        width = img[2]
        height = img[3]
        if min(width, height) <= dimlimit:
            continue
        image = recoverpix(doc, img)
        n = image["colorspace"]
        imgdata = image["image"]

        if len(imgdata) <= abssize:
            continue
        if len(imgdata) / (width * height * n) <= relsize:
            continue

        # imgfile = os.path.join(imgdir, "img%05i.%s" % (xref, image["ext"]))
        if (str(xref) in monsterMap) and monsterMap[str(xref)] != "":
            imgfile = os.path.join(imgdir, "%s.%s" % (monsterMap[str(xref)], image["ext"]))
            fout = open(imgfile, "wb")
            fout.write(imgdata)
            fout.close()
        else:
            print("Skipping ", xref)
            skipped += 1;
        xreflist.append(xref)

t1 = time.time()
imglist = list(set(imglist))
print(len(set(imglist)), "images in total")
print(skipped, "images skipped because they weren't monsters")
print(len(xreflist) - skipped, "images extracted")

print("total time %g sec" % (t1 - t0))