all: conda

clean:
	python setup.py clean

dev:
	python setup.py develop 


conda:
	rm -rf outputdir
	conda build --output-folder outputdir -n .
	#conda convert --platform all outputdir/linux-64/*.tar.bz2 -o outputdir/
	for dfile in outputdir/*/*.tar.bz2; do \
		anaconda upload --force -u primatelang $$dfile; \
	done
	    

