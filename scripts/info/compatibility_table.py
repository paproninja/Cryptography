compatibility_table ="""

    Compatibility table:

    Tool              | Operations                        | T             | K            | Key Type
    ------------------+-----------------------------------+---------------+--------------+------------------
    ROT               | -e (T, K); -d (T, K); -b (T); -g  | Requires Text | Requires Key | int
    SUBST             | -e (T, K); -d (T, K); -g          | Requires Text | Requires Key | 26 char long str
    ATBASH            | -e (T); -d (T)                    | Requires Text | -            | -
                      |                                   |               |              |
    VIGENERE          | -e (T, K); -d (T, K), -g          | Requires Text | Requires Key | str
                      |                                   |               |              |
    RAIL FENCE        | -e (T, K); -d (T, K); -b (T); -g  | Requires Text | Requires Key | int
    COLUMNAR TRANSPOS | -e (T, K); -d (T, K); -g          | Requires Text | Requires Key | str
                      |                                   |               |              |
    NUMVAL            | -e (T); -d (T)                    | Requires Text | -            | -

    """