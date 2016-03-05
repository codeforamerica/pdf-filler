# pdfhook

_put test coverage and build status here_

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

### Installation

Install pdftk here: https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/pdftk_server-2.02-mac_osx-10.11-setup.pkg

    git clone https://github.com/codeforamerica/pdfhook.git
    cd pdfhook
    python3.5 -m venv .
    source bin/activate
    make install

### Running

    make run

### Deployment




