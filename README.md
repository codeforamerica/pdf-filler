# pdfhook

[![Build Status](https://travis-ci.org/codeforamerica/pdfhook.svg?branch=master)](https://travis-ci.org/codeforamerica/pdfhook) [![Coverage Status](https://coveralls.io/repos/github/codeforamerica/pdfhook/badge.svg?branch=master)](https://coveralls.io/github/codeforamerica/pdfhook?branch=master)

A Python web application for converting PDF forms into PDF-filling APIs.

You post an interactive PDF form, and the app will return a URL. If you post JSONs to that URL, the app will return the PDF and use the JSON to fill the form fields.


### Status

This app is **a prototype**. It is less than a month old. Don't use it in production.

* If you set up the project on your computer, you should be able to use it to fill pdf forms.
* It only supports a couple types of PDF form fields.
* The code base is only covered by a few integration tests.
* The app does not check for or properly handle a wide variety of errors that are likely to occur.
* It may be difficult to integrate this into an existing Flask project.

Here are the current priorities for development.

* [Improve the documentation](https://github.com/codeforamerica/pdfhook/issues/34).
* Support [the filling of most PDF field types](https://github.com/codeforamerica/pdfhook/issues/28).
* Increase test coverage to 100% with greater emphasis on unit tests.
* Make sure that [tests cover any reasonable use cases](https://github.com/codeforamerica/pdfhook/issues/26).


### Why

This app idea originated from a common need to automatically fill PDF forms in various Code for America projects. Filling PDFs is an all-too-common need for many government and institutional services, and automatically populating forms can be a useful step in redesigning those services to better serve clients.

After [an initial proof-of-concept in another project](https://github.com/codeforamerica/typeseam/pull/25), I decided to spin this off into a separate code app.

### Who

This was created by @bengolder at @CodeForAmerica with contributions from: @gauravmk, @zhoux10, @bhoeting, @samgensburg, @debrasol, and @joffemd

## How to use it

These instructions assume:
* You are using a unix-based operating system, such as OS X or Linux
* You are comfortable on [the command line](https://github.com/codeforamerica/howto/blob/master/Shell.md)
* Your computer has [essential build tools installed](https://github.com/codeforamerica/howto/blob/master/Build-Tools.md)
* You have [git installed and configured](https://help.github.com/articles/set-up-git/) on your command line.


### Dependencies

This is a [Python 3](https://docs.python.org/3/) app written using [Flask](http://flask.pocoo.org/). It assumes that you are installing it on a unix operating system. It has only been tested on Ubuntu 14.04 (via Travis CI) and OS X 10.11
Currently it depends on too many Python libraries.

This application depends on a command line utility called [`pdftk` server](https://www.pdflabs.com/docs/pdftk-man-page/),  by [PDF Labs](https://www.pdflabs.com/), offered under a [GPL License](https://www.pdflabs.com/docs/pdftk-license/).

### Installation

If you are running OS X El Capitan 10.11, download the pdftk server installer here (requires your password for installation):
https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/pdftk_server-2.02-mac_osx-10.11-setup.pkg

#### Install Python 3.4 or 3.5

If your computer does not have Python 3, you can install it on OS X using [Homebrew](http://brew.sh/) or by [downloading it from python.org](https://www.python.org/downloads/). Make sure that `python3` is available on your [`PATH`](http://superuser.com/questions/517894/what-is-the-unix-path-variable-and-how-do-i-add-to-it).

    brew install python3
    # check the version
    python3 --version


#### Quickstart

    git clone https://github.com/codeforamerica/pdfhook.git
    cd pdfhook
    python3.5 -m venv .  # create the virtual environment
    source bin/activate
    make install

### Setting up the database
    
    You do not need to set up a database, but you can create a custom one if you like. By default, the application will create and use an SQLite database. It only uses one database table. Upon the first request it checks if that table has been created. If not, it will create it before processing the request.
    
### Running the local server

    make run

Visit http://localhost:5000/ to see the demo page or any software of your choice to [post a PDF form to the same URL](https://github.com/codeforamerica/pdfhook/blob/master/tests/integration/test_sample_pdfhook.py#L42-L47).

### Tests

    make test
    # or if you'd like to run specific tests
    make test TEST_SCOPE=tests.integration.test_sample_pdfhook:TestPDFHook.test_fill_pdf

### Deployment

_Not yet implemented_
