LATEX=pdflatex
BIBTEX=bibtex
STEM=best-practices-scientific-computing-2012

all : ${STEM}.pdf

${STEM}.pdf : ${STEM}.tex ${STEM}.bib
	${LATEX} ${STEM}
	${BIBTEX} ${STEM}
	${LATEX} ${STEM}
	${LATEX} ${STEM}

clean :
	@rm -f temp.tex *~ *.aux *.bbl *.blg *.log *.svn *.toc
