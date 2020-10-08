# Changelog

## 1.0.0 (27/07/2020)

- Initial version

## 1.0.1 (28/07/2020)

Bug fixes: 
- Added a margin to the elements of the AuthorTagList.vue component so they would not overlap if the column is too wide
- Added alphabetical sorting for the lists of publications in the KITOpenAnalytics and KITOpenMetrics pages
- Fixed the bug, that the metrics page counted all the duplicates

## 1.1.0 (28/07/2020)

Bug fixes:
- Changed the CSS in MultiSelect.vue so that the labels are now vertically centered
- Increased the timeout for the REST API GET call for the frontend, because big sets of publications took too long to 
be loaded (1s to 10s)

Features added:
- Added a third selection box to the metrics page, which can be used to select the publications by their POF structure
    - Also added a new column "Pof Structure" to the list view in the metrics page
    - Displaying metrics by POF as well
    
## 1.1.1 (29/07/2020)

Documentation:
- Extended the development section
- Wrote installation section
- Included README properly

## 1.1.2 (08/10/2020)

Documentation:
- Made Sphinxs autodoc to work
    - Fixed docstring formatting
- Docstrings pubs/util.py
- Docstrings pubs/models.py