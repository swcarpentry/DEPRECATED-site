SCLL=software-carpentry-lessons-learned

all : ${SCLL}.html ${SCLL}.pdf

${SCLL}.html : ${SCLL}.md
	${CONVERT} < $< > $@

${SCLL}.pdf : ${SCLL}.tex ${SCLL}.bib
	pdflatex ${SCLL}
	bibtex ${SCLL}
	pdflatex ${SCLL}
	pdflatex ${SCLL}

clean :
	@rm -f ${SCLL}.html ${SCLL}.aux ${SCLL}.log ${SCLL}.out ${SCLL}.pdf *~
