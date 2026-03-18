CLI tool for classical ciphers
***
To add a new tool, you need to:
   1. Add help text for the tool in argument_parser() -> parser definition -> epilog
   2. Add argument parsing logic for the tool in argument_parser() below parser definition, in the Tools section
   3. Add the tool to the TOOL_INFO dictionary in argument_parser() -> TOOL INFORMATION TABLE section.
   4. Add the script for the cipher, import it and call it.
