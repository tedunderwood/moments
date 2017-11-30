moments
=======

Code and data used to investigate duration in narrative, supporting Ted Underwood, "Why Is Literary Time Measured in Minutes?" (forthcoming in *ELH*). Data for this project was also gathered by Sabrina Lee and Jessica Mercado.

I have aimed to make calculations fully reproducible by people who are comfortable with Python and R. Readers who don't program could still inspect intermediate stages of analysis using a spreadheet. (You would probably start with [averagetimes.csv.](https://github.com/tedunderwood/moments/blob/master/averagetimes.csv)) The scripts in this repository require Python 3; they were written in Python 3.5. Visualizations were produced using R version 3.3.3.

parsetime2.py
------------
This script parses the raw results in order to produce **segleveldata** and **averagetimes**. If you're interested in reproducing the calculations in the article, running this is the first step. You could also edit the script to aggregate results differently.

[**rplots**](https://github.com/tedunderwood/moments/tree/master/rplots)
------------
Scripts used to produce the illustrations in the essay. Running these scripts would be the second stage in reproducing my results.

tagnovels3.py
-------------
The script we originally used to tag novels, turning a text into a json object containing passages plus the reader's annotations about time. This script is provided to document the research process, but I haven't aimed to make it executable , since it depends on data sources not provided in this repository (the original texts of books, some under copyright).

/results
---------
The passages annotated by Lee, Mercado, and Underwood are stored here as json objects.
Earlier versions of some of these are contained in /rawsources
underwoodresults was produced by rectifying some omissions in /rawsources/underwoodtimedata.json
mercadomerged.json was produced by merging mercadopassages2.json and mercadopassages3.json

segleveldata.csv
----------------
Figures for individual passages.

averagetimes.csv
----------------
Figures for whole volumes; different columns (meantime and weightedavg) contain different ways of weighting the sixteen individual passages that compose a volume. The column "col" (color) represents the reader who annotated the book and/or, in the case of biography, genre. No, it is not best practice to use a column in two ways at once like this. :) 

