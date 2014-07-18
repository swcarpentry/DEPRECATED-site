PAPER=wssspe2014-assessment

all : ${PAPER}.pdf

${PAPER}.pdf : ${PAPER}.tex ${PAPER}.bib
	pdflatex ${PAPER}
	bibtex ${PAPER}
	pdflatex ${PAPER}
	pdflatex ${PAPER}

clean :
	@rm -f ${PAPER}.html *.aux *.bbl *.blg *.log *.out *.pdf *~
