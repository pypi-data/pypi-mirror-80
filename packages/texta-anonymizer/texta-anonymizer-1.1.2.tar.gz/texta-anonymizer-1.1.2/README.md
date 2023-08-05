# Texta Anonymizer

For anonymizing entities in plaintexts.


## Installation

`pip install texta-anonymizer`

##### From Git
`pip install git+https://git.texta.ee/texta/texta-anonymizer-python.git`

### Testing

`python -m pytest -v tests`

### Documentation

Documentation is available [here](https://git.texta.ee/texta/texta-anonymizer-python/-/wikis/Documentation).

## Usage examples

### Import Anonymizer and define input data

``` python
from texta_anonymizer.anonymizer import Anonymizer

text = """
   A. Hitler läks koos oma sõbra Jossif Staliniga poodi.
   Adolf ostis kolm pakki suitsu ja Jossif neli saia.
   Adolf Hilteri ja J. Stalini majas elab kass.
   Hiljem liitus Hitleriga neli koera.
   Hitteler ja J. Stalen läksid magama.
   Ka Yossif Stalin oli kohal.
   Pärast läks A d o l f HITLER joonistama.
   """

names = [
   {
    "first_name": "Adolf",
    "last_name" : "Hitler"
    },
  {
    "first_name": "Jossif",
    "last_name" : "Stalin"
  }
]
```

### Examples

#### Example 1: Default anonymization


``` python
# -------------------------------------------------------- #
#   Default anonymizer allows:
#       1) fuzzy matching (typos)
#       2) different forms (cases etc.)
#       3) single last name detection
#       4) single first name detection
# -------------------------------------------------------- #

anonymizer = Anonymizer()
anonymized_text = anonymizer.anonymize(text, names)
```

##### Output:
```
>>> print(anonymized_text)
    M.P läks koos oma sõbra F.F-iga poodi.
    M.P ostis kolm pakki suitsu ja F.F neli saia.
    M.P ja F.F-i majas elab kass.
    Hiljem liitus M.P-ga neli koera.
    M.P ja F.F läksid magama.
    Ka F.F oli kohal.
    Pärast läks M.P joonistama.
```

#### Example 2: Disable misspelled names replacement

``` python
anonymizer = Anonymizer(
                replace_misspelled_names = False
)

anonymized_text = anonymizer.anonymize(text, names)
```

##### Output

```
>>> print(anonymized_text)
   O.W läks koos oma sõbra A.C-ga poodi.
   O.W ostis kolm pakki suitsu ja A.C neli saia.
   O.W Hilteri ja A.C majas elab kass.
   Hiljem liitus O.W-ga neli koera.
   Hitteler ja J. Stalen läksid magama.
   Ka Yossif A.C oli kohal.
   Pärast läks O.W joonistama.

```
#### Example 3: Disable replacing single first and last names
``` python
anonymizer = Anonymizer(
                replace_single_first_names = False,
                replace_single_last_names = False
)

anonymized_text = anonymizer.anonymize(text, names)
```

##### Output

```
>>> print(anonymized_text)
   T.N läks koos oma sõbra U.W-ga poodi.
   Adolf ostis kolm pakki suitsu ja Jossif neli saia.
   T.N-i ja U.W majas elab kass.
   Hiljem liitus Hitleriga neli koera.
   Hitteler ja U.W läksid magama.
   Ka U.W oli kohal.
   Pärast läks T.N joonistama.

```
