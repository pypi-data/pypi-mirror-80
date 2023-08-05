# FarsTail: A Persian Natural Language Inference Dataset
<br>
<br>
Natural Language Inference (NLI) who is also called Texual Entailment is an important task in NLP that its goal is to determine the inference relationship between a premise p and a hypothesis h. It is a three-class problem, where each pair (p, h) is assigned to one of these classes: "ENTAILMENT" if the hypothesis can be inferred from the premise, "CONTRADICTION" if the hypothesis contradicts with the premise, and "NEUTRAL" if infering hypothesis from premise is not possible.
<br>In English, large datasets such as SNLI, MNLI, SciTail are created for this task. Even for some other languages, datasets has been created that has improved this task in these languages. But we see this less for poor source languages like persian.
<br>Persian (Farsi) language is a pluricentric language spoken by around 110 million people in countries such as Iran, Afghanistan, and Tajikistan. In this github, we present the first large scale Persian corpus for NLI task, called FarsTail.
<br>
<br>
We divided the data into test, train, and dev based on the following distribution:

| Split |     Number   |
|-------|--------------|
| Train |     7266     |
| Dev   |     1537     |
| Test  |     1564     |


## Getting started with package
We have provided an API in the form of a python package to read and use FarsTail easier. In the following, we will explain how to use this package.
<br>
<br>You'll need Python 3.6 or higher.
### Installation
```
pip install farstail
```
### using
* Loading the the FarsTail dataset.
```python
from farstail.datasets import farstail
(p_train, h_train, l_train), (p_dev, h_dev, l_dev), (p_test, h_test, l_test) = farstail.load_data()
```

* Retrieving a dict mapping words to their index in the IMDB dataset.
```python
from farsfail.datasets import farstail
farstail_word_index = farstail.get_word_index()
```
