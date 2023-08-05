# Yara Scanner

[![ace-ecosystem](https://circleci.com/gh/ace-ecosystem/yara_scanner.svg?style=svg)](https://circleci.com/gh/ace-ecosystem/yara_scanner)

A wrapper around the [yara-python](https://github.com/VirusTotal/yara-python) project the provides the following capabilities.

- Change tracking of yara files, directories of yara files, or git repositories of yara files.
- File and data scanning with the ability to filter based on meta data matching.
- Distributed scanning processes that maximize the use of multi-core systems.
- Command line interface.

## Python Examples

Loading a single yara file and then scanning data.

```python
from pprint import pprint
from yara_scanner import YaraScanner

scanner = YaraScanner()
# tells the scanner to start tracking this yara file
scanner.track_yara_file('my_rules.yar')
scanner.load_rules()
if scanner.scan('/path/to/scan_target.txt'):
   pprint(scanner.scan_results)
   
# this returns True if any tracked yara files have changed
if scanner.check_rules():
   scanner.load_rules()
```

## Installation Instructions

```bash
pip install yara-scanner
```

## Command Line Instructions

   ```
   usage: scan [-h] [-r] [--from-stdin] [--debug] [-j] [-t] [-y YARA_RULES]
               [-Y YARA_DIRS] [-G YARA_REPOS] [-c] [-b BLACKLISTED_RULES]
               [-B BLACKLISTED_RULES_PATH] [-d SIGNATURE_DIR]
               [PATHS [PATHS ...]]

   Scan the given file with yara using all available rulesets.

   positional arguments:
     PATHS                 One or more files or directories to scan with yara.

   optional arguments:
     -h, --help            show this help message and exit
     -r, --recursive       Recursively scan directories.
     --from-stdin          Read the list of files to scan from stdin.
     --debug               Log debug level messages.
     -j, --dump-json       Dump JSON details of matches. Otherwise just list the
                           rules that hit.
     -t, --test            Test each yara file separately against different types
                           of buffers for performance issues.
     -y YARA_RULES, --yara-rules YARA_RULES
                           One yara rule to load. You can specify more than one
                           of these.
     -Y YARA_DIRS, --yara-dirs YARA_DIRS
                           One directory containing yara rules to load. You can
                           specify more than one of these.
     -G YARA_REPOS, --yara-repos YARA_REPOS
                           One directory that is a git repository that contains
                           yara rules to load. You can specify more than one of
                           these.
     -c, --compile-only    Compile the rules and exit.
     -b BLACKLISTED_RULES, --blacklist BLACKLISTED_RULES
                           A rule to blacklist (remove from the results.) You can
                           specify more than one of these options.
     -B BLACKLISTED_RULES_PATH, --blacklist-path BLACKLISTED_RULES_PATH
                           Path to a file that contains a list of rules to
                           blacklist, one per line.
   ```

## Command Line Examples

scan a single file
   ```bash
   scan ms0day.ppsx
   ```

scan a single file and generate JSON output
   ```bash
   scan -j ms0day.ppsx
   scan -j ms0day.ppsx | json_pp
   ```  

scan multiple files
   ```bash
   scan file1 file2 file3
   ```

scan all files in a directory and all sub-directories
   ```bash
   scan -r dir
   ```

scan a list of files passed in on standard input
   ``` bash
   find dridex -type f | scan --from-stdin
   ```

scan a single file with a single yara rule
   ```bash
   scan -y myrule.yar target_file
   ```

scan a single file with all rules in a given directory
  ```bash
  scan -Y my_rule_dir target_file
  ```

check the syntax of all the rules in a given directory
   ```bash
   scan -c -Y my_rule_dir
   ```

## Blacklisting

The scan tool also supports "blacklisting" rules. These are specified by using the -b and -B command line options. These allow you to exclude certain rules from the search results rather than making changes to the rules themselves. We use this technique to allow us to use the open source yara repository as-is, rather than trying to maintain a modified branch.

## Rule Output Selection

You can specify when a rule should (or should not) be displayed. This allows you to prevent some rules from matching against certain kinds of files, or for a rule to be matched against only one specific file.

The rules are specified as metadata name and value pairs. (example rule syntax)

```yara
rule html_rule: odd html
{
meta:
   mime_type = "text/html"
strings:
   ...
condition:
   ...
}
```

### Metadata Names and Descriptions

```
file_ext   | Matches everything past the first period in the file name.
file_name  | Matches the full name of the file (not including the path.)
full_path  | Matches against the full path of the file, if one was specified.
mime_type  | Matches against the output of file -b --mime-type.
```

The value of the metadata variable is the string to match. By default the library matches as is, but special modifiers can be used to perform sub string matching and regular expressions. **Special modifiers are added to the beginning of the value (or list of values) and apply to all values in the string.**

### Matching Modifiers

```
!     | negation    | Negates the match. This can be placed before other modifiers.
sub:  | sub-search  | Match if this string appears anywhere.
re:   | regex       | Match if the regular expression is satisfied.
```

Values can be a comma separated list of values, regardless of the modifiers. Therefor, commas cannot be used in the patterns.

### Rule Selection Examples

Only match files the end with the .exe extension.

``` 
file_ext = "exe"
```

Only match files that end with .exe, .dll or .ocx extension.

```
file_ext = "exe, dll, ocx"
```

Only match files that do not end with .exe, .dll or .ocx extension.

```
file_ext = "!exe, dll, ocx"
```

Only matches files that do not end with .bmp.

```
file_ext = "!bmp"
```

Only match files identified as PDF despite the file name.

```
mime_type = "application/pdf"
```

Only match files not identified as images.

```
mime_type = "!sub:image/"
```

Only match files that look like an invoice phish.

```
file_name = "re:invoice[0-9]+\\.doc$"
```

Only match files in a subdirectory called /ole.

```
full_path = "sub:/ole/"
```

## Yara Rule Performance Testing

It's often useful to know not only what rules have poor performance, but also what strings inside of those rules are causing the issue. This library has special support for this.

### How Performance Testing Works

Each yara rule is extracted and tested on its own against the following sets of data.

- random data (either a 1MB random sequence of bytes or the contents of a file specified by the `--test-data` option.)
- repeating byte patterns (1MB of repeating bytes of the same value.)

In total there are 256 buffers to test against for each test (one random and 255 repeating byte buffers.)

You can optionally also extract each regular expression from specified rules and test them by themselves against the same buffers. This allows you to determine which string is causing the issue.

## Executing Performance Tests

Testing all rules but not strings.

```bash
scan -t
```

Testing all rules and the strings of rules that take longer than 0.1 seconds to scan any buffer.

```bash
scan -t --test-strings-if --test-strings-threshold 0.1
```

Test a specific rule and all the strings inside of it.

```bash
scan -t --test-rule MyYaraRule --test-strings
```

Test all rules against the file `sample.dat`.

```bash
scan -t --test-data sample.dat
```

## CSV Output

The output of the test can be saved to CSV files using the following options.

`--performance-csv` saves the performance data of entire yara files.

`--failure-csv` saves any rules that fail under performance testing.

`--string-performance-csv` saves the performance data of individual yara strings.

`--string-failure-csv` save any strings that fail under performance testing.

Note that if you do not specify these options the output is sent to standard out.

## Output Format (Performance Data)

Performance data has the following format.

`buffer_name, file_path, rule_name, total_seconds`

`buffer_name` a description of the buffer that was used by the test, either **random** for random (or file) data, or **chr(*n*)** where *n* is the byte that was used for the buffer.

`file_path` the path to the file that contains the yara rule.

`rule_name` the name of the yara rule.

`total_seconds` the total amount of time it took the yara rule to scan the given buffer.

String performance data is similar but contains two additional fields.

`buffer_name, file_path, rule_name, string_name, result_count, total_seconds`

`string_name` is the name of the string inside the yara rule.

`result_count` is the total number of times the string matched inside the buffer.

## Output Format (Error Data)

Error data has a format that is similar to the performance data but inside of **total_seconds** you will see the error message that occurred when the given yara rule or string was used to scan the given buffer.

## Error 30

If you see "Error 30" is means your rule, or strings inside of a rule, matched too many times.