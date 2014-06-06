PY=python
PELICAN=TZ=UTC pelican
PELICANOPTS=-q

BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/../edmonds.github.io
CONFFILE=$(BASEDIR)/config/pelicanconf.py

html:
	@$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)
	@echo "blog.mycre.ws" > $(OUTPUTDIR)/CNAME

clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)

.PHONY: html clean
