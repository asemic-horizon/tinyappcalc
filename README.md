# tinyappcalc
## World's Tiniest Jackknife Population-Mean Bounds-Giver and Phone App


"Phone app" is meant as a joke. But the page does open on my mobile.

This started because my phone didn't have any apps that calculated [jackknife](http://en.wikipedia.org/wiki/Jackknife) distributions for simple averages, something I needed with small samples.

The project has two files

- `main.py` has the whole logic for calculating the jackknife and the resulting metrics. There is a dependence to scipy because I used kernel density estimates to compute a mode; that can be easily disabled. It also spins up FastAPI and offers a REST endpoint for this.

- `index.html` is a simple, broken html file with inline javascript that does the reading and writing.
