PY?=python3
PELICAN?=pelican
PELICANOPTS=

BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
CONFFILE=$(BASEDIR)/pelicanconf.py
PUBLISHCONF=$(BASEDIR)/publishconf.py

FTP_HOST=localhost
FTP_USER=anonymous
FTP_TARGET_DIR=/

SSH_HOST=localhost
SSH_PORT=22
SSH_USER=root
SSH_TARGET_DIR=/var/www

S3_BUCKET=my_s3_bucket

CLOUDFILES_USERNAME=my_rackspace_username
CLOUDFILES_API_KEY=my_rackspace_api_key
CLOUDFILES_CONTAINER=my_cloudfiles_container

DROPBOX_DIR=~/Dropbox/Public/

GITHUB_PAGES_BRANCH=gh-pages
GH_TOKEN = bpQmhqSMRWgKR+Eq75Sj0e4e1MBYUrujUVe2A5t5GqfYOlbDcfwLAwSyAfdDbzDif7Gp1HkBuCIOVGKefL5ZiWZn/5MJ1JHi0t+psJQLCcknT1xC2YK6TzP0LB1lfQoWB62TAZ4ftOC9UYHWrZC9gJXqBzjU0J6yx0dlCFH4V9pywncyQO4JidnkPSnel/kbwq87hDpPw9VMmPFV8UaDawnjKvtCWCxK2qfGXCRDujNYJAtTojscLRCuUAmyhxXTeDNWI29aTd36rUhMRfEbzMA/Fn2cFhz+yRmYvYFwDysy5bKWJy9iJmTFw1/s0CxAthQBDVTNZCOw6srTScRvRJ1sPP/8ddMMsuHUz+4Z9bf4b5ExYuuBP19Xxnnqdmrsc9D5jQ0BNnxpBmZ/tKIjMEbcjM9IPdh4tbQnKlWF6ibD8p6ulVflpIUP3IMeuXktfssVDSPI4f8IxT8TBfthXQ0YNoIToHyFoxg0rYmePhRd20n99B1RUMa5XI5OIoXczIpEY6VzP4/7HjjhFLchLimAJ6LtnqTUEe/9aq/MMnMdMYCSIiaAyJYh6c70/XAD+LGXI4yyx/JHjOOkznwRABXmIEjnrXre5ZgMVYGV6xKGxal1gG/LZa0Pji2Km4eygbWiobXH9h8+ObatoMp8Q7IYIU/9jLm08d5JLQRcqSs=

DEBUG ?= 0
ifeq ($(DEBUG), 1)
	PELICANOPTS += -D
endif

RELATIVE ?= 0
ifeq ($(RELATIVE), 1)
	PELICANOPTS += --relative-urls
endif

help:
	@echo 'Makefile for a pelican Web site                                           '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make html                           (re)generate the web site          '
	@echo '   make clean                          remove the generated files         '
	@echo '   make regenerate                     regenerate files upon modification '
	@echo '   make publish                        generate using production settings '
	@echo '   make serve [PORT=8000]              serve site at http://localhost:8000'
	@echo '   make serve-global [SERVER=0.0.0.0]  serve (as root) to $(SERVER):80    '
	@echo '   make devserver [PORT=8000]          start/restart develop_server.sh    '
	@echo '   make stopserver                     stop local server                  '
	@echo '   make ssh_upload                     upload the web site via SSH        '
	@echo '   make rsync_upload                   upload the web site via rsync+ssh  '
	@echo '   make dropbox_upload                 upload the web site via Dropbox    '
	@echo '   make ftp_upload                     upload the web site via FTP        '
	@echo '   make s3_upload                      upload the web site via S3         '
	@echo '   make cf_upload                      upload the web site via Cloud Files'
	@echo '   make github                         upload the web site via gh-pages   '
	@echo '                                                                          '
	@echo 'Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html   '
	@echo 'Set the RELATIVE variable to 1 to enable relative urls                    '
	@echo '                                                                          '

html:
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)

regenerate:
	$(PELICAN) -r $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

serve:
ifdef PORT
	cd $(OUTPUTDIR) && $(PY) -m pelican.server $(PORT)
else
	cd $(OUTPUTDIR) && $(PY) -m pelican.server
endif

serve-global:
ifdef SERVER
	cd $(OUTPUTDIR) && $(PY) -m pelican.server 80 $(SERVER)
else
	cd $(OUTPUTDIR) && $(PY) -m pelican.server 80 0.0.0.0
endif


devserver:
ifdef PORT
	$(BASEDIR)/develop_server.sh restart $(PORT)
else
	$(BASEDIR)/develop_server.sh restart
endif

stopserver:
	$(BASEDIR)/develop_server.sh stop
	@echo 'Stopped Pelican and SimpleHTTPServer processes running in background.'

publish:
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONF) $(PELICANOPTS)

ssh_upload: publish
	scp -P $(SSH_PORT) -r $(OUTPUTDIR)/* $(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR)

rsync_upload: publish
	rsync -e "ssh -p $(SSH_PORT)" -P -rvzc --delete $(OUTPUTDIR)/ $(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR) --cvs-exclude

dropbox_upload: publish
	cp -r $(OUTPUTDIR)/* $(DROPBOX_DIR)

ftp_upload: publish
	lftp ftp://$(FTP_USER)@$(FTP_HOST) -e "mirror -R $(OUTPUTDIR) $(FTP_TARGET_DIR) ; quit"

s3_upload: publish
	s3cmd sync $(OUTPUTDIR)/ s3://$(S3_BUCKET) --acl-public --delete-removed --guess-mime-type --no-mime-magic --no-preserve

cf_upload: publish
	cd $(OUTPUTDIR) && swift -v -A https://auth.api.rackspacecloud.com/v1.0 -U $(CLOUDFILES_USERNAME) -K $(CLOUDFILES_API_KEY) upload -c $(CLOUDFILES_CONTAINER) .

github: publish
	ghp-import -n $(OUTPUTDIR)
    git push -fq https://${GH_TOKEN}@github.com/KMBlog.git gh-pages > /dev/null

.PHONY: html help clean regenerate serve serve-global devserver stopserver publish ssh_upload rsync_upload dropbox_upload ftp_upload s3_upload cf_upload github
