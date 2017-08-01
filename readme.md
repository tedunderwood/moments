moments
=======

Code and data used to investigate duration in narrative, supporting Ted Underwood, "Why Is Literary Time Measured in Minutes?" Data for this project was also gathered by Sabrina Lee and Jessica Mercado.

tagnovels3.py
-------------
The script we actually used to tag novels, turning a text into a json object containing passages plus the reader's annotations about time.

/results
---------
The passages annotated by Lee, Mercado, and Underwood are stored here as json objects.
Earlier versions of some of these are contained in /rawsources
underwoodresults was produced by rectifying some omissions in /rawsources/underwoodtimedata.json
mercadomerged.json was produced by merging mercadopassages2.json and mercadopassages3.json

parsetime2.py
------------
This script parses the raw results in order to produce **segleveldata** and **averagetimes**.

segleveldata.csv
----------------
Figures for individual passages.

averagetimes.csv
----------------
Figures for whole volumes; different columns (meantime and weightedavg) contain different ways of weighting the sixteen individual passages that compose a volume. The column "col" (color) represents the reader who annotated the book and/or, in the case of biography, genre. No, it is not recommended to use a column two ways at once like this. :) 

results/
--------
Contains the jsons actually used for article.
