# Trevenant
Automatic bibtext file to markdown converter (for UbiSeC Lab webpage update) 


![project logo](http://i.v2ex.co/K5s7K30ql.jpeg)

#Usage:
Install bibtexparser through pip

```
 pip install bibtexparser
```

Make sure the bibtex file is in the same folder and named `main.bib`

Execute the script

```
	python main.py
```

It will generate a folder and a markdown file named `info/publication.md` and a folder named `bib`.
Copy both of them to our lab website directory, replace the old file. 

Done.