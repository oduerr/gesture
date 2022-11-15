This project uses markdown see https://quarto.org/ for more info. 

# How to create webpages from R (qmd)

In this directory is a file called `_quarto.yml` with the content:

```
output-dir: ../../docs/
```

This means that calling  in Terminal
```
  quarto render 
```
within this directory `R/to_docs` will render all `*.qmd` files into `../../docs/` as html. In github the github_page directory is set to `docs/`. Included is also an empty file `.nojekyll` which allows to serve the "raw"html files.

# How top render into pdf (and other format)
Just call in the Terminal
```
  quarto render --to pdf # Renders all files
  quarto render Note_on_Quaternion.qmd --to pdf  #Renders the single file 
  quarto render Note_on_Quaternion.qmd --to docx #Renders the single file --> word
```
