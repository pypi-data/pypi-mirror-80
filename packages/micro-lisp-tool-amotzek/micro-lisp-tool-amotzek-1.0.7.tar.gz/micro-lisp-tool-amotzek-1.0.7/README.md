# Micro Lisp Tool #

This command line tool is for ESP32 boards that are flashed with Micro Lisp.
The tool allows to run and upload Lisp programs to the boards and use the read-eval-print loop.

## Running files ##

python -m micro_lisp_tool run <file name> --port <com port>

## Uploading files ##

python -m micro_lisp_tool put <file name> --port <com port>
