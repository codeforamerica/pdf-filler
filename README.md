# pdfhook

[![Build Status](https://travis-ci.org/codeforamerica/pdfhook.svg?branch=master)](https://travis-ci.org/codeforamerica/pdfhook)

A Python web application for converting PDF forms into PDF-filling APIs.

You post an interactive PDF form, and the app will return a URL. If you post JSONs to that URL, the app will return the PDF and use the JSON to fill the form fields.



### Status

This code repository is currently a non-functional shell. Code will be added soon to make this a semi-functional prototype. The app needs further tests in order to become a fully-functional prototype which can fill all types of PDF fields.

### Why

This app idea originated from a common need to automatically fill PDF forms in various Code for America projects. Filling PDFs is an all-too-common need for many government and institutional services, and automatically populating forms can be a useful step in redesigning those services to better serve clients.

After [an initial proof-of-concept in another project](https://github.com/codeforamerica/typeseam/pull/25), I decided to spin this off into a separate code app.

### Who

This was made by @bengolder at @CodeForAmerica, with guidance and knowledge gleaned from many others. Hopefully you will help make it too!

## How to use it

### Dependencies

This is a Python app written using Flask.
Currently it depends on too many Python libraries and unnecessarily depends on PostgreSQL.

This application depends on a command line utility called [`pdftk` server](https://www.pdflabs.com/docs/pdftk-man-page/),  by [PDF Labs](https://www.pdflabs.com/), offered under a [GPL License](https://www.pdflabs.com/docs/pdftk-license/).

### Installation

If you are running OS X El Capitan install pdftk server here: https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/pdftk_server-2.02-mac_osx-10.11-setup.pkg

    git clone https://github.com/codeforamerica/pdfhook.git
    cd pdfhook
    Install homebrew: http://brew.sh/
    install python3.5: $ brew install python 3
    check that it's installed $ python3 --version
    python3.5 -m venv .
    source bin/activate
    Install postgres: http://postgresapp.com/
    Add postgres to path: $ export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/9.4/bin
    make install

### Running

    make run

### Deployment
