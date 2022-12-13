# Simple File Parser

#### Authors
Adil Iqbal, Sumiyyah Ahmed

### Installation

Installation is done via the command line or terminal. Instruction are given for Windows environment. 

1. Go to desktop (or site where script is to be located)
2. Clone the repository.
3. Navigate into the repository.
4. Start the virtual environment.
5. Install the requirements: `PyPDF2` and `docx2txt`

```
cd "C:\\path\\to\\desktop"
git clone ...
cd simple_file_parser
venv\Scripts\activate
pip install PyPDF2 docx2txt
```

### Usage

You can use the script via the command line. Run the script and pass in the target directory as the first argument. 

To be clear, the target directory is the directory that will be searched for the keywords provided.

```
python main.py "C:\\path\\to\\target\\folder"
```

You will then be prompted to provide a comma-sperated list of keywords. The example below will search target directory 
for DOCX and PDF files that contain the words "foo", "bar", or "baz".

```
Enter comma-separated keywords: foo, bar, baz
```

Query results will be printed in the command-line or terminal.

```
Target Directory: C:\path\to\target\folder
Output Directory: C:\path\to\desktop\simple_file_parser\query_20221213164423524
Keywords: foo, bar, baz
Timestamp: 12-13-2022 16:44:23.524
Number of files in total: 9
Number of matches found: 3

 Files found:
C:\path\to\target\folder\file01.pdf
C:\path\to\target\folder\file02.docx
C:\path\to\target\folder\file03.pdf
```

The matched files will be copied to the output directory for your perusal. You can navigate there via the command-line 
using the absolute path. Or simply navigate there using the file explorer. Command-line method shown below.

```
cd "C:\\path\\to\\desktop\\simple_file_parser\\query_20221213164423524" && Explorer .
```

The output directory will also contain a file named `__metadata.txt` that will contain the query results that were 
printed when the query first ran.

#### Caveat

If no target file path is provided when the script is run, the script 
will attempt to search in a directory called `input` at the same level as the script. 
This directory is likely to be empty unless you create and populate it.

#### Supported file formats.

* PDF
* DOCX
* TXT