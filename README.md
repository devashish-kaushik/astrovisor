# astrovisor
Inter IIT 2021 : ISRO PS - Catalogue visualization


A description of the files included here

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
A set of preprocessed files, that go directly into the application for visualisation, and comparing. They are obtained from the original catalogs and underwent simple preprocessing which appended a list of related publications to the objects they referred to. They are as follows:
1. AstroSat_final_table1.csv
2. hmxbFull.csv
3. lmxbFull.csv
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
A set of notebook describing the preprocessing steps in detail
1. DataPreprocessing.ipynb (for linking objects and references in catalog A)
2. Data Preprocessing of Astrosat Publications.ipynb
3. Data Preprocessing of Astrosat Observations.ipynb
4. Linking AstroSat Publications to AstroSat Observations.ipynb
(2-4 deal with mergin catalogs B and C suitably)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
The actual applications include
1. CatalogVisualisationAndSearchTool.ipynb (can be launched in a web browser with steps described in attached documentation 'Documentation-CatalogVisualisationAndSearchTool.pdf')
2. Documentation-CatalogVisualisationAndSearchTool.pdf (The documentation and instructions for usage for above)
3. main.py (Standalone desktop application. The 'AstroSat_final_table1.csv' needs to be in the same directory as the .py file. The coordinates, RA and Dec on the screen are in degrees, and 0 degrees and 360 are the same on the map)
4. Documentation for the Standalone Application (1).pdf (documentation for the same)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
The analysis files (for analysis of X ray data from Chandra) include:
1. CatalogVisualisationAndSearchToolWebAppDemo.mp4 
2. StandaloneAppDemo.mp4
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
