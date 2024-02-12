# DCF
Discounted Cash Flow with Python

This repository is a learning effort to use python to read financial statements and parse the data as inputs to a dcf valuation of a stock's intrinsic value.

Financial statements sourced from Financial Modeling Prep

## 20211008 - 
set up virtual environment for DCF project (ignore venv)

## 20240212

Over time using Financial Modeling Prep data I found elements that FMP did not have.  I inquired as to whether or not they intended to add these items.  They answered that future versions of their data would contain these items.

Additionally, I found errors in their data when comparing to official 10Q and 10K reports as reported on SEC/EDGAR.  I pointed out that these errors existed.  FMP asked me to furnish some additional data to them which I did.  FMP stated that they wouel pass this on to their developers and get back to me.  Over 1 year later, no feedback and the data errors still exist.  

For these reasons, I felt that I could no longer trust FMP or their data.  I have since researched several other data sources.  Some were way too expensive (Morningstar) or did not have an active API that I could use in my programs (GURUFocus).  I finally found Alpha Vantage and settled on them to be my data source.

This repository is now ened.  No further updates will be made to it.
