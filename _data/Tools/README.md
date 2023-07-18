# Tools

The python files in this directory are tools for parsing and automatically updating data. Their uses (and current drawbacks) are listed below.

| File Name | Data Source | Description | Outputs | Current Drawbacks |
| --------- | ----------- | ----------- | ------- | ----------------- |
| ENR4.1parser.py | AIP ENR4.1 | Parse the VOR/NDB beacons of the UK from the AIPs ENR4.1 | `output.txt` | Currently, the output is missing some VOR/NDB beacons (which must be manually added back in), and the output includes some NDB beacons which shouldn't be included, which must be manually removed (identifiable by frequencies > 130MHz). |
