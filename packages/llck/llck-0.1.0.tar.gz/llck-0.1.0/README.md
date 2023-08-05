# Lingorithm Language Core Kit
This package is the core function for any NLP operation or pacakge used by lingorithm.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install llck.

```bash
pip install llck
```

# Usage
```Python
import llck

nlp = llck('ar', {'tokenize': 'tokenize' }) 

processed = nlp.process('منشار أرضيتم بالحيوة الدنيا من الأخرة')

print(processed.sentences[0].tokens)
# [منشار, أرضيتم, ب, الحيوة, الدنيا, من, الأخرة]
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)