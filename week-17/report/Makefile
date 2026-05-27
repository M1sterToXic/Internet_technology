all:
	xelatex -interaction=nonstopmode 0_main.tex
	biber 0_main
	xelatex -interaction=nonstopmode 0_main.tex
	xelatex -interaction=nonstopmode 0_main.tex

clean:
	rm -f *.aux *.log *.out *.toc *.bbl *.bcf *.blg *.xml *.pdf *.pdf.tmp
