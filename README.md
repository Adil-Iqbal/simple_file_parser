# Simple File Parser

## Description

Will search all files in a target directory tree to see if they contain user provided keywords. 
Then, matching files will be copied into output directories along with text file summarizing query results.


### Supported File Formats.

* PDF
* DOCX
* TXT

## Installation

Installation is done via the command line or terminal. Instruction are given for Windows environment. 

1. Go to desktop (or site where script is to be located)
2. Clone the repository.
3. Navigate into the repository.
4. (Optional) Create and activate a [virtual environment](https://towardsdatascience.com/why-you-should-use-a-virtual-environment-for-every-python-project-c17dab3b0fd0).
5. Install the requirements: `PyPDF2` and `docx2txt`

Without virtual environment.

```
cd "C:\\path\\to\\desktop"
git clone https://github.com/Adil-Iqbal/simple_file_parser.git
cd simple_file_parser
pip install PyPDF2 docx2txt
```

With virtual environment.

```
cd "C:\\path\\to\\desktop"
git clone https://github.com/Adil-Iqbal/simple_file_parser.git
cd simple_file_parser
python -m venv venv
./venv/Scripts/activate.bat
pip install PyPDF2 docx2txt
```

## Usage

### Summary
You can use the script via the command line. Run the script and pass in the target directory as the first argument. 

To be clear, the target directory will be the root of the search tree. 

### Detailed Instructions

Step 1. Navigate into the folder created during installation.

```
cd "C:\\path\\to\\desktop\\simple_file_parser"
```

Step 2. Run the `main.py` file with the directory to be searched as the first argument.

```
python main.py "C:\\path\\to\\target\\folder"
```

Step 3. You will then be prompted to provide a comma-separated list of keywords. The example below will search target directory 
for files that contain the words "foo", "bar", or "baz".

```
Enter comma-separated keywords: foo, bar, baz
```

Step 4. Query results will be printed in the command-line or terminal.

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
C:\path\to\target\folder\file03.txt
```

Step 5: The matched files will be copied to the **output directory** for your perusal. You can navigate there via the command-line 
using the absolute path. Or simply navigate there using the file explorer. Command-line method shown below.

**NOTE:** The **output directory** is on the second line of the printed information.

```
cd "C:\\path\\to\\desktop\\simple_file_parser\\query_20221213164423524" && Explorer .
```

The output directory will also contain a file named `__metadata.txt` that will contain the query results that were 
printed when the query first ran.

### All together now!

```
> cd "C:\\path\\to\\desktop\\simple_file_parser"
> python main.py "C:\\path\\to\\target\\folder"
> Enter comma-separated keywords: foo, bar, baz

Target Directory: C:\path\to\target\folder
Output Directory: C:\path\to\desktop\simple_file_parser\query_20221213164423524
Keywords: foo, bar, baz
Timestamp: 12-13-2022 16:44:23.524
Number of files in total: 9
Number of matches found: 3

 Files found:
C:\path\to\target\folder\file01.pdf
C:\path\to\target\folder\file02.docx
C:\path\to\target\folder\file03.txt

> cd "C:\\path\\to\\desktop\\simple_file_parser\\query_20221213164423524" && Explorer .
```


## Contact

If you need help, email **Adil Iqbal** at `main@adil-iqbal.com`


