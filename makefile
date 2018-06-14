test:
	make install
	py.test -s ABXpy/test

install:
	python ABXpy/distances/metrics/install/install_dtw.py
	python setup.py build
	python setup.py install

clean:
	find . -name '*.pyc' -delete
	find . -name '*.so' -delete

conda:
	rm -rf outputdir
	conda build --output-folder outputdir -n .
	conda convert --platform all outputdir/linux-64/*.tar.bz2 -o outputdir/
	for dfile in outputdir/*/*.tar.bz2; do \
		anaconda upload --force -u primatelang $$dfile; \
	done
	    

