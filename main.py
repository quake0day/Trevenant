import os
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

i = 0
j = 0
number = 0
def addTemplate(entrie):
    global i
    global number
    final_string = ""
    try:
        author = entrie['author']
        author = author.replace('\n','').replace('\r','')
        name = entrie['title']
        entrie_type = ""
        if 'journal' in entrie:
            place = entrie['journal']
            entrie_type = 'journal'
        elif 'booktitle' in entrie:
            place = entrie['booktitle']
            entrie_type = 'conf'
        elif entrie['type'] == 'book':
            place = entrie['publisher']
            entrie_type = 'book'
        else:
            place = ""
        if 'year' in entrie:
            year = entrie['year']
        else:
            year = ""
        # For DEBUG ONLY
        # year = entrie['year']
        number += 1
        link = "./bib/" + str(number) + ".bib"
        final_string = "* <author>"+author+"</author>,"+" <name>\""+name+"\",</name>"+" <place>"+place+",</place> "+"<year>"+year+"</year> [[cite]("+link+")]\n\r"
    except Exception, e:
        i+= 1
        print e
        print entrie
        pass

    return final_string,[year,entrie_type,entrie,number]



def print_year_template(target_year, md_data):
    global j
    has_journal = 1
    has_conference = 1
    has_book = 1
    """
        <div class="panel panel-primary">
    <div class="panel-heading">2014:</div>
    <div class="panel-body">
    """
    markdown_string = " <div class=\"panel panel-primary\">"
    markdown_string += "<div class=\"panel-heading\">"
    markdown_string += "<year_title>"+str(target_year)+"</year_title>:"
    markdown_string += "</div> <div class=\"panel-body\"> \n\r"
    # Check if journal exists
    for res,[year,entrie_type,entrie,number] in md_data.iteritems():
        if str(target_year) == str(year):
            if entrie_type == 'journal':
                has_journal = 0
            elif entrie_type == 'conf':
                has_conference = 0
            elif entrie_type == 'book':
                has_book = 0
            else:
                pass
    if has_journal == 0:
        markdown_string += "###Journal:\n\r"
        markdown_string += "---\n\r"
        for res,[year,entrie_type,entrie,number] in md_data.iteritems():
            if entrie_type == 'journal':
                if str(target_year) == str(year):
                    markdown_string += res
                    j+=1
    if has_conference == 0:
        markdown_string += "###Conference:\n\r"
        markdown_string += "---\n\r"
        for res,[year,entrie_type,entrie,number] in md_data.iteritems():
            if entrie_type == 'conf':
                if str(target_year) == str(year):
                    markdown_string += res
                    j+=1
    if has_book == 0:
        markdown_string += "###Book Chapters:\n\r"
        markdown_string += "---\n\r"
        for res,[year,entrie_type,entrie,number] in md_data.iteritems():
            if entrie_type == 'book':
                if str(target_year) == str(year):
                    markdown_string += res
                    j+=1
    markdown_string += "</div></div>"
    return markdown_string

def createBibLink(entire, number):
    try:
        db = BibDatabase()
        db.entries = [entrie]
        writer = BibTexWriter()
        path = "./bib/"
        if not os.path.exists(path):
            os.makedirs(path)
        name = path+str(number)+".bib"
        with open(name,'w') as bibfile:
            bibfile.write(writer.write(db))
    except Exception,e:
        print "ALERT: The bib file cotains the following error!! Please Fix it NOW!"
        print entrie
        print str(e)
        pass




if __name__ == "__main__":
    with open('main.bib') as bibtex_file:
        bibtex_str = bibtex_file.read()
    bib_database = bibtexparser.loads(bibtex_str)

    md_data = {}
    for item in bib_database.entries:
        final, [year,entrie_type,entrie,number] = addTemplate(item)
        if year != "":
            md_data[final] = [year,entrie_type,entrie,number]

    for res,[year,entrie_type,entrie,number] in md_data.iteritems():
        createBibLink(entrie,number)

    if not os.path.exists('./info'):
        os.makedirs('./info')

    with open('./info/publication.md','w') as markdown_file:
        md_string = ""
        for year in xrange(2015,2007,-1):
            md_string += print_year_template(year,md_data)
        md_string = md_string.encode('UTF-8') 
        markdown_file.write(md_string)

    print "DONE!"
    print "Processed",j,"bib items. ",i," invalid bib items cannot be processed."
    if i > 0:
        print "Please check your main.bib file"