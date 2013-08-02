LATEX=pdflatex
BIBTEX=bibtex
PNAS=best-practices-scientific-computing-2012

all : ${PNAS}.pdf

${PNAS}.pdf : ${PNAS}.tex ${PNAS}.bib
	${LATEX} ${PNAS}
	${BIBTEX} ${PNAS}
	${LATEX} ${PNAS}
	${LATEX} ${PNAS}

temp.pdf : temp.tex ${PNAS}.bib
	${LATEX} temp
	${BIBTEX} temp
	${LATEX} temp
	${LATEX} temp

temp.tex : ${PNAS}.tex
	sed \
	-e 's:documentclass.pnastwo.:documentclass{temp}:g' \
	-e 's:issuedate.Issue Date whatever.:issuedate{}:g' \
	-e 's:volume.Volume whatever.:volume{}:g' \
	-e 's:issuenumber.Issue Number whatever.:issuenumber{}:g' \
	< ${PNAS}.tex \
	> temp.tex

clean :
	@rm -f temp.tex *~ *.aux *.bbl *.blg *.log *.pdf *.svn *.toc
