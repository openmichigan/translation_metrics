##open.michigan translation metrics

This is a set of scripts to work with the [Amara](http://amara.org) [API](http://amara.readthedocs.org/en/latest/api.html#api-endpoint) and other web scraping tools, with a goal of gathering metrics on the [video subtitle translation efforts](http://open.umich.edu/connect/projects#translation) that [Open.Michigan](http://open.umich.edu) has been involved in.

##what you have

Two Python scripts: ``` amara_vids.py ``` and ``` amara_langs.py ``` are included, and a text file, ``` iana_subtag_registry.txt ```.

##what you need

You will need an Amara.org account, and Python 2.7 installed on your computer.

(In order to run this script in Python 3, one need only change string syntax.)

To use, you will need to create a file called ``` api_key.py ```, and put in it one line:

``` amara_api_key = "" ```

Then go to [this page](http://www.amara.org/en/auth/login/?next=/en/profiles/edit/), log in, and [get your own API key](http://amara.readthedocs.org/en/latest/api.html), and copy it within the quotes in that file.

You will need Python installed on your machine, and you will need to install (via PyPi, ``` pip install ``` ) the following dependencies:

 - requests
 - BeautifulSoup4

If you are not installing these packages within a virtual environment, you will need to install them as root, i.e. ``` sudo pip install requests ```, for example.

All other package dependencies are included with the Python standard library.

##how to use

If you wish to get all **Open.Michigan** translations, you can ``` cd ``` to the directory to which you've cloned this repository, and run ``` python amara_langs.py ``` without any arguments. 
The total aggregate information about Open.Michigan subtitle translations will be printed to the console, and two files will be created:

- ``` amara_info_[date and time].csv ```, which is a tab-delimited file that includes aggregate information about the Open.Michigan video subtitle translations
- ``` video_ids_langs_[date and time].csv ```, which is a comma-delimited file that includes all Amara video IDs and the corresponding languages in which there is a subtitle track

_If you provide an argument to the command line_ run of the program, e.g. ``` python amara_langs.py othertestaccountname ```, the program will do the same thing, but for all the videos belonging to the account **othertestaccountname**, and _not_ the Open.Michigan videos.

If you wish to inspect an individual video on the Amara website, the URL format is: ```  http://amara.org/en/videos/<video_ID>/ ```. (e.g. ```  http://amara.org/en/videos/mTDSCV3CAxHY/ ```)

##license

All code in the **translation_metrics** repository, unless otherwise noted, is licensed under the [MIT License](http://opensource.org/licenses/MIT), Copyright &copy; 2014 Regents of the University of Michigan.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

