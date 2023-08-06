# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seqviz']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'seqviz',
    'version': '0.1.0',
    'description': 'seqviz is a Python package to visualize sequence tagging results. It can be either be used to print to console or in Jupyter Notebooks.',
    'long_description': '# seqviz\n\n**seqviz** (sequence visualization) is a Python package to visualize sequence tagging results. It can be either be used\nto print to console or in Jupyter Notebooks.\n\n<p align="center">\n  <img src="img/header.png" />\n</p>\n\n\n## Usage\n\nYou can load tagged sentences from many common formats:\n\n**iob1**\n\n```python\nfrom seqviz import TaggedSequence\n\ndata = [\n    (\'Alex\', \'I-PER\'),\n    (\'is\', \'O\'),\n    (\'going\', \'O\'),\n    (\'to\', \'O\'),\n    (\'Los\', \'I-LOC\'),\n    (\'Angeles\', \'I-LOC\'),\n    (\'in\', \'O\'),\n    (\'California\', \'I-LOC\')\n]\n\ntagged = TaggedSequence.from_bio(data, fmt="iob1")\n\nprint(tagged) # [Alex](PER) is going to [Los Angeles](LOC) in [California](LOC)\n```\n\n**iob2**\n\n```python\nfrom seqviz import TaggedSequence\n\ndata = [\n    ("Today", "O"),\n    ("Alice", "B-PER"),\n    ("Bob", "B-PER"),\n    ("and", "O"),\n    ("I", "B-PER"),\n    ("ate", "O"),\n    ("lasagna", "O"),\n]\n\ntagged = TaggedSequence.from_bio(data, fmt="iob2")\n\nprint(tagged) # Today [Alice](PER) [Bob](PER) and [I](PER) ate lasagna\n```\n\n**BIOES**\n\n```python\nfrom seqviz import TaggedSequence\n\ndata = [\n    ("Alex", "S-PER"),\n    ("is", "O"),\n    ("going", "O"),\n    ("with", "O"),\n    ("Marty", "B-PER"),\n    ("A", "I-PER"),\n    ("Rick", "E-PER"),\n    ("to", "O"),\n    ("Los", "B-LOC"),\n    ("Angeles", "E-LOC")\n]\n\ntagged = TaggedSequence.from_bio(data, fmt="bioes")\n\nprint(tagged) # "[Alex](PER) is going with [Marty A Rick](PER) to [Los Angeles](LOC)"\n```\n\n## Output formats\n\nUse it in terminal via `str(seq)`:\n\n    [Alex](PER) is going to [Los Angeles](LOC) in [California](LOC)\n\nOr as HTML via `seq.to_html()`:\n\n<p align="center">\n  <img src="img/header.png" />\n</p>\n\n## Jupyter Notebook integration\n\nYou can also use `TaggedSequence` in an Jupyter notebook:\n\n<p align="center">\n  <img src="img/jupyter_ner.png" />\n</p>\n\n## Integration with other NLP frameworks\n\n*seqviz* can be used to visualize sequences from many different popular NLP frameworks.\n\n### Hugging Face Transformers\n\n```python\nfrom transformers import AutoModelForTokenClassification, AutoTokenizer\nimport torch\n\nfrom seqviz import TaggedSequence, tokenize_for_bert\n\nmodel = AutoModelForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")\ntokenizer = AutoTokenizer.from_pretrained("bert-base-cased")\n\nlabel_list = [\n    "O",       # Outside of a named entity\n    "B-MISC",  # Beginning of a miscellaneous entity right after another miscellaneous entity\n    "I-MISC",  # Miscellaneous entity\n    "B-PER",   # Beginning of a person\'s name right after another person\'s name\n    "I-PER",   # Person\'s name\n    "B-ORG",   # Beginning of an organisation right after another organisation\n    "I-ORG",   # Organisation\n    "B-LOC",   # Beginning of a location right after another location\n    "I-LOC"    # Location\n]\n\ntext = "Hugging Face Inc. is a company based in New York City. Its headquarters are in DUMBO, therefore very " \\\n           "close to the Manhattan Bridge."\n\ninputs, groups = tokenize_for_bert(text, tokenizer)\n\noutputs = model(inputs)[0]\npredictions_tensor = torch.argmax(outputs, dim=2)[0]\n\npredictions = [label_list[prediction] for prediction in predictions_tensor]\n\nseq = TaggedSequence.from_transformers_bio(text, groups, predictions)\n```\n\n<p align="center">\n  <img src="img/transformer_ner.png" />\n</p>',
    'author': 'Jan-Christoph Klie',
    'author_email': 'git@mrklie.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jcklie/seqviz',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
