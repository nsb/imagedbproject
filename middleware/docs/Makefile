DOC_DIR:=../
CATEGORY:=ip_addr_filter
TOP_DIR:= $(DOC_DIR)/docs

AUX_FILES=$(CATEGORY).aux $(CATEGORY).bbl $(CATEGORY).blg $(CATEGORY).dvi $(CATEGORY).log
DOC_FILES:=$(CATEGORY).ps $(CATEGORY).pdf $(CATEGORY).rtf $(CATEGORY)/$(CATEGORY).html $(CATEGORY)_split/$(CATEGORY).html

all: $(CATEGORY).pdf

%.dvi: %.tex
	@echo Running LaTex for the first time
	latex $(CATEGORY) && echo "" && sleep 2
	@echo Running BibTex to find bibliographic entries
	bibtex $(CATEGORY) && echo "" && sleep 2
	@echo Running LaTex for the second time to fill in bibliographic entries
	latex $(CATEGORY) && echo "" && sleep 2
	@echo Running LaTex for the third time to fix references
	latex $(CATEGORY)

$(CATEGORY)/$(CATEGORY).html: $(CATEGORY).tex
	@echo Making single-page HTML
	rm -rf $(CATEGORY)
	latex2html -no_math -html_version 4.0,math,unicode,i18n,tables -mkdir -dir $(CATEGORY) -split 0 $(CATEGORY)

$(CATEGORY)_split/$(CATEGORY).html: $(CATEGORY).tex
	@echo Making multiple-pages HTML
	rm -rf $(CATEGORY)_split
	latex2html -no_math -html_version 4.0,math,unicode,i18n,tables -mkdir -dir $(CATEGORY)_split $(CATEGORY)

$(CATEGORY).pdf: $(CATEGORY).dvi
	@echo Making PDF
	dvipdf $(CATEGORY)

$(CATEGORY).ps: $(CATEGORY).dvi
	@echo Making Postscript
	dvips -o $(CATEGORY).ps $(CATEGORY)

$(CATEGORY).rtf: $(CATEGORY).tex
	@echo Making RTF
	latex2rtf $(CATEGORY)

docs: $(DOC_FILES) ;

clean:
	rm -rf $(AUX_FILES) $(DOC_FILES) $(CATEGORY) $(CATEGORY)_split

realclean: clean
	rm -f *~
