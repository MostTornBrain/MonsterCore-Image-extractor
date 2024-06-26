# MonsterCore-Image-extractor

Extract all the monster images from an owned copy of the Monster Core pdf so 
they can be matched with other external data, such as Obsidian notes, or used 
as tokens or portraits in Foundry.

This assumes you have a purchased copy of the Monster Core PDF from Paizo, which 
can be purchased here:   https://paizo.com/products/btq02ex5?Pathfinder-Monster-Core

Please support Paizo's work!

-------------------------------------------------------------------------------
NOTE:
This is heavily based on https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/examples/extract-images/extract-from-pages.py
License: GNU GPL V3
(c) 2018 Jorj X. McKie
-------------------------------------------------------------------------------

Prerequisites
-------------
This requires PyMuPDF, version 1.18.18 or later.  (install via `python3 -m pip install PyMuPDF`)


Usage
-----
`python3 monster-images.py input.pdf`

Description
-----------
This script will extract all the monster images from the Monster Core PDF and save them
as individual png images into the folder `pf2e-monster-core-pdf-mapping/MonsterCoreImages/`.  The extracted images will be 
cross-referenced with the supplied MonsterCore.csv file to generate the proper file names for
each monster as used in Foundry.

If you want to use the extracted images in Foundry, copy the complete `pf2e-monster-core-mapping` folder into your Foundry `data/modules` directory (**after** you run the image extraction script).  Then, when you launch your world, choose to enable the `PF2e Monster Core PDF Mapping` module.   All the Monster Core creatures from the PDF that had images should now have images in Foundry.

**NOTE:** The PDF xref numbers and names were transcribed by hand and are accurate for the current 
released Monster Core PDF as of March 2024.  This csv file may need updates in the future 
if the PDF is ever revised by Paizo.
