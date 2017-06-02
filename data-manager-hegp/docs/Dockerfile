FROM data-manager

MAINTAINER William Digan william.digan@aphp.fr

RUN pip install --upgrade pip
RUN pip install sphinx
RUN pip install sphinx_rtd_theme
RUN apt-get update
RUN apt-get install -y texlive-latex-extra --fix-missing
RUN apt-get install -y texlive-lang-french
RUN apt-get install -y mercurial
#this tool is here to automatically generated an .rst files from a python pakage
WORKDIR /home

RUN hg clone https://bitbucket.org/etienned/sphinx-autopackage-script
WORKDIR /data

