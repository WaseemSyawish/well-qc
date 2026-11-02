# Well Production Data QC
A small project I made to practise checking production data for errors. I generate fake well data, break it on purpose, then check if my script finds every error I planted.

Files
generate_data.py makes clean data for 30 wells over 60 days (oil rate, water cut, wellhead pressure)
inject_errors.py adds errors to a copy of the data and saves a list of what it planted (injected_errors.csv)
qc.py looks for the errors and compares what it found to that list
Errors it checks
duplicate rows
-999 values
negative oil rates
wrong units (one well in m3/d instead of bbl/d)
missing days
How to run
pip install pandas numpy
python generate_data.py
python inject_errors.py
python qc.py
Result

It found all 105 planted errors.

Next

I want to add loading the data into a database (SQLite first) and a chart.

I made this to learn, with help from AI.
