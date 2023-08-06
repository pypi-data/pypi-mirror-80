# Copyright Canonical Ltd.  This software is licensed under the GNU
# Affero General Public License version 3 (see the file LICENSE).

PYTHON = python
PYDOC = pydoc

all: gettextpo.so gettextpo.html

check: all
	$(PYTHON) test_gettextpo.py -v

clean:
	rm -rf build dist gettextpo*.so gettextpo.html

gettextpo.so: setup.py gettextpo.c
	$(PYTHON) setup.py build_ext -i

gettextpo.html: gettextpo.so
	$(PYDOC) -w gettextpo



.PHONY: all check clean

