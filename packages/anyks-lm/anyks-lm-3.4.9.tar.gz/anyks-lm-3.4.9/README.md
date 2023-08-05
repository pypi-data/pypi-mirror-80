[![ANYKS Smart language model](https://raw.githubusercontent.com/anyks/alm/master/site/img/banner.jpg)](https://anyks.com)

# ANYKS Language Model (ALM)

## Project goals and features

The are many toolkits capable of creating language models: ([KenLM](https://github.com/kpu/kenlm), [SriLM](https://github.com/BitMindLab/SRILM), [IRSTLM](https://github.com/irstlm-team/irstlm)), and each of those toolkits may have a reason to exist. But our language model creation toolkit has the following goals and features:

- **UTF-8 support**: Full UTF-8 support without third-party dependencies.
- **Support of many data formats**: ARPA, Vocab, Map Sequence, N-grams, Binary alm dictionary.
- **Smoothing algorithms**: Kneser-Nay, Modified Kneser-Nay, Witten-Bell, Additive, Good-Turing, Absolute discounting.
- **Normalisation and preprocessing for corpora**: Transferring corpus to lowercase, smart tokenization, ability to create black - and white - lists for n-grams.
- **ARPA modification**: Frequencies and n-grams replacing, adding new n-grams with frequencies, removing n-grams.
- **Pruning**: N-gram removal based on specified criteria.
- **Removal of low-probability n-grams**: Removal of n-grams which backoff probability is higher than standard probability.
- **ARPA recovery**: Recovery of damaged n-grams in ARPA with subsequent recalculation of their backoff probabilities.
- **Support of additional word features**: Feature extraction: (numbers, roman numbers, ranges of numbers, numeric abbreviations, any other custom attributes) using scripts written in Python3.
- **Text preprocessing**: Unlike all other language model toolkits, ALM can extract correct context from files with unnormalized texts.
- **Unknown word token accounting**: Accounting of 〈unk〉 token as full n-gram.
- **Redefinition of 〈unk〉 token**: Ability to redefine an attribute of an unknown token.
- **N-grams preprocessing**: Ability to pre-process n-grams before adding them to ARPA using custom Python3 scripts.
- **Binary container for Language Models**: The binary container supports compression, encryption and installation of copyrights.
- **Convenient visualization of the Language model assembly process**: ALM implements several types of visualizations: textual, graphic, process indicator, and logging to files or console.
- **Collection of all n-grams**: Unlike other language model toolkits, ALM is guaranteed to extract all possible n-grams from the corpus, regardless of their length (except for Modified Kneser-Nay); you can also force all n-grams to be taken into account even if they occured only once.

## Requirements

- [Zlib](http://www.zlib.net)
- [OpenSSL](https://www.openssl.org)
- [Python3](https://www.python.org/download/releases/3.0)
- [NLohmann::json](https://github.com/nlohmann/json)
- [BigInteger](http://mattmccutchen.net/bigint)

## Install PyBind11

```bash
$ python3 -m pip install pybind11
```

## Description of Methods

### Methods:
- **idw** - Word ID retrieval method
- **idt** - Token ID retrieval method
- **ids** - Sequence ID retrieval method

### Example:
```python
>>> import alm
>>>
>>> alm.idw("hello")
313191024
>>>
>>> alm.idw("<s>")
1
>>>
>>> alm.idw("</s>")
22
>>>
>>> alm.idw("<unk>")
3
>>>
>>> alm.idt("1424")
2
>>>
>>> alm.idt("hello")
0
>>>
>>> alm.idw("Living")
13268942501
>>>
>>> alm.idw("in")
2047
>>>
>>> alm.idw("the")
83201
>>>
>>> alm.idw("USA")
72549
>>>
>>> alm.ids([13268942501, 2047, 83201, 72549])
16314074810955466382
```

### Description
| Name      | Description                                                                                                                                           |
|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
|〈s〉       | Sentence beginning token                                                                                                                              |
|〈/s〉      | Sentence end token                                                                                                                                    |
|〈url〉     | URL-address token                                                                                                                                     |
|〈num〉     | Number (arabic or roman) token                                                                                                                        |
|〈unk〉     | Unknown word token                                                                                                                                    |
|〈time〉    | Time token (15:44:56)                                                                                                                                 |
|〈score〉   | Score count token (4:3 ¦ 01:04)                                                                                                                       |
|〈fract〉   | Fraction token (5/20 ¦ 192/864)                                                                                                                       |
|〈date〉    | Date token (18.07.2004 ¦ 07/18/2004)                                                                                                                  |
|〈abbr〉    | Abbreviation token (1-й ¦ 2-е ¦ 20-я ¦ p.s ¦ p.s.)                                                                                                    |
|〈dimen〉   | Dimensions token (200x300 ¦ 1920x1080)                                                                                                                |
|〈range〉   | Range of numbers token (1-2 ¦ 100-200 ¦ 300-400)                                                                                                      |
|〈aprox〉   | Approximate number token (~93 ¦ ~95.86 ¦ 10~20)                                                                                                       |
|〈anum〉    | Pseudo-number token (combination of numbers and other symbols) (T34 ¦ 895-M-86 ¦ 39km)                                                                |
|〈pcards〉  | Symbols of the play cards (♠ ¦ ♣ ¦ ♥ ¦ ♦ )                                                                                                            |
|〈punct〉   | Punctuation token (. ¦ , ¦ ? ¦ ! ¦ : ¦ ; ¦ … ¦ ¡ ¦ ¿)                                                                                                 |
|〈route〉   | Direction symbols (arrows) (← ¦ ↑ ¦ ↓ ¦ ↔ ¦ ↵ ¦ ⇐ ¦ ⇑ ¦ ⇒ ¦ ⇓ ¦ ⇔ ¦ ◄ ¦ ▲ ¦ ► ¦ ▼)                                                                    |
|〈greek〉   | Symbols of the Greek alphabet (Α ¦ Β ¦ Γ ¦ Δ ¦ Ε ¦ Ζ ¦ Η ¦ Θ ¦ Ι ¦ Κ ¦ Λ ¦ Μ ¦ Ν ¦ Ξ ¦ Ο ¦ Π ¦ Ρ ¦ Σ ¦ Τ ¦ Υ ¦ Φ ¦ Χ ¦ Ψ ¦ Ω)                         |
|〈isolat〉  | Isolation/quotation token (( ¦ ) ¦ [ ¦ ] ¦ { ¦ } ¦ " ¦ « ¦ » ¦ „ ¦ “ ¦ ` ¦ ⌈ ¦ ⌉ ¦ ⌊ ¦ ⌋ ¦ ‹ ¦ › ¦ ‚ ¦ ’ ¦ ′ ¦ ‛ ¦ ″ ¦ ‘ ¦ ” ¦ ‟ ¦ ' ¦〈 ¦ 〉)         |
|〈specl〉   | Special character token (_ ¦ @ ¦ # ¦ № ¦ © ¦ ® ¦ & ¦ § ¦ æ ¦ ø ¦ Þ ¦ – ¦ ‾ ¦ ‑ ¦ — ¦ ¯ ¦ ¶ ¦ ˆ ¦ ˜ ¦ † ¦ ‡ ¦ • ¦ ‰ ¦ ⁄ ¦ ℑ ¦ ℘ ¦ ℜ ¦ ℵ ¦ ◊ ¦ \ )     |
|〈currency〉| Symbols of world currencies ($ ¦ € ¦ ₽ ¦ ¢ ¦ £ ¦ ₤ ¦ ¤ ¦ ¥ ¦ ℳ ¦ ₣ ¦ ₴ ¦ ₸ ¦ ₹ ¦ ₩ ¦ ₦ ¦ ₭ ¦ ₪ ¦ ৳ ¦ ƒ ¦ ₨ ¦ ฿ ¦ ₫ ¦ ៛ ¦ ₮ ¦ ₱ ¦ ﷼ ¦ ₡ ¦ ₲ ¦ ؋ ¦ ₵ ¦ ₺ ¦ ₼ ¦ ₾ ¦ ₠ ¦ ₧ ¦ ₯ ¦ ₢ ¦ ₳ ¦ ₥ ¦ ₰ ¦ ₿ ¦ ұ) |
|〈math〉    | Mathematical operation token (+ ¦ - ¦ = ¦ / ¦ * ¦ ^ ¦ × ¦ ÷ ¦ − ¦ ∕ ¦ ∖ ¦ ∗ ¦ √ ¦ ∝ ¦ ∞ ¦ ∠ ¦ ± ¦ ¹ ¦ ² ¦ ³ ¦ ½ ¦ ⅓ ¦ ¼ ¦ ¾ ¦ % ¦ ~ ¦ · ¦ ⋅ ¦ ° ¦ º ¦ ¬ ¦ ƒ ¦ ∀ ¦ ∂ ¦ ∃ ¦ ∅ ¦ ∇ ¦ ∈ ¦ ∉ ¦ ∋ ¦ ∏ ¦ ∑ ¦ ∧ ¦ ∨ ¦ ∩ ¦ ∪ ¦ ∫ ¦ ∴ ¦ ∼ ¦ ≅ ¦ ≈ ¦ ≠ ¦ ≡ ¦ ≤ ¦ ≥ ¦ ª ¦ ⊂ ¦ ⊃ ¦ ⊄ ¦ ⊆ ¦ ⊇ ¦ ⊕ ¦ ⊗ ¦ ⊥ ¦ ¨) |

---

### Methods:
- **setZone** - User zone set method

### Example:
```python
>>> import alm
>>>
>>> alm.setZone("com")
>>> alm.setZone("ru")
>>> alm.setZone("org")
>>> alm.setZone("net")
```

---

### Methods:
- **clear** - Method clear all data
- **setAlphabet** - Method set alphabet
- **getAlphabet** - Method get alphabet

### Example:
```python
>>> import alm
>>>
>>> alm.getAlphabet()
'abcdefghijklmnopqrstuvwxyz'
>>>
>>> alm.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> alm.getAlphabet()
'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
>>>
>>> alm.clear()
>>>
>>> alm.getAlphabet()
'abcdefghijklmnopqrstuvwxyz'
```

---

### Methods:
- **setUnknown** - Method set unknown word
- **getUnknown** - Method extraction unknown word

### Example:
```python
>>> import alm
>>>
>>> alm.setUnknown("word")
>>>
>>> alm.getUnknown()
'word'
```

---

### Methods:
- **info** - Dictionary information output method
- **init** - Language Model Initialization Method signature: [smoothing = wittenBell, modified = False, prepares = False, mod = 0.0]
- **token** - Method for determining the type of the token words
- **addText** - Method of adding text for estimate
- **collectCorpus** - Training method of assembling the text data for ALM
- **pruneVocab** - Dictionary pruning method
- **buildArpa** - Method for build ARPA
- **writeALM** - Method for writing data from ARPA file to binary container
- **writeWords** - Method for writing these words to a file
- **writeVocab** - Method for writing dictionary data to a file
- **writeNgrams** - Method of writing data to NGRAMs files
- **writeMap** - Method of writing sequence map to file
- **writeSuffix** - Method for writing data to a suffix file for digital abbreviations
- **writeAbbrs** - Method for writing data to an abbreviation file
- **getSuffixes** - Method for extracting the list of suffixes of digital abbreviations
- **writeArpa** - Method of writing data to ARPA file
- **setSize** - Method for set size N-gram
- **setLocale** - Method set locale (Default: en_US.UTF-8)
- **pruneArpa** - Language model pruning method
- **addWord** - Method for add a word to the dictionary
- **setThreads** - Method for setting the number of threads used in work (0 - all available threads)
- **setSubstitutes** - Method for set letters to correct words from mixed alphabets
- **addAbbr** - Method add abbreviation
- **setAbbrs** - Method set abbreviations
- **getAbbrs** - Method for extracting the list of abbreviations
- **addGoodword** - Method add good word
- **addBadword** - Method add bad word
- **readArpa** - Method for reading an ARPA file, language model
- **readVocab** - Method of reading the dictionary
- **setAdCw** - Method for set dictionary characteristics (cw - count all words in dataset, ad - count all documents in dataset)

#### Description
| Smoothing       |
|-----------------|
| wittenBell      |
| addSmooth       |
| goodTuring      |
| constDiscount   |
| naturalDiscount |
| kneserNey       |
| modKneserNey    |

### Example:
```python
>>> import alm
>>>
>>> alm.info("./lm.alm")


* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

* Name: Test Language Model

* Encryption: AES128

* Alphabet: абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz

* Build date: 09/18/2020 21:52:00

* N-gram size: 3

* Words: 9373

* N-grams: 25021

* Author: Some name

* Contacts: site: https://example.com, e-mail: info@example.com

* Copyright ©: You company LLC

* License type: MIT

* License text:
... License text ...

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

>>> 
```

### Example:
```python
>>> import alm
>>> import json
>>> 
>>> alm.setSize(3)
>>> alm.setThreads(0)
>>> alm.setLocale("en_US.UTF-8")
>>> alm.setAlphabet("абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz")
>>> alm.setSubstitutes({'p':'р','c':'с','o':'о','t':'т','k':'к','e':'е','a':'а','h':'н','x':'х','b':'в','m':'м'})
>>> 
>>> alm.setOption(alm.options_t.allowUnk)
>>> alm.setOption(alm.options_t.resetUnk)
>>> alm.setOption(alm.options_t.mixDicts)
>>> alm.setOption(alm.options_t.tokenWords)
>>> alm.setOption(alm.options_t.interpolate)
>>> 
>>> alm.init(alm.smoothing_t.modKneserNey, True, True)
>>> 
>>> p = alm.getParams()
>>> p.algorithm
4
>>> p.mod
0.0
>>> p.prepares
True
>>> p.modified
True
>>> alm.idw("Сбербанк")
13236490857
>>> alm.idw("Совкомбанк")
22287680895
>>> 
>>> alm.token("Сбербанк")
'<unk>'
>>> alm.token("совкомбанк")
'<unk>'
>>> 
>>> alm.setAbbrs({13236490857, 22287680895})
>>> 
>>> alm.addAbbr("США")
>>> alm.addAbbr("Сбер")
>>> 
>>> alm.token("Сбербанк")
'<abbr>'
>>> alm.token("совкомбанк")
'<abbr>'
>>> 
>>> alm.token("сша")
'<abbr>'
>>> alm.token("СБЕР")
'<abbr>'
>>> 
>>> alm.getAbbrs()
{13236490857, 189243, 22287680895, 26938511}
>>> 
>>> alm.addGoodword("T-34")
>>> alm.addGoodword("АН-25")
>>> 
>>> alm.addBadword("ийти")
>>> alm.addBadword("циган")
>>> alm.addBadword("апичатка")
>>> 
>>> alm.addWord("министерство")
>>> alm.addWord("возмездие", 0, 1)
>>> alm.addWord("возражение", alm.idw("возражение"), 2)
>>> 
>>> def status(text, status):
...     print(text, status)
... 
>>> def statusWriteALM(status):
...     print("Write ALM", status)
... 
>>> def statusWriteArpa(status):
...     print("Write ARPA", status)
... 
>>> def statusBuildArpa(status):
...     print("Build ARPA", status)
... 
>>> def statusPrune(status):
...     print("Prune data", status)
... 
>>> def statusWords(status):
...     print("Write words", status)
... 
>>> def statusVocab(status):
...     print("Write vocab", status)
... 
>>> def statusNgram(status):
...     print("Write ngram", status)
... 
>>> def statusMap(status):
...     print("Write map", status)
... 
>>> def statusSuffix(status):
...     print("Write suffix", status)
... 
>>> def statusAbbreviation(status):
...     print("Write abbreviation", status)
... 
>>> alm.addText("The future is now", 0)
>>> 
>>> alm.collectCorpus("./correct.txt", status)
Read text corpora 0
Read text corpora 1
Read text corpora 2
Read text corpora 3
Read text corpora 4
Read text corpora 5
Read text corpora 6
...
>>> alm.pruneVocab(-15.0, 0, 0, statusPrune)
Prune data 0
Prune data 1
Prune data 2
Prune data 3
Prune data 4
Prune data 5
Prune data 6
...
>>> alm.pruneArpa(0.015, 3, statusPrune)
Prune data 0
Prune data 1
Prune data 2
Prune data 3
Prune data 4
Prune data 5
Prune data 6
...
>>> meta = {
...     "aes": 128,
...     "name": "Test Language Model",
...     "author": "Some name",
...     "lictype": "MIT",
...     "password": "password",
...     "copyright": "You company LLC",
...     "lictext": "... License text ...",
...     "contacts": "site: https://example.com, e-mail: info@example.com"
... }
>>> 
>>> alm.writeALM("./lm.alm", json.dumps(meta), statusWriteALM)
Write ALM 0
Write ALM 0
Write ALM 0
Write ALM 0
Write ALM 0
Write ALM 0
...
>>> alm.writeWords("./words.txt", statusWords)
Write words 0
Write words 1
Write words 2
Write words 3
Write words 4
Write words 5
Write words 6
...
>>> alm.writeVocab("./lm.vocab", statusVocab)
Write vocab 0
Write vocab 1
Write vocab 2
Write vocab 3
Write vocab 4
Write vocab 5
Write vocab 6
...
>>> alm.writeNgrams("./lm.ngram", statusNgram)
Write ngram 0
Write ngram 1
Write ngram 2
Write ngram 3
Write ngram 4
Write ngram 5
Write ngram 6
...
>>> alm.writeMap("./lm.map", statusMap, "|")
Write map 0
Write map 1
Write map 2
Write map 3
Write map 4
Write map 5
Write map 6
...
>>> alm.writeSuffix("./suffix.txt", statusSuffix)
Write suffix 10
Write suffix 20
Write suffix 30
Write suffix 40
Write suffix 50
Write suffix 60
...
>>> alm.writeAbbrs("./words.abbr", statusAbbreviation)
Write abbreviation 25
Write abbreviation 50
Write abbreviation 75
Write abbreviation 100
...
>>> alm.getAbbrs()
{13236490857, 189243, 22287680895, 26938511}
>>> 
>>> alm.getSuffixes()
{2633, 1662978425, 14279182218, 3468, 47, 28876661395, 29095464659, 2968, 57, 30}
>>> 
>>> alm.buildArpa(statusBuildArpa)
Build ARPA 0
Build ARPA 1
Build ARPA 2
Build ARPA 3
Build ARPA 4
Build ARPA 5
Build ARPA 6
...
>>> alm.writeArpa("./lm.arpa", statusWriteArpa)
Write ARPA 0
Write ARPA 1
Write ARPA 2
Write ARPA 3
Write ARPA 4
Write ARPA 5
Write ARPA 6
...
```

---

### Methods:
- **setOption** - Library options setting method
- **unsetOption** - Disable module option method

### Example:
```python
>>> import alm
>>>
>>> alm.unsetOption(alm.options_t.debug)
>>> alm.unsetOption(alm.options_t.mixDicts)
>>> alm.unsetOption(alm.options_t.onlyGood)
>>> alm.unsetOption(alm.options_t.confidence)
...
```

#### Description
| Options     | Description                                                                              |
|-------------|------------------------------------------------------------------------------------------|
| debug       | Flag debug mode                                                                          |
| stress      | Flag allowing to stress in words                                                         |
| uppers      | Flag that allows you to correct the case of letters                                      |
| onlyGood    | Flag allowing to consider words from the white list only                                 |
| mixDicts    | Flag allowing the use of words consisting of mixed dictionaries                          |
| allowUnk    | Flag allowing to unknown word                                                            |
| resetUnk    | Flag to reset the frequency of an unknown word                                           |
| allGrams    | Flag allowing accounting of all collected n-grams                                        |
| lowerCase   | Flag allowing to case-insensitive                                                        |
| confidence  | Flag ARPA file loading without pre-processing the words                                  |
| tokenWords  | Flag that takes into account when assembling N-grams, only those tokens that match words |
| interpolate | Flag allowing to use interpolation in estimating                                         |

---

### Methods:
- **readMap** - Method for reading sequence map from file

### Example:
```python
>>> import alm
>>>
>>> alm.setLocale("en_US.UTF-8")
>>>
>>> alm.setAlphabet("абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz")
>>> alm.setSubstitutes({'p':'р','c':'с','o':'о','t':'т','k':'к','e':'е','a':'а','h':'н','x':'х','b':'в','m':'м'})
>>>
>>> alm.setOption(alm.options_t.allowUnk)
>>> alm.setOption(alm.options_t.resetUnk)
>>> alm.setOption(alm.options_t.mixDicts)
>>> 
>>> def statusMap(text, status):
...     print("Read map", text, status)
... 
>>> def statusBuildArpa(status):
...     print("Build ARPA", status)
... 
>>> def statusPrune(status):
...     print("Prune data", status)
... 
>>> def statusVocab(text, status):
...     print("Read Vocab", text, status)
... 
>>> def statusWriteArpa(status):
...     print("Write ARPA", status)
... 
>>> alm.init(alm.smoothing_t.wittenBell)
>>> 
>>> p = alm.getParams()
>>> p.algorithm
2
>>> alm.readVocab("./lm.vocab", statusVocab)
Read Vocab ./lm.vocab 0
Read Vocab ./lm.vocab 1
Read Vocab ./lm.vocab 2
Read Vocab ./lm.vocab 3
Read Vocab ./lm.vocab 4
Read Vocab ./lm.vocab 5
Read Vocab ./lm.vocab 6
...
>>> alm.readMap("./lm1.map", statusMap, "|")
Read map ./lm.map 0
Read map ./lm.map 1
Read map ./lm.map 2
Read map ./lm.map 3
Read map ./lm.map 4
Read map ./lm.map 5
Read map ./lm.map 6
...
>>> alm.readMap("./lm2.map", statusMap, "|")
Read map ./lm.map 0
Read map ./lm.map 1
Read map ./lm.map 2
Read map ./lm.map 3
Read map ./lm.map 4
Read map ./lm.map 5
Read map ./lm.map 6
...
>>> alm.pruneVocab(-15.0, 0, 0, statusPrune)
Prune data 0
Prune data 1
Prune data 2
Prune data 3
Prune data 4
Prune data 5
Prune data 6
...
>>> alm.buildArpa(statusBuildArpa)
Build ARPA 0
Build ARPA 1
Build ARPA 2
Build ARPA 3
Build ARPA 4
Build ARPA 5
Build ARPA 6
...
>>> alm.writeArpa("./lm.arpa", statusWriteArpa)
Write ARPA 0
Write ARPA 1
Write ARPA 2
Write ARPA 3
Write ARPA 4
Write ARPA 5
Write ARPA 6
...
>>> def getWords(word, idw, oc, dc, count):
...     print(word, idw, oc, dc, count)
...     return True
... 
>>> alm.words(getWords)
а 25 244 12 9373
б 26 11 6 9373
в 27 757 12 9373
ж 32 12 7 9373
и 34 823 12 9373
к 36 102 12 9373
о 40 63 12 9373
п 41 1 1 9373
р 42 1 1 9373
с 43 290 12 9373
у 45 113 12 9373
Х 47 1 1 9373
я 57 299 12 9373
D 61 1 1 9373
I 66 1 1 9373
да 2179 32 10 9373
за 2183 92 12 9373
на 2189 435 12 9373
па 2191 1 1 9373
та 2194 4 4 9373
об 2276 20 10 9373
...
>>> alm.getStatistic()
(13, 38124)
>> alm.setAdCw(44381, 20)
>>> alm.getStatistic()
(20, 44381)
```

### Example:
```python
>>> import alm
>>>
>>> alm.setAlphabet("абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz")
>>> alm.setSubstitutes({'p':'р','c':'с','o':'о','t':'т','k':'к','e':'е','a':'а','h':'н','x':'х','b':'в','m':'м'})
>>>
>>> alm.setOption(alm.options_t.allowUnk)
>>> alm.setOption(alm.options_t.resetUnk)
>>> alm.setOption(alm.options_t.mixDicts)
>>> 
>>> def statusBuildArpa(status):
...     print("Build ARPA", status)
... 
>>> def statusPrune(status):
...     print("Prune data", status)
... 
>>> def statusNgram(text, status):
...     print("Read Ngram", text, status)
... 
>>> def statusWriteArpa(status):
...     print("Write ARPA", status)
... 
>>> alm.init(alm.smoothing_t.addSmooth, False, False, 0.5)
>>> 
>>> p = alm.getParams()
>>> p.algorithm
0
>>> p.mod
0.5
>>> p.prepares
False
>>> p.modified
False
>>> 
>>> alm.readNgram("./lm.ngram", statusNgram)
Read Ngram ./lm.ngram 0
Read Ngram ./lm.ngram 1
Read Ngram ./lm.ngram 2
Read Ngram ./lm.ngram 3
Read Ngram ./lm.ngram 4
Read Ngram ./lm.ngram 5
Read Ngram ./lm.ngram 6
...
>>> alm.pruneVocab(-15.0, 0, 0, statusPrune)
Prune data 0
Prune data 1
Prune data 2
Prune data 3
Prune data 4
Prune data 5
Prune data 6
...
>>> alm.buildArpa(statusBuildArpa)
Build ARPA 0
Build ARPA 1
Build ARPA 2
Build ARPA 3
Build ARPA 4
Build ARPA 5
Build ARPA 6
...
>>> alm.writeArpa("./lm.arpa", statusWriteArpa)
Write ARPA 0
Write ARPA 1
Write ARPA 2
Write ARPA 3
Write ARPA 4
Write ARPA 5
Write ARPA 6
...
```

---

### Methods:
- **modify** - ARPA modification method
- **sweep** - ARPA Low Frequency N-gram Removal Method
- **repair** - Method of repair of previously calculated ARPA

### Example:
```python
>>> import alm
>>>
>>> alm.setAlphabet("абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz")
>>>
>>> alm.setOption(alm.options_t.confidence)
>>> 
>>> def statusSweep(text, status):
...     print("Sweep n-grams", text, status)
... 
>>> def statusWriteArpa(status):
...     print("Write ARPA", status)
... 
>>> alm.init()
>>> 
>>> alm.sweep("./lm.arpa", statusSweep)
Sweep n-grams Read ARPA file 0
Sweep n-grams Read ARPA file 1
Sweep n-grams Read ARPA file 2
Sweep n-grams Read ARPA file 3
Sweep n-grams Read ARPA file 4
Sweep n-grams Read ARPA file 5
Sweep n-grams Read ARPA file 6
...
Sweep n-grams Sweep N-grams 0
Sweep n-grams Sweep N-grams 1
Sweep n-grams Sweep N-grams 2
Sweep n-grams Sweep N-grams 3
Sweep n-grams Sweep N-grams 4
Sweep n-grams Sweep N-grams 5
Sweep n-grams Sweep N-grams 6
...
>>> alm.writeArpa("./lm.arpa", statusWriteArpa)
Write ARPA 0
Write ARPA 1
Write ARPA 2
Write ARPA 3
Write ARPA 4
Write ARPA 5
Write ARPA 6
...
>>> alm.clear()
>>> 
>>> alm.setAlphabet("абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz")
>>> 
>>> def statusRepair(text, status):
...     print("Repair n-grams", text, status)
... 
>>> def statusWriteArpa(status):
...     print("Write ARPA", status)
... 
>>> alm.init()
>>> 
>>> alm.repair("./lm.arpa", statusRepair)
Repair n-grams Read ARPA file 0
Repair n-grams Read ARPA file 1
Repair n-grams Read ARPA file 2
Repair n-grams Read ARPA file 3
Repair n-grams Read ARPA file 4
Repair n-grams Read ARPA file 5
Repair n-grams Read ARPA file 6
...
Repair n-grams Repair ARPA data 0
Repair n-grams Repair ARPA data 1
Repair n-grams Repair ARPA data 2
Repair n-grams Repair ARPA data 3
Repair n-grams Repair ARPA data 4
Repair n-grams Repair ARPA data 5
Repair n-grams Repair ARPA data 6
...
>>> alm.writeArpa("./lm.arpa", statusWriteArpa)
Write ARPA 0
Write ARPA 1
Write ARPA 2
Write ARPA 3
Write ARPA 4
Write ARPA 5
Write ARPA 6
...
>>> alm.clear()
>>> 
>>> alm.setAlphabet("абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz")
>>> 
>>> def statusModify(text, status):
...     print("Modify ARPA data", text, status)
... 
>>> def statusWriteArpa(status):
...     print("Write ARPA", status)
... 
>>> alm.init()
>>> 
>>> alm.modify("./lm.arpa", "./remove.txt", alm.modify_t.remove, statusModify)
Modify ARPA data Read ARPA file 0
Modify ARPA data Read ARPA file 1
Modify ARPA data Read ARPA file 2
Modify ARPA data Read ARPA file 3
Modify ARPA data Read ARPA file 4
Modify ARPA data Read ARPA file 5
Modify ARPA data Read ARPA file 6
...
Modify ARPA data Modify ARPA data 3
Modify ARPA data Modify ARPA data 10
Modify ARPA data Modify ARPA data 15
Modify ARPA data Modify ARPA data 18
Modify ARPA data Modify ARPA data 24
Modify ARPA data Modify ARPA data 30
...
>>> alm.writeArpa("./lm.arpa", statusWriteArpa)
Write ARPA 0
Write ARPA 1
Write ARPA 2
Write ARPA 3
Write ARPA 4
Write ARPA 5
Write ARPA 6
...
```

### Modification flags
| Name    | Description                                             |
|---------|---------------------------------------------------------|
| emplace | Flag of adding n-gram into existing ARPA file           |
| remove  | Flag of removing n-gram from existing ARPA file         |
| change  | Flag of changing n-gram frequency in existing ARPA file |
| replace | Flag of replacing n-gram in existing ARPA file          |

### File of adding n-gram into existing ARPA file
```
-3.002006	США
-1.365296	границ США
-0.988534	у границ США
-1.759398	замуж за
-0.092796	собираюсь замуж за
-0.474876	и тоже
-19.18453	можно и тоже
...
```

| N-gram frequency      | Separator   | N-gram       |
|-----------------------|-------------|--------------|
| -0.988534             | \t          | у границ США |

### File of changing n-gram frequency in existing ARPA file
```
-0.6588787	получайте удовольствие </s>
-0.6588787	только в одном
-0.6588787	работа связана с
-0.6588787	мужчины и женщины
-0.6588787	говоря про то
-0.6588787	потому что я
-0.6588787	потому что это
-0.6588787	работу потому что
-0.6588787	пейзажи за окном
-0.6588787	статусы для одноклассников
-0.6588787	вообще не хочу
...
```

| N-gram frequency      | Separator   | N-gram            |
|-----------------------|-------------|-------------------|
| -0.6588787            | \t          | мужчины и женщины |

### File of replacing n-gram in existing ARPA file
```
коем случае нельзя	там да тут
но тем не	да ты что
неожиданный у	ожидаемый к
в СМИ	в ФСБ
Шах	Мат
...
```

| Existing N-gram       | Separator   | New N-gram        |
|-----------------------|-------------|-------------------|
| но тем не             | \t          | да ты что         |

### File of removing n-gram from existing ARPA file
```
ну то есть
ну очень большой
бы было если
мы с ней
ты смеешься над
два года назад
над тем что
или еще что-то
как я понял
как ни удивительно
как вы знаете
так и не
все-таки права
все-таки болят
все-таки сдохло
все-таки встала
все-таки решился
уже
мне
мое
все
...
```

---

### Methods:
- **mix** - Multiple ARPA Interpolation Method [backward = True, forward = False]
- **mix** - Interpolation method of multiple arpa algorithms (Bayesian and Logarithmic-linear) [Bayes: length > 0, Loglinear: length == 0]

### Example:
```python
>>> import alm
>>> 
>>> alm.setAlphabet("абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz")
>>> 
>>> alm.setOption(alm.options_t.confidence)
>>> 
>>> def statusMix(text, status):
...     print("Mix ARPA data", text, status)
... 
>>> def statusWriteArpa(status):
...     print("Write ARPA", status)
... 
>>> alm.init()
>>> 
>>> alm.mix(["./lm1.arpa", "./lm2.arpa"], [0.02, 0.05], True, statusMix)
Mix ARPA data ./lm1.arpa 0
Mix ARPA data ./lm1.arpa 1
Mix ARPA data ./lm1.arpa 2
Mix ARPA data ./lm1.arpa 3
Mix ARPA data ./lm1.arpa 4
Mix ARPA data ./lm1.arpa 5
Mix ARPA data ./lm1.arpa 6
...
Mix ARPA data  0
Mix ARPA data  1
Mix ARPA data  2
Mix ARPA data  3
Mix ARPA data  4
Mix ARPA data  5
Mix ARPA data  6
>>> alm.writeArpa("./lm.arpa", statusWriteArpa)
Write ARPA 0
Write ARPA 1
Write ARPA 2
Write ARPA 3
Write ARPA 4
Write ARPA 5
Write ARPA 6
...
>>> alm.clear()
>>> 
>>> alm.setAlphabet("абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz")
>>> 
>>> def statusMix(text, status):
...     print("Mix ARPA data", text, status)
... 
>>> def statusWriteArpa(status):
...     print("Write ARPA", status)
... 
>>> alm.init()
>>> 
>>> alm.mix(["./lm1.arpa", "./lm2.arpa"], [0.02, 0.05], 0, 0.032, statusMix)
Mix ARPA data ./lm1.arpa 0
Mix ARPA data ./lm1.arpa 1
Mix ARPA data ./lm1.arpa 2
Mix ARPA data ./lm1.arpa 3
Mix ARPA data ./lm1.arpa 4
Mix ARPA data ./lm1.arpa 5
Mix ARPA data ./lm1.arpa 6
...
Mix ARPA data  0
Mix ARPA data  1
Mix ARPA data  2
Mix ARPA data  3
Mix ARPA data  4
Mix ARPA data  5
Mix ARPA data  6
>>> alm.writeArpa("./lm.arpa", statusWriteArpa)
Write ARPA 0
Write ARPA 1
Write ARPA 2
Write ARPA 3
Write ARPA 4
Write ARPA 5
Write ARPA 6
...
```

---

### Methods:
- **size** - Method of obtaining the size of the N-gram

### Example:
```python
>>> import alm
>>>
>>> alm.setOption(alm.options_t.confidence)
>>>
>>> alm.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> alm.readArpa('./lm.arpa')
>>>
>>> alm.size()
3
```

---

### Methods:
- **damerauLevenshtein** - Determination of the Damerau-Levenshtein distance in phrases
- **distanceLevenshtein** - Determination of Levenshtein distance in phrases
- **tanimoto** - Method for determining Jaccard coefficient (quotient - Tanimoto coefficient)
- **needlemanWunsch** - Word stretching method

### Example:
```python
>>> import alm
>>> alm.damerauLevenshtein("привет", "приветик")
2
>>> 
>>> alm.damerauLevenshtein("приевтик", "приветик")
1
>>> 
>>> alm.distanceLevenshtein("приевтик", "приветик")
2
>>> 
>>> alm.tanimoto("привет", "приветик")
0.7142857142857143
>>> 
>>> alm.tanimoto("привеитк", "приветик")
0.4
>>> 
>>> alm.needlemanWunsch("привеитк", "приветик")
4
>>> 
>>> alm.needlemanWunsch("привет", "приветик")
2
>>> 
>>> alm.damerauLevenshtein("acre", "car")
2
>>> alm.distanceLevenshtein("acre", "car")
3
>>> 
>>> alm.damerauLevenshtein("anteater", "theatre")
4
>>> alm.distanceLevenshtein("anteater", "theatre")
5
>>> 
>>> alm.damerauLevenshtein("banana", "nanny")
3
>>> alm.distanceLevenshtein("banana", "nanny")
3
>>> 
>>> alm.damerauLevenshtein("cat", "crate")
2
>>> alm.distanceLevenshtein("cat", "crate")
2
>>>
>>> alm.mulctLevenshtein("привет", "приветик")
4
>>>
>>> alm.mulctLevenshtein("приевтик", "приветик")
1
>>>
>>> alm.mulctLevenshtein("acre", "car")
3
>>>
>>> alm.mulctLevenshtein("anteater", "theatre")
5
>>>
>>> alm.mulctLevenshtein("banana", "nanny")
4
>>>
>>> alm.mulctLevenshtein("cat", "crate")
4
```

---

### Methods:
- **textToJson** - Method to convert text to JSON
- **isAllowApostrophe** - Apostrophe permission check method
- **switchAllowApostrophe** - Method for permitting or denying an apostrophe as part of a word

### Example:
```python
>>> import alm
>>>
>>> def callbackFn(text):
...     print(text)
... 
>>> alm.isAllowApostrophe()
False
>>> alm.switchAllowApostrophe()
>>>
>>> alm.isAllowApostrophe()
True
>>> alm.textToJson("«On nous dit qu'aujourd'hui c'est le cas, encore faudra-t-il l'évaluer» l'astronomie", callbackFn)
[["«","On","nous","dit","qu'aujourd'hui","c'est","le","cas",",","encore","faudra-t-il","l'évaluer","»","l'astronomie"]]
```

---

### Methods:
- **jsonToText** - Method to convert JSON to text

### Example:
```python
>>> import alm
>>>
>>> def callbackFn(text):
...     print(text)
... 
>>> alm.jsonToText('[["«","On","nous","dit","qu\'aujourd\'hui","c\'est","le","cas",",","encore","faudra-t-il","l\'évaluer","»","l\'astronomie"]]', callbackFn)
«On nous dit qu'aujourd'hui c'est le cas, encore faudra-t-il l'évaluer» l'astronomie
```

---

### Methods:
- **restore** - Method for restore text from context

### Example:
```python
>>> import alm
>>>
>>> alm.setOption(alm.options_t.uppers)
>>>
>>> alm.restore(["«","On","nous","dit","qu\'aujourd\'hui","c\'est","le","cas",",","encore","faudra-t-il","l\'évaluer","»","l\'astronomie"])
"«On nous dit qu'aujourd'hui c'est le cas, encore faudra-t-il l'évaluer» l'astronomie"
```

---

### Methods:
- **allowStress** - Method for allow using stress in words
- **disallowStress** - Method for disallow using stress in words

### Example:
```python
>>> import alm
>>>
>>> alm.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> def callbackFn(text):
...     print(text)
... 
>>> alm.textToJson('«Бе́лая стрела́» — согласно распространённой в 1990-е годы в России городской легенде, якобы специально организованная и подготовленная законспирированная правительственная спецслужба, сотрудники которой — бывшие и действовавшие милиционеры и спецназовцы, имеющие право на физическую ликвидацию особо опасных уголовных авторитетов и лидеров орудовавших в России ОПГ, относительно которых не представляется возможным привлечения их к уголовной ответственности законными методами[1][2][3]. Несмотря на отсутствие официальных доказательств существования организации и многочисленные опровержения со стороны силовых структур и служб безопасности[4], в российском обществе легенду считают основанной на подлинных фактах громких убийств криминальных авторитетов, совершённых в 1990-е годы, и не исключают существование реальной спецслужбы[5].', callbackFn)
[["«","Белая","стрела","»","—","согласно","распространённой","в","1990-е","годы","в","России","городской","легенде",",","якобы","специально","организованная","и","подготовленная","законспирированная","правительственная","спецслужба",",","сотрудники","которой","—","бывшие","и","действовавшие","милиционеры","и","спецназовцы",",","имеющие","право","на","физическую","ликвидацию","особо","опасных","уголовных","авторитетов","и","лидеров","орудовавших","в","России","ОПГ",",","относительно","которых","не","представляется","возможным","привлечения","их","к","уголовной","ответственности","законными","методами","[","1","]","[","2","]","[","3","]","."],["Несмотря","на","отсутствие","официальных","доказательств","существования","организации","и","многочисленные","опровержения","со","стороны","силовых","структур","и","служб","безопасности","[","4","]",",","в","российском","обществе","легенду","считают","основанной","на","подлинных","фактах","громких","убийств","криминальных","авторитетов",",","совершённых","в","1990-е","годы",",","и","не","исключают","существование","реальной","спецслужбы","[","5","]","."]]
>>>
>>> alm.jsonToText('[["«","Белая","стрела","»","—","согласно","распространённой","в","1990-е","годы","в","России","городской","легенде",",","якобы","специально","организованная","и","подготовленная","законспирированная","правительственная","спецслужба",",","сотрудники","которой","—","бывшие","и","действовавшие","милиционеры","и","спецназовцы",",","имеющие","право","на","физическую","ликвидацию","особо","опасных","уголовных","авторитетов","и","лидеров","орудовавших","в","России","ОПГ",",","относительно","которых","не","представляется","возможным","привлечения","их","к","уголовной","ответственности","законными","методами","[","1","]","[","2","]","[","3","]","."],["Несмотря","на","отсутствие","официальных","доказательств","существования","организации","и","многочисленные","опровержения","со","стороны","силовых","структур","и","служб","безопасности","[","4","]",",","в","российском","обществе","легенду","считают","основанной","на","подлинных","фактах","громких","убийств","криминальных","авторитетов",",","совершённых","в","1990-е","годы",",","и","не","исключают","существование","реальной","спецслужбы","[","5","]","."]]', callbackFn)
«Белая стрела» — согласно распространённой в 1990-е годы в России городской легенде, якобы специально организованная и подготовленная законспирированная правительственная спецслужба, сотрудники которой — бывшие и действовавшие милиционеры и спецназовцы, имеющие право на физическую ликвидацию особо опасных уголовных авторитетов и лидеров орудовавших в России ОПГ, относительно которых не представляется возможным привлечения их к уголовной ответственности законными методами [1] [2] [3].
Несмотря на отсутствие официальных доказательств существования организации и многочисленные опровержения со стороны силовых структур и служб безопасности [4], в российском обществе легенду считают основанной на подлинных фактах громких убийств криминальных авторитетов, совершённых в 1990-е годы, и не исключают существование реальной спецслужбы [5].
>>>
>>> alm.allowStress()
>>> alm.textToJson('«Бе́лая стрела́» — согласно распространённой в 1990-е годы в России городской легенде, якобы специально организованная и подготовленная законспирированная правительственная спецслужба, сотрудники которой — бывшие и действовавшие милиционеры и спецназовцы, имеющие право на физическую ликвидацию особо опасных уголовных авторитетов и лидеров орудовавших в России ОПГ, относительно которых не представляется возможным привлечения их к уголовной ответственности законными методами[1][2][3]. Несмотря на отсутствие официальных доказательств существования организации и многочисленные опровержения со стороны силовых структур и служб безопасности[4], в российском обществе легенду считают основанной на подлинных фактах громких убийств криминальных авторитетов, совершённых в 1990-е годы, и не исключают существование реальной спецслужбы[5].', callbackFn)
[["«","Бе́лая","стрела́","»","—","согласно","распространённой","в","1990-е","годы","в","России","городской","легенде",",","якобы","специально","организованная","и","подготовленная","законспирированная","правительственная","спецслужба",",","сотрудники","которой","—","бывшие","и","действовавшие","милиционеры","и","спецназовцы",",","имеющие","право","на","физическую","ликвидацию","особо","опасных","уголовных","авторитетов","и","лидеров","орудовавших","в","России","ОПГ",",","относительно","которых","не","представляется","возможным","привлечения","их","к","уголовной","ответственности","законными","методами","[","1","]","[","2","]","[","3","]","."],["Несмотря","на","отсутствие","официальных","доказательств","существования","организации","и","многочисленные","опровержения","со","стороны","силовых","структур","и","служб","безопасности","[","4","]",",","в","российском","обществе","легенду","считают","основанной","на","подлинных","фактах","громких","убийств","криминальных","авторитетов",",","совершённых","в","1990-е","годы",",","и","не","исключают","существование","реальной","спецслужбы","[","5","]","."]]
>>>
>>> alm.jsonToText('[["«","Бе́лая","стрела́","»","—","согласно","распространённой","в","1990-е","годы","в","России","городской","легенде",",","якобы","специально","организованная","и","подготовленная","законспирированная","правительственная","спецслужба",",","сотрудники","которой","—","бывшие","и","действовавшие","милиционеры","и","спецназовцы",",","имеющие","право","на","физическую","ликвидацию","особо","опасных","уголовных","авторитетов","и","лидеров","орудовавших","в","России","ОПГ",",","относительно","которых","не","представляется","возможным","привлечения","их","к","уголовной","ответственности","законными","методами","[","1","]","[","2","]","[","3","]","."],["Несмотря","на","отсутствие","официальных","доказательств","существования","организации","и","многочисленные","опровержения","со","стороны","силовых","структур","и","служб","безопасности","[","4","]",",","в","российском","обществе","легенду","считают","основанной","на","подлинных","фактах","громких","убийств","криминальных","авторитетов",",","совершённых","в","1990-е","годы",",","и","не","исключают","существование","реальной","спецслужбы","[","5","]","."]]', callbackFn)
«Бе́лая стрела́» — согласно распространённой в 1990-е годы в России городской легенде, якобы специально организованная и подготовленная законспирированная правительственная спецслужба, сотрудники которой — бывшие и действовавшие милиционеры и спецназовцы, имеющие право на физическую ликвидацию особо опасных уголовных авторитетов и лидеров орудовавших в России ОПГ, относительно которых не представляется возможным привлечения их к уголовной ответственности законными методами [1] [2] [3].
Несмотря на отсутствие официальных доказательств существования организации и многочисленные опровержения со стороны силовых структур и служб безопасности [4], в российском обществе легенду считают основанной на подлинных фактах громких убийств криминальных авторитетов, совершённых в 1990-е годы, и не исключают существование реальной спецслужбы [5].
>>>
>>> alm.disallowStress()
>>> alm.textToJson('«Бе́лая стрела́» — согласно распространённой в 1990-е годы в России городской легенде, якобы специально организованная и подготовленная законспирированная правительственная спецслужба, сотрудники которой — бывшие и действовавшие милиционеры и спецназовцы, имеющие право на физическую ликвидацию особо опасных уголовных авторитетов и лидеров орудовавших в России ОПГ, относительно которых не представляется возможным привлечения их к уголовной ответственности законными методами[1][2][3]. Несмотря на отсутствие официальных доказательств существования организации и многочисленные опровержения со стороны силовых структур и служб безопасности[4], в российском обществе легенду считают основанной на подлинных фактах громких убийств криминальных авторитетов, совершённых в 1990-е годы, и не исключают существование реальной спецслужбы[5].', callbackFn)
[["«","Белая","стрела","»","—","согласно","распространённой","в","1990-е","годы","в","России","городской","легенде",",","якобы","специально","организованная","и","подготовленная","законспирированная","правительственная","спецслужба",",","сотрудники","которой","—","бывшие","и","действовавшие","милиционеры","и","спецназовцы",",","имеющие","право","на","физическую","ликвидацию","особо","опасных","уголовных","авторитетов","и","лидеров","орудовавших","в","России","ОПГ",",","относительно","которых","не","представляется","возможным","привлечения","их","к","уголовной","ответственности","законными","методами","[","1","]","[","2","]","[","3","]","."],["Несмотря","на","отсутствие","официальных","доказательств","существования","организации","и","многочисленные","опровержения","со","стороны","силовых","структур","и","служб","безопасности","[","4","]",",","в","российском","обществе","легенду","считают","основанной","на","подлинных","фактах","громких","убийств","криминальных","авторитетов",",","совершённых","в","1990-е","годы",",","и","не","исключают","существование","реальной","спецслужбы","[","5","]","."]]
>>>
>>> alm.jsonToText('[["«","Белая","стрела","»","—","согласно","распространённой","в","1990-е","годы","в","России","городской","легенде",",","якобы","специально","организованная","и","подготовленная","законспирированная","правительственная","спецслужба",",","сотрудники","которой","—","бывшие","и","действовавшие","милиционеры","и","спецназовцы",",","имеющие","право","на","физическую","ликвидацию","особо","опасных","уголовных","авторитетов","и","лидеров","орудовавших","в","России","ОПГ",",","относительно","которых","не","представляется","возможным","привлечения","их","к","уголовной","ответственности","законными","методами","[","1","]","[","2","]","[","3","]","."],["Несмотря","на","отсутствие","официальных","доказательств","существования","организации","и","многочисленные","опровержения","со","стороны","силовых","структур","и","служб","безопасности","[","4","]",",","в","российском","обществе","легенду","считают","основанной","на","подлинных","фактах","громких","убийств","криминальных","авторитетов",",","совершённых","в","1990-е","годы",",","и","не","исключают","существование","реальной","спецслужбы","[","5","]","."]]', callbackFn)
«Белая стрела» — согласно распространённой в 1990-е годы в России городской легенде, якобы специально организованная и подготовленная законспирированная правительственная спецслужба, сотрудники которой — бывшие и действовавшие милиционеры и спецназовцы, имеющие право на физическую ликвидацию особо опасных уголовных авторитетов и лидеров орудовавших в России ОПГ, относительно которых не представляется возможным привлечения их к уголовной ответственности законными методами [1] [2] [3].
Несмотря на отсутствие официальных доказательств существования организации и многочисленные опровержения со стороны силовых структур и служб безопасности [4], в российском обществе легенду считают основанной на подлинных фактах громких убийств криминальных авторитетов, совершённых в 1990-е годы, и не исключают существование реальной спецслужбы [5].
```

---

### Methods:
- **addBadword** - Method add bad word
- **setBadwords** - Method set words to blacklist
- **getBadwords** - Method get words in blacklist

### Example:
```python
>>> import alm
>>>
>>> alm.setBadwords(["hello", "world", "test"])
>>>
>>> alm.getBadwords()
{1554834897, 2156498622, 28307030}
>>>
>>> alm.addBadword("test2")
>>>
>>> alm.getBadwords()
{5170183734, 1554834897, 2156498622, 28307030}
```

### Example:
```python
>>> import alm
>>>
>>> alm.setBadwords({24227504, 1219922507, 1794085167})
>>>
>>> alm.getBadwords()
{24227504, 1219922507, 1794085167}
>>>
>>> alm.clear(alm.clear_t.badwords)
>>>
>>> alm.getBadwords()
{}
```

---

### Methods:
- **addGoodword** - Method add good word
- **setGoodwords** - Method set words to whitelist
- **getGoodwords** - Method get words in whitelist

### Example:
```python
>>> import alm
>>>
>>> alm.setGoodwords(["hello", "world", "test"])
>>>
>>> alm.getGoodwords()
{1554834897, 2156498622, 28307030}
>>>
>>> alm.addGoodword("test2")
>>>
>>> alm.getGoodwords()
{5170183734, 1554834897, 2156498622, 28307030}
>>>
>>> alm.clear(alm.clear_t.goodwords)
>>>
>>  alm.getGoodwords()
{}
```

### Example:
```python
>>> import alm
>>>
>>> alm.setGoodwords({24227504, 1219922507, 1794085167})
>>>
>>> alm.getGoodwords()
{24227504, 1219922507, 1794085167}
```

---

### Methods:
- **setUserToken** - Method for adding user token
- **getUserTokens** - User token list retrieval method
- **getUserTokenId** - Method for obtaining user token identifier
- **getUserTokenWord** - Method for obtaining a custom token by its identifier

### Example:
```python
>>> import alm
>>>
>>> alm.setUserToken("usa")
>>>
>>> alm.setUserToken("russia")
>>>
>>> alm.getUserTokenId("usa")
5759809081
>>>
>>> alm.getUserTokenId("russia")
9910674734
>>>
>>> alm.getUserTokens()
['usa', 'russia']
>>>
>>> alm.getUserTokenWord(5759809081)
'usa'
>>>
>>> alm.getUserTokenWord(9910674734)
'russia'
>>>
>> alm.clear(alm.clear_t.utokens)
>>>
>>> alm.getUserTokens()
[]
```

---

### Methods:
- **findNgram** - N-gram search method in text
- **word** - "Method to extract a word by its identifier"

### Example:
```python
>>> import alm
>>> 
>>> def callbackFn(text):
...     print(text)
... 
>>> alm.setOption(alm.options_t.confidence)
>>> alm.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>> alm.readArpa('./lm.arpa')
>>> 
>>> alm.idw("привет")
2487910648
>>> alm.word(2487910648)
'привет'
>>> 
>>> alm.findNgram("Особое место занимает чудотворная икона Лобзание Христа Иудою", callbackFn)
<s> Особое
Особое место
место занимает
занимает чудотворная
чудотворная икона
икона Лобзание
Лобзание Христа
Христа Иудою
Иудою </s>


>>>
```

---

### Methods:
- **setUserTokenMethod** - Method for set a custom token processing function

### Example:
```python
>>> import alm
>>>
>>> def fn(token, word):
...     if token and (token == "<usa>"):
...         if word and (word.lower() == "usa"):
...             return True
...     elif token and (token == "<russia>"):
...         if word and (word.lower() == "russia"):
...             return True
...     return False
... 
>>> alm.setUserToken("usa")
>>>
>>> alm.setUserToken("russia")
>>>
>>> alm.setUserTokenMethod("usa", fn)
>>>
>>> alm.setUserTokenMethod("russia", fn)
>>>
>>> alm.idw("usa")
5759809081
>>>
>>> alm.idw("russia")
9910674734
>>>
>>> alm.getUserTokenWord(5759809081)
'usa'
>>>
>>> alm.getUserTokenWord(9910674734)
'russia'
```

---

### Methods:
- **setAlmV2** - Method for set the language model type ALMv2
- **unsetAlmV2** - Method for unset the language model type ALMv2
- **readALM** - Method for reading data from a binary container
- **setWordPreprocessingMethod** - Method for set the word preprocessing function

### Example:
```python
>>> import alm
>>> 
>>> alm.setAlmV2()
>>> 
>>> def run(word, context):
...     if word == "возле": word = "около"
...     return word
... 
>>> alm.setOption(alm.options_t.debug)
>>>
>>> alm.setOption(alm.options_t.confidence)
>>>
>>> alm.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> alm.readArpa('./lm.arpa')
>>>
>>> alm.setWordPreprocessingMethod(run)
>>>
>>> a = alm.perplexity("неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор???с лязгом выкатился и остановился возле мальчика....")
info: <s> Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор <punct> <punct> <punct> </s>

info: p( неожиданно | <s> ) 	= [2gram] 0.00038931 [ -3.40969900 ] / 0.99999991
info: p( из | неожиданно ...) 	= [2gram] 0.10110741 [ -0.99521700 ] / 0.99999979
info: p( подворотни | из ...) 	= [2gram] 0.00711798 [ -2.14764300 ] / 1.00000027
info: p( в | подворотни ...) 	= [2gram] 0.51077661 [ -0.29176900 ] / 1.00000021
info: p( олега | в ...) 	= [2gram] 0.00082936 [ -3.08125500 ] / 0.99999974
info: p( ударил | олега ...) 	= [2gram] 0.25002820 [ -0.60201100 ] / 0.99999978
info: p( яркий | ударил ...) 	= [2gram] 0.50002878 [ -0.30100500 ] / 1.00000034
info: p( прожектор | яркий ...) 	= [2gram] 0.50002878 [ -0.30100500 ] / 1.00000034
info: p( патрульный | прожектор ...) 	= [2gram] 0.50002878 [ -0.30100500 ] / 1.00000034
info: p( трактор | патрульный ...) 	= [2gram] 0.50002878 [ -0.30100500 ] / 1.00000034
info: p( <punct> | трактор ...) 	= [OOV] 0.00000000 [ -inf ] / 0.99999973
info: p( <punct> | <punct> ...) 	= [OOV] 0.00000000 [ -inf ] / 0.99999993
info: p( <punct> | <punct> ...) 	= [OOV] 0.00000000 [ -inf ] / 0.99999993
info: p( </s> | <punct> ...) 	= [1gram] 0.05693430 [ -1.24462600 ] / 0.99999993

info: 1 sentences, 13 words, 0 OOVs
info: 3 zeroprobs, logprob= -12.97624000 ppl= 8.45034200 ppl1= 9.95800426

info: <s> С лязгом выкатился и остановился около мальчика <punct> <punct> <punct> <punct> </s>

info: p( с | <s> ) 	= [2gram] 0.00642448 [ -2.19216200 ] / 0.99999991
info: p( лязгом | с ...) 	= [2gram] 0.00195917 [ -2.70792700 ] / 0.99999999
info: p( выкатился | лязгом ...) 	= [2gram] 0.50002878 [ -0.30100500 ] / 1.00000034
info: p( и | выкатился ...) 	= [2gram] 0.51169951 [ -0.29098500 ] / 1.00000024
info: p( остановился | и ...) 	= [2gram] 0.00143382 [ -2.84350600 ] / 0.99999975
info: p( около | остановился ...) 	= [1gram] 0.00011358 [ -3.94468000 ] / 1.00000003
info: p( мальчика | около ...) 	= [1gram] 0.00003932 [ -4.40541100 ] / 1.00000016
info: p( <punct> | мальчика ...) 	= [OOV] 0.00000000 [ -inf ] / 0.99999990
info: p( <punct> | <punct> ...) 	= [OOV] 0.00000000 [ -inf ] / 0.99999993
info: p( <punct> | <punct> ...) 	= [OOV] 0.00000000 [ -inf ] / 0.99999993
info: p( <punct> | <punct> ...) 	= [OOV] 0.00000000 [ -inf ] / 0.99999993
info: p( </s> | <punct> ...) 	= [1gram] 0.05693430 [ -1.24462600 ] / 0.99999993

info: 1 sentences, 11 words, 0 OOVs
info: 4 zeroprobs, logprob= -17.93030200 ppl= 31.20267541 ppl1= 42.66064865
>>> print(a.logprob)
-30.906542
```

### Example:
```python
>>> import alm
>>> 
>>> alm.setAlmV2()
>>> 
>>> alm.setOption(alm.options_t.debug)
>>>
>>> alm.setOption(alm.options_t.confidence)
>>>
>>> alm.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> def statusAlm(status):
...     print("Read ALM", status)
... 
>>> alm.readALM("./lm.alm", "password", 128, statusAlm)
Read ALM 0
Read ALM 1
Read ALM 2
Read ALM 3
Read ALM 4
Read ALM 5
Read ALM 6
...
>>>
>>> a = alm.perplexity("неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор???с лязгом выкатился и остановился возле мальчика....")
info: <s> Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор <punct> <punct> <punct> </s>

info: p( неожиданно | <s> ) 	= [2gram] 0.00038931 [ -3.40969900 ] / 0.99999991
info: p( из | неожиданно ...) 	= [2gram] 0.10110741 [ -0.99521700 ] / 0.99999979
info: p( подворотни | из ...) 	= [2gram] 0.00711798 [ -2.14764300 ] / 1.00000027
info: p( в | подворотни ...) 	= [2gram] 0.51077661 [ -0.29176900 ] / 1.00000021
info: p( олега | в ...) 	= [2gram] 0.00082936 [ -3.08125500 ] / 0.99999974
info: p( ударил | олега ...) 	= [2gram] 0.25002820 [ -0.60201100 ] / 0.99999978
info: p( яркий | ударил ...) 	= [2gram] 0.50002878 [ -0.30100500 ] / 1.00000034
info: p( прожектор | яркий ...) 	= [2gram] 0.50002878 [ -0.30100500 ] / 1.00000034
info: p( патрульный | прожектор ...) 	= [2gram] 0.50002878 [ -0.30100500 ] / 1.00000034
info: p( трактор | патрульный ...) 	= [2gram] 0.50002878 [ -0.30100500 ] / 1.00000034
info: p( <punct> | трактор ...) 	= [OOV] 0.00000000 [ -inf ] / 0.99999973
info: p( <punct> | <punct> ...) 	= [OOV] 0.00000000 [ -inf ] / 0.99999993
info: p( <punct> | <punct> ...) 	= [OOV] 0.00000000 [ -inf ] / 0.99999993
info: p( </s> | <punct> ...) 	= [1gram] 0.05693430 [ -1.24462600 ] / 0.99999993

info: 1 sentences, 13 words, 0 OOVs
info: 3 zeroprobs, logprob= -12.97624000 ppl= 8.45034200 ppl1= 9.95800426

info: <s> С лязгом выкатился и остановился около мальчика <punct> <punct> <punct> <punct> </s>

info: p( с | <s> ) 	= [2gram] 0.00642448 [ -2.19216200 ] / 0.99999991
info: p( лязгом | с ...) 	= [2gram] 0.00195917 [ -2.70792700 ] / 0.99999999
info: p( выкатился | лязгом ...) 	= [2gram] 0.50002878 [ -0.30100500 ] / 1.00000034
info: p( и | выкатился ...) 	= [2gram] 0.51169951 [ -0.29098500 ] / 1.00000024
info: p( остановился | и ...) 	= [2gram] 0.00143382 [ -2.84350600 ] / 0.99999975
info: p( около | остановился ...) 	= [1gram] 0.00011358 [ -3.94468000 ] / 1.00000003
info: p( мальчика | около ...) 	= [1gram] 0.00003932 [ -4.40541100 ] / 1.00000016
info: p( <punct> | мальчика ...) 	= [OOV] 0.00000000 [ -inf ] / 0.99999990
info: p( <punct> | <punct> ...) 	= [OOV] 0.00000000 [ -inf ] / 0.99999993
info: p( <punct> | <punct> ...) 	= [OOV] 0.00000000 [ -inf ] / 0.99999993
info: p( <punct> | <punct> ...) 	= [OOV] 0.00000000 [ -inf ] / 0.99999993
info: p( </s> | <punct> ...) 	= [1gram] 0.05693430 [ -1.24462600 ] / 0.99999993

info: 1 sentences, 11 words, 0 OOVs
info: 4 zeroprobs, logprob= -17.93030200 ppl= 31.20267541 ppl1= 42.66064865
>>> print(a.logprob)
-30.906542
```

---

### Methods:
- **setLogfile** - Method of set the file for log output
- **setOOvFile** - Method set file for saving OOVs words

### Example:
```python
>>> import alm
>>>
>>> alm.setLogfile("./log.txt")
>>>
>>> alm.setOOvFile("./oov.txt")
```

---

### Methods:
- **perplexity** - Perplexity calculation
- **pplConcatenate** - Method of combining perplexia
- **pplByFiles** - Method for reading perplexity calculation by file or group of files

### Example:
```python
>>> import alm
>>>
>>> alm.setOption(alm.options_t.confidence)
>>>
>>> alm.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> alm.readArpa('./lm.arpa')
>>>
>>> a = alm.perplexity("неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор???с лязгом выкатился и остановился возле мальчика....")
>>>
>>> print(a.logprob)
-30.906542
>>>
>>> print(a.oovs)
0
>>>
>>> print(a.words)
24
>>>
>>> print(a.sentences)
2
>>>
>>> print(a.zeroprobs)
7
>>>
>>> print(a.ppl)
17.229063831108224
>>>
>>> print(a.ppl1)
19.398698060810077
>>>
>>> b = alm.pplByFiles("./text.txt")
>>>
>>> c = alm.pplConcatenate(a, b)
>>>
>>> print(c.ppl)
7.384123548831112
```

### Description
| Name      | Description                                                                 |
|-----------|-----------------------------------------------------------------------------|
| ppl       | The meaning of perplexity without considering the beginning of the sentence |
| ppl1      | The meaning of perplexion taking into account the beginning of the sentence |
| oovs      | Count of oov words                                                          |
| words     | Count of words in sentence                                                  |
| logprob   | Word sequence frequency                                                     |
| sentences | Count of sequences                                                          |
| zeroprobs | Count of zero probs                                                         |

---

### Methods:
- **tokenization** - Method for breaking text into tokens

### Example:
```python
>>> import alm
>>>
>>> def tokensFn(word, context, reset, stop):
...     print(word, " => ", context)
...     return True
...
>>> alm.switchAllowApostrophe()
>>>
>>> alm.tokenization("«On nous dit qu'aujourd'hui c'est le cas, encore faudra-t-il l'évaluer» l'astronomie", tokensFn)
«  =>  []
On  =>  ['«']
nous  =>  ['«', 'On']
dit  =>  ['«', 'On', 'nous']
qu'aujourd'hui  =>  ['«', 'On', 'nous', 'dit']
c'est  =>  ['«', 'On', 'nous', 'dit', "qu'aujourd'hui"]
le  =>  ['«', 'On', 'nous', 'dit', "qu'aujourd'hui", "c'est"]
cas  =>  ['«', 'On', 'nous', 'dit', "qu'aujourd'hui", "c'est", 'le']
,  =>  ['«', 'On', 'nous', 'dit', "qu'aujourd'hui", "c'est", 'le', 'cas']
encore  =>  ['«', 'On', 'nous', 'dit', "qu'aujourd'hui", "c'est", 'le', 'cas', ',']
faudra-t-il  =>  ['«', 'On', 'nous', 'dit', "qu'aujourd'hui", "c'est", 'le', 'cas', ',', 'encore']
l  =>  ['«', 'On', 'nous', 'dit', "qu'aujourd'hui", "c'est", 'le', 'cas', ',', 'encore', 'faudra-t-il', 'l']
'  =>  ['«', 'On', 'nous', 'dit', "qu'aujourd'hui", "c'est", 'le', 'cas', ',', 'encore', 'faudra-t-il', 'l']
évaluer  =>  ['«', 'On', 'nous', 'dit', "qu'aujourd'hui", "c'est", 'le', 'cas', ',', 'encore', 'faudra-t-il', 'l', "'"]
»  =>  ['«', 'On', 'nous', 'dit', "qu'aujourd'hui", "c'est", 'le', 'cas', ',', 'encore', 'faudra-t-il', 'l', "'", 'évaluer']
l  =>  ['«', 'On', 'nous', 'dit', "qu'aujourd'hui", "c'est", 'le', 'cas', ',', 'encore', 'faudra-t-il', 'l', "'", 'évaluer', '»']
'  =>  ['«', 'On', 'nous', 'dit', "qu'aujourd'hui", "c'est", 'le', 'cas', ',', 'encore', 'faudra-t-il', 'l', "'", 'évaluer', '»', 'l']
astronomie  =>  ['«', 'On', 'nous', 'dit', "qu'aujourd'hui", "c'est", 'le', 'cas', ',', 'encore', 'faudra-t-il', 'l', "'", 'évaluer', '»', 'l', "'"]
```

---

### Methods:
- **setTokenizerFn** - Method for set the function of an external tokenizer

### Example:
```python
>>> import alm
>>>
>>> def tokenizerFn(text, callback):
...     word = ""
...     context = []
...     for letter in text:
...         if letter == " " and len(word) > 0:
...             if not callback(word, context, False, False): return
...             context.append(word)
...             word = ""
...         elif letter == "." or letter == "!" or letter == "?":
...             if not callback(word, context, True, False): return
...             word = ""
...             context = []
...         else:
...             word += letter
...     if len(word) > 0:
...         if not callback(word, context, False, True): return
...
>>> def tokensFn(word, context, reset, stop):
...     print(word, " => ", context)
...     return True
...
>>> alm.setTokenizerFn(tokenizerFn)
>>>
>>> alm.tokenization("Hello World today!", tokensFn)
Hello  =>  []
World  =>  ['Hello']
today  =>  ['Hello', 'World']
```

---

### Methods:
- **sentences** - Sentences generation method
- **sentencesToFile** - Method for assembling a specified number of sentences and writing to a file

### Example:
```python
>>> import alm
>>>
>>> def sentencesFn(text):
...     print("Sentences:", text)
...     return True
...
>>> alm.setOption(alm.options_t.confidence)
>>>
>>> alm.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> alm.readArpa('./lm.arpa')
>>>
>>> alm.sentences(sentencesFn)
Sentences: <s> В общем </s>
Sentences: <s> С лязгом выкатился и остановился возле мальчика </s>
Sentences: <s> У меня нет </s>
Sentences: <s> Я вообще не хочу </s>
Sentences: <s> Да и в общем </s>
Sentences: <s> Не могу </s>
Sentences: <s> Ну в общем </s>
Sentences: <s> Так что я вообще не хочу </s>
Sentences: <s> Потому что я вообще не хочу </s>
Sentences: <s> Продолжение следует </s>
Sentences: <s> Неожиданно из подворотни в олега ударил яркий прожектор патрульный трактор </s>
>>>
>>> alm.sentencesToFile(5, "./result.txt")
```

---

### Methods:
- **fixUppers** - Method for correcting registers in the text
- **fixUppersByFiles** - Method for correcting text registers in a text file

### Example:
```python
>>> import alm
>>>
>>> alm.setOption(alm.options_t.confidence)
>>>
>>> alm.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> alm.readArpa('./lm.arpa')
>>>
>>> alm.fixUppers("неожиданно из подворотни в олега ударил яркий прожектор патрульный трактор???с лязгом выкатился и остановился возле мальчика....")
'Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор??? С лязгом выкатился и остановился возле мальчика....'
>>>
>>> alm.fixUppersByFiles("./corpus", "./result.txt", "txt")
```

---

### Methods:
- **checkHypLat** - Hyphen and latin character search method

### Example:
```python
>>> import alm
>>>
>>> alm.checkHypLat("Hello-World")
(True, True)
>>>
>>> alm.checkHypLat("Hello")
(False, True)
>>>
>>> alm.checkHypLat("Привет")
(False, False)
>>>
>>> alm.checkHypLat("так-как")
(True, False)
```

---

### Methods:
- **getUppers** - Method for extracting registers for each word
- **countLetter** - Method for counting the amount of a specific letter in a word

### Example:
```python
>>> import alm
>>>
>>> alm.setOption(alm.options_t.confidence)
>>>
>>> alm.readArpa('./lm.arpa')
>>>
>>> alm.idw("Living")
10493385932
>>>
>>> alm.idw("in")
3301
>>>
>>> alm.idw("the")
217280
>>>
>>> alm.idw("USA")
188643
>>>
>>> alm.getUppers([10493385932, 3301, 217280, 188643])
[1, 0, 0, 7]
>>> 
>>> alm.countLetter("hello-world", "-")
1
>>>
>>> alm.countLetter("hello-world", "l")
3
```

---

### Methods:
- **urls** - Method for extracting URL address coordinates in a string

### Example:
```python
>>> import alm
>>>
>>> alm.urls("This website: example.com was designed with ...")
{14: 25}
>>>
>>> alm.urls("This website: https://a.b.c.example.net?id=52#test-1 was designed with ...")
{14: 52}
>>>
>>> alm.urls("This website: https://a.b.c.example.net?id=52#test-1 and 127.0.0.1 was designed with ...")
{14: 52, 57: 66}
```

---

### Methods:
- **roman2Arabic** - Method for translating Roman numerals to Arabic

### Example:
```python
>>> import alm
>>>
>>> alm.roman2Arabic("XVI")
16
```

---

### Methods:
- **rest** - Method for correction and detection of words with mixed alphabets
- **setSubstitutes** - Method for set letters to correct words from mixed alphabets
- **getSubstitutes** - Method of extracting letters to correct words from mixed alphabets

### Example:
```python
>>> import alm
>>>
>>> alm.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> alm.setSubstitutes({'p':'р','c':'с','o':'о','t':'т','k':'к','e':'е','a':'а','h':'н','x':'х','b':'в','m':'м'})
>>>
>>> alm.getSubstitutes()
{'a': 'а', 'b': 'в', 'c': 'с', 'e': 'е', 'h': 'н', 'k': 'к', 'm': 'м', 'o': 'о', 'p': 'р', 't': 'т', 'x': 'х'}
>>>
>>> str = "ПPИBETИК"
>>>
>>> str.lower()
'пpиbetик'
>>>
>>> alm.rest(str)
'приветик'
```

---

### Methods:
- **setTokensDisable** - Method for set the list of forbidden tokens
- **setTokensUnknown** - Method for set the list of tokens cast to 〈unk〉
- **setTokenDisable** - Method for set the list of unidentifiable tokens
- **setTokenUnknown** - Method of set the list of tokens that need to be identified as 〈unk〉
- **getTokensDisable** - Method for retrieving the list of forbidden tokens
- **getTokensUnknown** - Method for extracting a list of tokens reducible to 〈unk〉
- **setAllTokenDisable** - Method for set all tokens as unidentifiable
- **setAllTokenUnknown** - The method of set all tokens identified as 〈unk〉

### Example:
```python
>>> import alm
>>>
>>> alm.idw("<date>")
6
>>>
>>> alm.idw("<time>")
7
>>>
>>> alm.idw("<abbr>")
5
>>>
>>> alm.idw("<math>")
9
>>>
>>> alm.setTokenDisable("date|time|abbr|math")
>>>
>>> alm.getTokensDisable()
{9, 5, 6, 7}
>>>
>>> alm.setTokensDisable({6, 7, 5, 9})
>>>
>>> alm.setTokenUnknown("date|time|abbr|math")
>>>
>>> alm.getTokensUnknown()
{9, 5, 6, 7}
>>>
>>> alm.setTokensUnknown({6, 7, 5, 9})
>>>
>>> alm.setAllTokenDisable()
>>>
>>> alm.getTokensDisable()
{2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23}
>>>
>>> alm.setAllTokenUnknown()
>>>
>>> alm.getTokensUnknown()
{2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23}
```

---

### Methods:
- **countAlphabet** - Method of obtaining the number of letters in the dictionary

### Example:
```python
>>> import alm
>>>
>>> alm.getAlphabet()
'abcdefghijklmnopqrstuvwxyz'
>>>
>>> alm.countAlphabet()
26
>>>
>>> alm.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> alm.countAlphabet()
59
```

---

### Methods:
- **countBigrams** - Method get count bigrams
- **countTrigrams** - Method get count trigrams
- **countGrams** - Method get count N-gram by lm size

### Example:
```python
>>> import alm
>>>
>>> alm.setOption(alm.options_t.confidence)
>>>
>>> alm.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> alm.readArpa('./lm.arpa')
>>>
>>> alm.countBigrams("неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор???с лязгом выкатился и остановился возле мальчика....")
12
>>>
>>> alm.countTrigrams("неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор???с лязгом выкатился и остановился возле мальчика....")
10
>>>
>>> alm.size()
3
>>>
>>> alm.countGrams("неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор???с лязгом выкатился и остановился возле мальчика....")
10
>>>
>>> alm.idw("неожиданно")
3263936167
>>>
>>> alm.idw("из")
5134
>>>
>>> alm.idw("подворотни")
12535356101
>>>
>>> alm.idw("в")
53
>>>
>>> alm.idw("Олега")
2824508300
>>>
>>> alm.idw("ударил")
24816796913
>>>
>>> alm.countBigrams([3263936167, 5134, 12535356101, 53, 2824508300, 24816796913])
5
>>>
>>> alm.countTrigrams([3263936167, 5134, 12535356101, 53, 2824508300, 24816796913])
4
>>>
>>> alm.countGrams([3263936167, 5134, 12535356101, 53, 2824508300, 24816796913])
4
```

---

### Methods:
- **arabic2Roman** - Convert arabic number to roman number

### Example:
```python
>>> import alm
>>>
>>> alm.arabic2Roman(23)
'XXIII'
>>>
>>> alm.arabic2Roman("33")
'XXXIII'
```

---

### Methods:
- **setThreads** - Method for set the number of threads (0 - all threads)

### Example:
```python
>>> import alm
>>>
>>> alm.setOption(alm.options_t.confidence)
>>>
>>> alm.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> alm.readArpa('./lm.arpa')
>>>
>>> alm.setThreads(3)
>>>
>>> a = alm.pplByFiles("./text.txt")
>>>
>>> print(a.logprob)
-48201.29481399994
```

---

### Methods:
- **fti** - Method for removing the fractional part of a number

### Example:
```python
>>> import alm
>>>
>>> alm.fti(5892.4892)
5892489200000
>>>
>>> alm.fti(5892.4892, 4)
58924892
```

---

### Methods:
- **context** - Method for assembling text context from a sequence

### Example:
```python
>>> import alm
>>>
>>> alm.setOption(alm.options_t.confidence)
>>>
>>> alm.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> alm.readArpa('./lm.arpa')
>>>
>>> alm.idw("неожиданно")
3263936167
>>>
>>> alm.idw("из")
5134
>>>
>>> alm.idw("подворотни")
12535356101
>>>
>>> alm.idw("в")
53
>>>
>>> alm.idw("Олега")
2824508300
>>>
>>> alm.idw("ударил")
24816796913
>>>
>>> alm.context([3263936167, 5134, 12535356101, 53, 2824508300, 24816796913])
'Неожиданно из подворотни в Олега ударил'
```

---

### Methods:
- **isAbbr** - Method of checking a word for compliance with an abbreviation
- **isSuffix** - Method for checking a word for a suffix of a numeric abbreviation
- **isToken** - Method for checking if an identifier matches a token
- **isIdWord** - Method for checking if an identifier matches a word

### Example:
```python
>>> import alm
>>>
>>> alm.setOption(alm.options_t.confidence)
>>>
>>> alm.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> alm.readArpa('./lm.arpa')
>>>
>>> alm.addAbbr("США")
>>>
>>> alm.isAbbr("сша")
True
>>>
>>> alm.addSuffix("1-я")
>>>
>>> alm.isSuffix("1-я")
True
>>>
>>> alm.isToken(alm.idw("США"))
True
>>>
>>> alm.isToken(alm.idw("1-я"))
True
>>>
>>> alm.isToken(alm.idw("125"))
True
>>>
>>> alm.isToken(alm.idw("<s>"))
True
>>>
>>> alm.isToken(alm.idw("Hello"))
False
>>>
>>> alm.isIdWord(alm.idw("https://anyks.com"))
True
>>>
>>> alm.isIdWord(alm.idw("Hello"))
True
>>>
>>> alm.isIdWord(alm.idw("-"))
False
```

---

### Methods:
- **findByFiles** - Method search N-grams in a text file

### Example:
```python
>>> import alm
>>>
>>> alm.setOption(alm.options_t.debug)
>>>
>>> alm.setOption(alm.options_t.confidence)
>>>
>>> alm.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> alm.readArpa('./lm.arpa')
>>>
>>> alm.findByFiles("./text.txt", "./result.txt")
info: <s> Кукай
сари кукай
сари японские
японские каллиграфы
каллиграфы я
я постоянно
постоянно навещал
навещал их
их тайно
тайно от
от людей
людей </s>


info: <s> Неожиданно из
Неожиданно из подворотни
из подворотни в
подворотни в Олега
в Олега ударил
Олега ударил яркий
ударил яркий прожектор
яркий прожектор патрульный
прожектор патрульный трактор
патрульный трактор

<s> С лязгом
С лязгом выкатился
лязгом выкатился и
выкатился и остановился
и остановился возле
остановился возле мальчика
возле мальчика
```

---

### Methods:
- **checkSequence** - Sequence Existence Method
- **existSequence** - Method for checking the existence of a sequence, excluding non-word tokens
- **checkByFiles** - Method for checking if a sequence exists in a text file

### Example:
```python
>>> import alm
>>>
>>> alm.setOption(alm.options_t.debug)
>>>
>>> alm.setOption(alm.options_t.confidence)
>>>
>>> alm.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> alm.readArpa('./lm.arpa')
>>>
>>> alm.addAbbr("США")
>>>
>>> alm.isAbbr("сша")
>>>
>>> alm.checkSequence("Неожиданно из подворотни в олега ударил")
True
>>>
>>> alm.checkSequence("Сегодня сыграл и в Олега ударил яркий прожектор патрульный трактор с корпоративным сектором")
True
>>>
>>> alm.checkSequence("Сегодня сыграл и в Олега ударил яркий прожектор патрульный трактор с корпоративным сектором", True)
True
>>>
>>> alm.checkSequence("в Олега ударил яркий")
True
>>>
>>> alm.checkSequence("в Олега ударил яркий", True)
True
>>>
>>> alm.checkSequence("от госсекретаря США")
True
>>>
>>> alm.checkSequence("от госсекретаря США", True)
True
>>>
>>> alm.checkSequence("Неожиданно из подворотни в олега ударил", 2)
True
>>>
>>> alm.checkSequence(["Неожиданно","из","подворотни","в","олега","ударил"], 2)
True
>>>
>>> alm.existSequence("<s> Сегодня сыграл и в, Олега ударил яркий прожектор, патрульный трактор - с корпоративным сектором </s>", 2)
(True, 0)
>>>
>>> alm.existSequence(["<s>","Сегодня","сыграл","и","в",",","Олега","ударил","яркий","прожектор",",","патрульный","трактор","-","с","корпоративным","сектором","</s>"], 2)
(True, 2)
>>>
>>> alm.idw("от")
6086
>>>
>>> alm.idw("госсекретаря")
51273912082
>>>
>>> alm.idw("США")
5
>>>
>>> alm.checkSequence([6086, 51273912082, 5])
True
>>>
>>> alm.checkSequence([6086, 51273912082, 5], True)
True
>>>
>>> alm.checkSequence(["от", "госсекретаря", "США"])
True
>>>
>>> alm.checkSequence(["от", "госсекретаря", "США"], True)
True
>>>
>>> alm.checkByFiles("./text.txt", "./result.txt")
info: 1999 | YES | Какой-то период времени мы вообще не общались

info: 2000 | NO | Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор.С лязгом выкатился и остановился возле мальчика.

info: 2001 | YES | Так как эти яйца жалко есть а хочется все больше любоваться их можно покрыть лаком даже прозрачным лаком для ногтей

info: 2002 | NO | кукай <unk> <unk> сари кукай <unk> <unk> сари японские каллиграфы я постоянно навещал их тайно от людей

info: 2003 | NO | Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор???С лязгом выкатился и остановился возле мальчика....

info: 2004 | NO | Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор?С лязгом выкатился и остановился возле мальчика.

info: 2005 | YES | Сегодня яичницей никто не завтракал как впрочем и вчера на ближайшем к нам рынке мы ели фруктовый салат со свежевыжатым соком как в старые добрые времена в Бразилии

info: 2006 | NO | Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор!С лязгом выкатился и остановился возле мальчика.

info: 2007 | NO | Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор.с лязгом выкатился и остановился возле мальчика.

All texts: 2007
Exists texts: 1359
Not exists texts: 648
>>>
>>> alm.checkByFiles("./corpus", "./result.txt", False, "txt")
info: 1999 | YES | Какой-то период времени мы вообще не общались

info: 2000 | NO | Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор.С лязгом выкатился и остановился возле мальчика.

info: 2001 | YES | Так как эти яйца жалко есть а хочется все больше любоваться их можно покрыть лаком даже прозрачным лаком для ногтей

info: 2002 | NO | кукай <unk> <unk> сари кукай <unk> <unk> сари японские каллиграфы я постоянно навещал их тайно от людей

info: 2003 | NO | Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор???С лязгом выкатился и остановился возле мальчика....

info: 2004 | NO | Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор?С лязгом выкатился и остановился возле мальчика.

info: 2005 | YES | Сегодня яичницей никто не завтракал как впрочем и вчера на ближайшем к нам рынке мы ели фруктовый салат со свежевыжатым соком как в старые добрые времена в Бразилии

info: 2006 | NO | Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор!С лязгом выкатился и остановился возле мальчика.

info: 2007 | NO | Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор.с лязгом выкатился и остановился возле мальчика.

All texts: 2007
Exists texts: 1359
Not exists texts: 648
>>>
>>> alm.checkByFiles("./corpus", "./result.txt", True, "txt")
info: 2000 | NO | Так как эти яйца жалко есть а хочется все больше любоваться их можно покрыть лаком даже прозрачным лаком для ногтей

info: 2001 | NO | Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор.С лязгом выкатился и остановился возле мальчика.

info: 2002 | NO | Сегодня яичницей никто не завтракал как впрочем и вчера на ближайшем к нам рынке мы ели фруктовый салат со свежевыжатым соком как в старые добрые времена в Бразилии

info: 2003 | NO | Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор!С лязгом выкатился и остановился возле мальчика.

info: 2004 | NO | кукай <unk> <unk> сари кукай <unk> <unk> сари японские каллиграфы я постоянно навещал их тайно от людей

info: 2005 | NO | Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор?С лязгом выкатился и остановился возле мальчика.

info: 2006 | NO | Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор???С лязгом выкатился и остановился возле мальчика....

info: 2007 | NO | Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор.с лязгом выкатился и остановился возле мальчика.

All texts: 2007
Exists texts: 0
Not exists texts: 2007
```

---

### Methods:
- **check** - String Check Method
- **match** - String Matching Method
- **addAbbr** - Method add abbreviation
- **addSuffix** - Method add number suffix abbreviation
- **setSuffixes** - Method set number suffix abbreviations
- **readSuffix** - Method for reading data from a file of suffixes and abbreviations

### Example:
```python
>>> import alm
>>> 
>>> alm.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>> alm.setSubstitutes({'p':'р','c':'с','o':'о','t':'т','k':'к','e':'е','a':'а','h':'н','x':'х','b':'в','m':'м'})
>>> 
>>> alm.check("Дом-2", alm.check_t.home2)
True
>>> 
>>> alm.check("Дом2", alm.check_t.home2)
False
>>> 
>>> alm.check("Дом-2", alm.check_t.latian)
False
>>> 
>>> alm.check("Hello", alm.check_t.latian)
True
>>> 
>>> alm.check("прiвет", alm.check_t.latian)
True
>>> 
>>> alm.check("Дом-2", alm.check_t.hyphen)
True
>>> 
>>> alm.check("Дом2", alm.check_t.hyphen)
False
>>> 
>>> alm.check("Д", alm.check_t.letter)
True
>>> 
>>> alm.check("$", alm.check_t.letter)
False
>>> 
>>> alm.check("-", alm.check_t.letter)
False
>>> 
>>> alm.check("просtоквaшино", alm.check_t.similars)
True
>>> 
>>> alm.match("my site http://example.ru, it's true", alm.match_t.url)
True
>>> 
>>> alm.match("по вашему ip адресу 46.40.123.12 проводится проверка", alm.match_t.url)
True
>>> 
>>> alm.match("мой адрес в формате IPv6: http://[2001:0db8:11a3:09d7:1f34:8a2e:07a0:765d]/", alm.match_t.url)
True
>>> 
>>> alm.match("13-я", alm.match_t.abbr)
True
>>> 
alm.match("13-я-й", alm.match_t.abbr)
False
>>> 
alm.match("т.д", alm.match_t.abbr)
True
>>> 
alm.match("т.п.", alm.match_t.abbr)
True
>>> 
>>> alm.match("С.Ш.А.", alm.match_t.abbr)
True
>>> 
>>> alm.addAbbr("сша")
>>> alm.match("США", alm.match_t.abbr)
True
>>> 
>>> alm.addSuffix("15-летия")
>>> alm.match("15-летия", alm.match_t.abbr)
True
>>> 
>>> alm.getSuffixes()
{3139900457}
>>> 
>>> alm.idw("лет")
328041
>>> 
>>> alm.idw("тых")
352214
>>> 
>>> alm.setSuffixes({328041, 352214})
>>> 
>>> alm.getSuffixes()
{328041, 352214}
>>> 
>>> def status(status):
...     print(status)
... 
>>> alm.readSuffix("./suffix.abbr", status)
>>> 
>>> alm.match("15-лет", alm.match_t.abbr)
True
>>> 
>>> alm.match("20-тых", alm.match_t.abbr)
True
>>> 
>>> alm.match("15-летия", alm.match_t.abbr)
False
>>> 
>>> alm.match("Hello", alm.match_t.latian)
True
>>> 
>>> alm.match("прiвет", alm.match_t.latian)
False
>>> 
>>> alm.match("23424", alm.match_t.number)
True
>>> 
>>> alm.match("hello", alm.match_t.number)
False
>>> 
>>> alm.match("23424.55", alm.match_t.number)
False
>>> 
>>> alm.match("23424", alm.match_t.decimal)
False
>>> 
>>> alm.match("23424.55", alm.match_t.decimal)
True
>>> 
>>> alm.match("23424,55", alm.match_t.decimal)
True
>>> 
>>> alm.match("-23424.55", alm.match_t.decimal)
True
>>> 
>>> alm.match("+23424.55", alm.match_t.decimal)
True
>>> 
>>> alm.match("+23424.55", alm.match_t.anumber)
True
>>> 
>>> alm.match("15T-34", alm.match_t.anumber)
True
>>> 
>>> alm.match("hello", alm.match_t.anumber)
False
>>> 
>>> alm.match("hello", alm.match_t.allowed)
True
>>> 
>>> alm.match("évaluer", alm.match_t.allowed)
False
>>> 
>>> alm.match("13", alm.match_t.allowed)
True
>>> 
>>> alm.match("Hello-World", alm.match_t.allowed)
True
>>> 
>>> alm.match("Hello", alm.match_t.math)
False
>>> 
>>> alm.match("+", alm.match_t.math)
True
>>> 
>>> alm.match("=", alm.match_t.math)
True
>>> 
>>> alm.match("Hello", alm.match_t.upper)
True
>>> 
>>> alm.match("hello", alm.match_t.upper)
False
>>> 
>>> alm.match("hellO", alm.match_t.upper)
False
>>> 
>>> alm.match("a", alm.match_t.punct)
False
>>> 
>>> alm.match(",", alm.match_t.punct)
True
>>> 
>>> alm.match(" ", alm.match_t.space)
True
>>> 
>>> alm.match("a", alm.match_t.space)
False
>>> 
>>> alm.match("a", alm.match_t.special)
False
>>> 
>>> alm.match("±", alm.match_t.special)
False
>>> 
>>> alm.match("[", alm.match_t.isolation)
True
>>> 
>>> alm.match("a", alm.match_t.isolation)
False
>>> 
>>> alm.match("a", alm.match_t.greek)
False
>>> 
>>> alm.match("Ψ", alm.match_t.greek)
True
>>> 
>>> alm.match("->", alm.match_t.route)
False
>>> 
>>> alm.match("⇔", alm.match_t.route)
True
>>> 
>>> alm.match("a", alm.match_t.letter)
True
>>> 
>>> alm.match("!", alm.match_t.letter)
False
>>> 
>>> alm.match("!", alm.match_t.pcards)
False
>>> 
>>> alm.match("♣", alm.match_t.pcards)
True
>>> 
>>> alm.match("p", alm.match_t.currency)
False
>>> 
>>> alm.match("$", alm.match_t.currency)
True
>>> 
>>> alm.match("€", alm.match_t.currency)
True
>>> 
>>> alm.match("₽", alm.match_t.currency)
True
>>> 
>>> alm.match("₿", alm.match_t.currency)
True
```

---

### Methods:
- **delInText** - Method for delete letter in text

### Example:
```python
>>> import alm
>>>
>>> alm.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> alm.delInText("неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор??? с лязгом выкатился и остановился возле мальчика....", alm.wdel_t.punct)
'неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор с лязгом выкатился и остановился возле мальчика'
>>>
>>> alm.delInText("hello-world-hello-world", alm.wdel_t.hyphen)
'helloworldhelloworld'
>>>
>>> alm.delInText("неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор??? с лязгом выкатился и остановился возле мальчика....", alm.wdel_t.broken)
'неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор с лязгом выкатился и остановился возле мальчика'
>>>
>>> alm.delInText("«On nous dit qu'aujourd'hui c'est le cas, encore faudra-t-il l'évaluer» l'astronomie", alm.wdel_t.broken)
"On nous dit qu'aujourd'hui c'est le cas encore faudra-t-il l'valuer l'astronomie"
```

---

### Methods:
- **countsByFiles** - Method for counting the number of n-grams in a text file

### Example:
```python
>>> import alm
>>>
>>> alm.setOption(alm.options_t.debug)
>>>
>>> alm.setOption(alm.options_t.confidence)
>>>
>>> alm.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> alm.readArpa('./lm.arpa')
>>>
>>> alm.countsByFiles("./text.txt", "./result.txt", 3)
info: 0 | Сегодня яичницей никто не завтракал как впрочем и вчера на ближайшем к нам рынке мы ели фруктовый салат со свежевыжатым соком как в старые добрые времена в Бразилии

info: 10 | Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор?С лязгом выкатился и остановился возле мальчика.

info: 10 | Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор!С лязгом выкатился и остановился возле мальчика.

info: 0 | Так как эти яйца жалко есть а хочется все больше любоваться их можно покрыть лаком даже прозрачным лаком для ногтей

info: 10 | Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор???С лязгом выкатился и остановился возле мальчика....

Counts 3grams: 471
>>>
>>> alm.countsByFiles("./corpus", "./result.txt", 2, "txt")
info: 19 | Так как эти яйца жалко есть а хочется все больше любоваться их можно покрыть лаком даже прозрачным лаком для ногтей

info: 12 | Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор.с лязгом выкатился и остановился возле мальчика.

info: 12 | Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор!С лязгом выкатился и остановился возле мальчика.

info: 10 | кукай <unk> <unk> сари кукай <unk> <unk> сари японские каллиграфы я постоянно навещал их тайно от людей

info: 12 | Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор???С лязгом выкатился и остановился возле мальчика....

info: 12 | Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор?С лязгом выкатился и остановился возле мальчика.

info: 27 | Сегодня яичницей никто не завтракал как впрочем и вчера на ближайшем к нам рынке мы ели фруктовый салат со свежевыжатым соком как в старые добрые времена в Бразилии

Counts 2grams: 20270
```

### Description
| N-gram size | Description         |
|-------------|---------------------|
| 1           | language model size |
| 2           | bigram              |
| 3           | trigram             |
