# Light Life Logger

Light Life Logger is a modular, nucrses based diary/status tool.

Python modules in the `plugins` folder are loaded and sequenced; these can
define data fields, questions, and charts to be generated.

The command `log` will ask the user the questions, outputting a JSON blob
for the current date. If such a JSON blob already exists, then those values
will be used as defaults.

The command `graph` will output SVG charts for the current year, based on
the JSON blobs that are available.

Two sample plugins are provided as an example.

This project is currently 100% documentation-free. (Sorry).
