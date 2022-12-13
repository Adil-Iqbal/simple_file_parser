import os
import re
import shutil
import sys
import traceback
import logging
import warnings
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Callable, Pattern

import PyPDF2
import docx2txt

# Ignore noise from third-party packages.
warnings.filterwarnings("ignore")
logging.getLogger("PyPDF2").setLevel(logging.ERROR)


def contains_kw(contents: str, kw_pattern: Pattern) -> bool:
    """Returns true if string contents contains keyword patter."""
    return re.search(kw_pattern, contents) is not None


def docx_contains_kw(file_path: Path, kw_pattern: Pattern) -> bool:
    """Return true if DOCX file at given path matches the keyword pattern."""
    text = docx2txt.process(str(file_path.absolute()))
    return contains_kw(text, kw_pattern)


def pdf_contains_kw(file_path: Path, kw_pattern: Pattern) -> bool:
    """Return true if PDF file at given path matches the keyword pattern."""
    with open(str(file_path), 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        for page_num in range(reader.numPages):
            text = reader.getPage(page_num).extract_text()
            if contains_kw(text, kw_pattern):
                return True
    return False


def txt_contains_kw(file_path: Path, kw_pattern: Pattern) -> bool:
    """Return true if TXT file at given path matches the keyword pattern."""
    with open(str(file_path), 'r', encoding='UTF8') as file:
        return contains_kw(file.read(), kw_pattern)


# Add file parsers to this dictionary to support other file types.
parsers: Dict[str, Callable[[Path, Pattern], bool]] = {
    "docx": docx_contains_kw,
    "pdf": pdf_contains_kw,
    "txt": txt_contains_kw
}


kw_sepr: Pattern[str] = re.compile(r"\s*,\s*")
query_dir_prefix: str = "query_"


@dataclass
class SearchResult:
    matches: List[Path] = field(default_factory=list)
    failed_to_parse: List[Path] = field(default_factory=list)
    failed_to_copy: List[Path] = field(default_factory=list)


@dataclass
class Query:
    timestamp: datetime
    target_dir: Path
    output_dir: Path
    keywords: Pattern
    files_count: int = 0
    result: SearchResult = field(default_factory=SearchResult)


def create_metadata_report(query: Query) -> str:
    """Create report with information related to query operation."""
    data = f"Target Directory: {str(query.target_dir)}"
    data += f"\nOutput Directory: {str(query.output_dir)}"
    data += f"\nKeywords: {str(query.keywords.pattern).replace('|', ', ')}"
    data += f"\nTimestamp: {query.timestamp.strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]}"
    data += f"\nNumber of files in total: {query.files_count}"
    data += f"\nNumber of matches found: {len(query.result.matches)}"

    if query.result.failed_to_parse:
        data += f"\n\n ** FOLLOWING MATCHES COULD NOT BE PARSED **"
        for file_path in query.result.failed_to_parse:
            data += f"\n{str(file_path)}"

    if query.result.failed_to_copy:
        data += f"\n\n ** FOLLOWING MATCHES COULD NOT BE COPIED **"
        for file_path in query.result.failed_to_copy:
            data += f"\n{str(file_path)}"

    if query.result.matches:
        data += f"\n\n Files found:"
        for file_path in query.result.matches:
            data += f"\n{str(file_path)}"
    else:
        data += "\n\nNo matches found."

    print(data)
    return data


def create_metadata(query: Query) -> None:
    """Save report in output directory."""
    data = create_metadata_report(query)
    meta_file_path = query.output_dir / "__metadata.txt"
    meta_file_path.write_text(data)


def copy_results(query: Query) -> None:
    """Copy files that match provided keywords into output directory."""
    for src_path in query.result.matches:
        dst_path = query.output_dir / os.path.basename(str(src_path))
        try:
            shutil.copy2(str(src_path), str(dst_path))
        except IOError:
            query.result.failed_to_copy.append(src_path)


def find_files_with_keywords(query: Query) -> None:
    """Perform search on target directory."""
    target_dir = str(query.target_dir)

    # Iterate over directory subtrees starting with target directory as root.
    for root, dirs, files in os.walk(target_dir):
        query.files_count += len(files)

        # Iterate over all files in this directory.
        for filename in files:
            _, file_ext = os.path.splitext(filename)
            file_path = Path(root) / filename

            # Ensure that appropriate parser exists for file type.
            if (file_ext := file_ext[1:]) not in parsers:
                query.result.failed_to_parse.append(file_path)
                continue

            # Attempt to parse file.
            try:
                contains_keywords = parsers[file_ext]
                if contains_keywords(file_path, query.keywords):
                    query.result.matches.append(file_path)

            # If failed to parse file, let user know.
            except Exception:
                traceback.print_exc()
                query.result.failed_to_parse.append(file_path)


def resolve_keywords() -> Pattern:
    """Return regular expression pattern from keywords provided by user."""
    user_input: str = input("Enter comma-separated keywords: ")
    keywords: List[str] = \
        [kw.strip().lower() for kw in user_input.split(',')]
    if len(keywords) == 0:
        raise ValueError("Keywords not recognized.")
    return re.compile("|".join(keywords))


def resolve_output_dir(timestamp: datetime) -> Path:
    """Return file path to the directory where search results are to be stored."""
    timestamp: str = timestamp.strftime("%Y%m%d%H%M%S%f")[:-3]
    parent_dir: Path = Path(__file__).parent.resolve()
    dirname: Path = parent_dir / f"{query_dir_prefix}{timestamp}"
    dirname.mkdir()
    return parent_dir / dirname


def resolve_target_dir() -> Path:
    """Return file path to the directory to be searched."""
    if len(sys.argv) > 1:
        target_dir = Path(sys.argv[1])
        if not target_dir.exists() or not target_dir.is_dir():
            raise ValueError("Path not recognized: " + str(target_dir))
        return target_dir
    raise ValueError("Path not provided! See `README.md` file for proper usage.")


def create_query() -> Query:
    """Create query object from user input."""
    timestamp: datetime = datetime.utcnow()
    return Query(
        timestamp=timestamp,
        target_dir=resolve_target_dir(),
        output_dir=resolve_output_dir(timestamp),
        keywords=resolve_keywords()
    )


def main() -> None:
    query = create_query()
    find_files_with_keywords(query)
    copy_results(query)
    create_metadata(query)



if __name__ == '__main__':
    main()
