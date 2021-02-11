# Changelog

## 1.0.0 (27.07.2020)

- Initial version

## 1.0.1 (28.07.2020)

Bug fixes: 
- Added a margin to the elements of the AuthorTagList.vue component so they would not overlap if the column is too wide
- Added alphabetical sorting for the lists of publications in the KITOpenAnalytics and KITOpenMetrics pages
- Fixed the bug, that the metrics page counted all the duplicates

## 1.1.0 (28.07.2020)

Bug fixes:
- Changed the CSS in MultiSelect.vue so that the labels are now vertically centered
- Increased the timeout for the REST API GET call for the frontend, because big sets of publications took too long to 
be loaded (1s to 10s)

Features added:
- Added a third selection box to the metrics page, which can be used to select the publications by their POF structure
    - Also added a new column "Pof Structure" to the list view in the metrics page
    - Displaying metrics by POF as well
    
## 1.1.1 (29.07.2020)

Documentation:
- Extended the development section
- Wrote installation section
- Included README properly

## 1.1.2 (10.08.2020)

Documentation:
- Made Sphinxs autodoc to work
    - Fixed docstring formatting
- Docstrings pubs/util.py
- Docstrings pubs/models.py

## 1.1.3 (12.10.2020)

Changed
- "install.sh", which is a better script to be used, when installing the 
pubtrack application on an entirely new system.
- Renamed "production.yaml" to "production.yml"

Documentation
- Updated the installation instructions

## 1.2.0 (11.02.2020)

Changed
- The date format in the changelog is now more readable
- The production version now no longer uses nginx to deliver static files, but the 
  django server instance directly. This is achieved by using the "WhiteNoise" package, 
  which provided improved static file handling. The decision to switch to WhiteNoise is 
  mainly to reduce complexity of the application, as two docker containers are easier to 
  manage than three.
- There was an interesting bug with the switch to whitenoise. It would throw a server error
  with "...Manifest file not found..." this was because whitenoise was only configured within the 
  Production environment and as it turns out, it is important to call the "manage.py collectstatic" 
  with the option to define the appropriate configuration! "manage.py collectstatic --configuration Production"

## TODO

Command LIne Interface:
- "build" script: A script which will attempt to build the necessary docker containers
- "export" script: Generate a single folder which contains the contents of the database. This
  will have to be imported again somewhere else
- "import" script: Import the database content from a previously exported folder
- "up" script: Start the container
- "config" script: Configure important variables and environments

Documentation:
- Proper installation with pip