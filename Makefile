# This Makefile implements common tasks needed by developers
# A list of implemented rules can be obtained by the command "make help"

.DEFAULT_GOAL=run
.PHONY .SILENT : help
help :
	echo
	echo "    Implemented targets:"
	echo
	echo "    check        use nosetests to test pypmc with python 2.7 and 3"
	echo "    checkX       use nosetests to test pypmc with python 2.7 or 3,"
	echo "                 where X is one of {2,3}"
	echo "    clean        delete compiled and temporary files"
	echo "    coverage     produce and show a code coverage report"
	echo "    help         show this message"
	echo "    run          play Gomoku"
	echo "    show-todos   show todo marks in the source code"
	echo

.PHONY : run
run : check
	./game.py

.PHONY : clean
clean:
	#remove build doc
	rm -rf ./doc/_build

	#remove .pyc files created by python 2.7
	rm -f ./*.pyc
	find -P . -name '*.pyc' -delete

	#remove .pyc files crated by python 3
	rm -rf ./__pycache__
	find -P . -name __pycache__ -delete

	#remove build folder in root directory
	rm -rf ./build

	#remove cythonized C source and object files
	find -P . -name '*.c' -delete

	#remove variational binaries only if command line argument specified
	find -P . -name '*.so' -delete

	#remove backup files
	find -P . -name '*~' -delete

	#remove files created by coverage
	rm -f .coverage
	rm -rf coverage

	# remove egg info
	rm -rf pypmc.egg-info

	# remove downloaded seutptools
	rm -f setuptools-3.3.zip

	# remove dist/
	rm -rf dist

.PHONY : check
check : check2 check3

.PHONY : check2
check2 :
	@ # run tests
	nosetests-2.7 --processes=-1 --process-timeout=60

	# run tests in parallel
	mpirun -n 2 nosetests-2.7

.PHONY : check3
check3 :
	@ # run tests
	nosetests3 --processes=-1 --process-timeout=60

	# run tests in parallel
	mpirun -n 2 nosetests3

.PHONY : check-fast
check-fast : build
	nosetests-2.7 -a '!slow' --processes=-1 --process-timeout=60
	nosetests3    -a '!slow' --processes=-1 --process-timeout=60

.PHONY : show-todos
grep_cmd = ack-grep -i --no-html --no-cc --no-make [^"au""sphinx.ext."]todo
begin_red = "\033[0;31m"
end_red   = "\033[0m"
show-todos :
	@ # suppress errors here
	@ # note that no todo found is considered as error
	$(grep_cmd) . ; \
	echo ; 	echo ; \
	echo $(begin_red)"********************************************************"$(end_red) ; \
	echo $(begin_red)"* The following file types are NOT searched for TODOs: *"$(end_red) ; \
	echo $(begin_red)"* o c source                                           *"$(end_red) ; \
	echo $(begin_red)"* o html source                                        *"$(end_red) ; \
	echo $(begin_red)"* o makefiles                                          *"$(end_red) ; \
	echo $(begin_red)"********************************************************"$(end_red) ; \
	echo

.PHONY : coverage
coverage : .build-system-default
	rm -rf coverage
	nosetests --with-coverage --cover-package=pypmc --cover-html --cover-html-dir=coverage
	xdg-open coverage/index.html
