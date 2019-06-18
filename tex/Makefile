.PHONY: run

run:
	pdflatex pscore_correlation.tex && bibtex pscore_correlation && pdflatex pscore_correlation.tex && tput reset

.PHONY: clean

clean:
	rm -f *.aux *.lof *.log *.lot *.out *.toc *.pdf *.ist *.blg
