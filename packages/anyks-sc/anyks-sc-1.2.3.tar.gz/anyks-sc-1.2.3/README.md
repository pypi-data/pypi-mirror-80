[![ANYKS Smart language model](https://raw.githubusercontent.com/anyks/asc/master/site/img/banner.jpg)](https://anyks.com)

# ANYKS Spell-checker (ASC)

## Project description

There are a lot of typo and text error correction systems out there. Each one of those systems has its pros and cons, and each system has the right to live and will find its own user base. I would like to present my own version of the typo correction system with its own unique features.

## List of features

- Correction of mistakes in words with a **Levenshtein distance** of up to 4;
- Correction of different types of typos in words: insertion, deletion, substitution, rearrangement of character;
- **Ё**-fication of a word given the context (letter 'ё' is commonly replaced by letter 'е' in russian typed text);
- Context-based word capitalization for proper names and titles;
- Context-based splitting for words that are missing the separating space character;
- Text analysis without correcting the original text;
- Searching the text for errors, typos, incorrect context.

## Requirements

- [Zlib](http://www.zlib.net)
- [Bloom](http://www.partow.net/programming/bloomfilter/index.html)
- [OpenSSL](https://www.openssl.org)
- [hnswlib](https://github.com/nmslib/hnswlib)
- [HandyPack](https://github.com/bakwc/HandyPack)
- [GperfTools](https://github.com/gperftools/gperftools)
- [Python3](https://www.python.org/download/releases/3.0)
- [NLohmann::json](https://github.com/nlohmann/json)
- [BigInteger](http://mattmccutchen.net/bigint)
- [ALM](https://github.com/anyks/alm)

## Install PyBind11

```bash
$ python3 -m pip install pybind11
```

## Ready-to-use dictionaries

| Dictionary name                                                        | Size (GB)   | RAM (GB)                | N-gram order   | Language |
|------------------------------------------------------------------------|-------------|-------------------------|----------------|----------|
| [wittenbell-3-big.asc](https://cloud.mail.ru/public/2b9E/sz9b8YGJ1)    | 1.97        | 15.6                    | 3              | RU       |
| [wittenbell-3-middle.asc](https://cloud.mail.ru/public/5zo5/2F6uav8fz) | 1.24        | 9.7                     | 3              | RU       |
| [mkneserney-3-middle.asc](https://cloud.mail.ru/public/3SBP/35WJFKFyd) | 1.33        | 9.7                     | 3              | RU       |
| [wittenbell-3-single.asc](https://cloud.mail.ru/public/21jt/YEW493XQa) | 0.772       | 5.14                    | 3              | RU       |
| [wittenbell-5-single.asc](https://cloud.mail.ru/public/5Adc/5x5Ea1eA6) | 1.37        | 10.7                    | 5              | RU       |

## Testing

To test the system, we used data from the [2016 "spelling correction" competition organized by Dialog21](http://www.dialog-21.ru/evaluation/2016/spelling_correction).<br>
The trained binary dictionary that was used for testing: [wittenbell-3-middle.asc](https://cloud.mail.ru/public/5zo5/2F6uav8fz)

| Mode                              | Precision | Recall | FMeasure |
|-----------------------------------|-----------|--------|----------|
| **Typo correction**               | 76.97     | 62.71  | 69.11    |
| **Error correction**              | 73.72     | 60.53  | 66.48    |

I think it is unnecessary to add any other data. Anyone can repeat the test if they wish (all files used for testing are attached below).

### Files used for testing

- [test.txt](https://cloud.mail.ru/public/3rzx/2HwqDU9j5) - Text used for testing;
- [correct.txt](https://cloud.mail.ru/public/3dAN/J4EzV4U3W) - File with correct text;
- [evaluate.py](https://cloud.mail.ru/public/ZTRf/4sUS1Sc2p) - Python3 script for correction result evaluation.

---

## Description of Methods

### Methods:
- **idw** - Word ID retrieval method
- **idt** - Token ID retrieval method
- **ids** - Sequence ID retrieval method

### Example:
```python
>>> import asc
>>>
>>> asc.idw("hello")
313191024
>>>
>>> asc.idw("<s>")
1
>>>
>>> asc.idw("</s>")
22
>>>
>>> asc.idw("<unk>")
3
>>>
>>> asc.idt("1424")
2
>>>
>>> asc.idt("hello")
0
>>>
>>> asc.idw("Living")
13268942501
>>>
>>> asc.idw("in")
2047
>>>
>>> asc.idw("the")
83201
>>>
>>> asc.idw("USA")
72549
>>>
>>> asc.ids([13268942501, 2047, 83201, 72549])
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
>>> import asc
>>>
>>> asc.setZone("com")
>>> asc.setZone("ru")
>>> asc.setZone("org")
>>> asc.setZone("net")
```

---

### Methods:
- **clear** - Method clear all data
- **setAlphabet** - Method set alphabet
- **getAlphabet** - Method get alphabet

### Example:
```python
>>> import asc
>>>
>>> asc.getAlphabet()
'abcdefghijklmnopqrstuvwxyz'
>>>
>>> asc.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> asc.getAlphabet()
'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
>>>
>>> asc.clear()
>>>
>>> asc.getAlphabet()
'abcdefghijklmnopqrstuvwxyz'
```

---

### Methods:
- **setUnknown** - Method set unknown word
- **getUnknown** - Method extraction unknown word

### Example:
```python
>>> import asc
>>>
>>> asc.setUnknown("word")
>>>
>>> asc.getUnknown()
'word'
```

---

### Methods:
- **infoIndex** - Method for print information about the dictionary
- **token** - Method for determining the type of the token words
- **addText** - Method of adding text for estimate
- **collectCorpus** - Training method of assembling the text data for ASC [curpus = filename or dir, smoothing = wittenBell, modified = False, prepares = False, mod = 0.0, status = Null]
- **pruneVocab** - Dictionary pruning method
- **buildArpa** - Method for build ARPA
- **writeWords** - Method for writing these words to a file
- **writeVocab** - Method for writing dictionary data to a file
- **writeNgrams** - Method of writing data to NGRAMs files
- **writeMap** - Method of writing sequence map to file
- **writeSuffix** - Method for writing data to a suffix file for digital abbreviations
- **writeAbbrs** - Method for writing data to an abbreviation file
- **getSuffixes** - Method for extracting the list of suffixes of digital abbreviations
- **writeArpa** - Method of writing data to ARPA file
- **setThreads** - Method for setting the number of threads used in work (0 - all available threads)
- **setStemmingMethod** - Method for setting external stemming function
- **loadIndex** - Binary index loading method
- **spell** - Method for performing spell-checker
- **analyze** - Method for analyze text
- **addAlt** - Method for add a word/letter with an alternative letter
- **setAlphabet** - Method for set Alphabet
- **setPilots** - Method for set pilot words
- **setSubstitutes** - Method for set letters to correct words from mixed alphabets
- **addAbbr** - Method add abbreviation
- **setAbbrs** - Method set abbreviations
- **getAbbrs** - Method for extracting the list of abbreviations
- **addGoodword** - Method add good word
- **addBadword** - Method add bad word
- **addUWord** - Method for add a word that always starts with a capital letter
- **setUWords** - Method for add a list of identifiers for words that always start with a capital letter
- **readArpa** - Method for reading an ARPA file, language model
- **readVocab** - Method of reading the dictionary
- **setEmbedding** - Method for set embedding
- **buildIndex** - Method for build spell-checker index
- **setAdCw** - Method for set dictionary characteristics (cw - count all words in dataset, ad - count all documents in dataset)
- **setCode** - Method for set code language
- **addLemma** - Method for add a Lemma to the dictionary
- **setNSWLibCount** - Method for set the maximum number of options for analysis

### Example:
```python
>>> import asc
>>> 
>>> asc.infoIndex("./wittenbell-3-single.asc")

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

* Code: RU

* Version: 1.0.0

* Dictionary name: Russian - single

* Locale: en_US.UTF-8
* Alphabet: абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz

* Build date: 09/08/2020 15:39:31

* Encrypted: NO

* ALM type: ALMv1

* Allow apostrophe: NO

* Count words: 106912195
* Count documents: 263998

* Only good words: NO
* Mix words in dicts: YES
* Confidence arpa: YES

* Count upper words: 841915
* Count pilots words: 15
* Count bad words: 108790
* Count good words: 124
* Count substitutes: 14
* Count abbreviations: 16532

* Alternatives: е => ё
* Count alternatives words: 58138

* Size embedding: 28

* Length n-gram: 3
* Count n-grams: 6710202

* Author: Yuriy Lobarev

* Contacts: site: https://anyks.com, e-mail: forman@anyks.com

* Copyright ©: Yuriy Lobarev

* License type: GPLv3
* License text:
The GNU General Public License is a free, copyleft license for software and other kinds of works.

The licenses for most software and other practical works are designed to take away your freedom to share and change the works. By contrast, the GNU General Public License is intended to guarantee your freedom to share and change all versions of a program--to make sure it remains free software for all its users. We, the Free Software Foundation, use the GNU General Public License for most of our software; it applies also to any other work released this way by its authors. You can apply it to your programs, too.

When we speak of free software, we are referring to freedom, not price. Our General Public Licenses are designed to make sure that you have the freedom to distribute copies of free software (and charge for them if you wish), that you receive source code or can get it if you want it, that you can change the software or use pieces of it in new free programs, and that you know you can do these things.

To protect your rights, we need to prevent others from denying you these rights or asking you to surrender the rights. Therefore, you have certain responsibilities if you distribute copies of the software, or if you modify it: responsibilities to respect the freedom of others.

For example, if you distribute copies of such a program, whether gratis or for a fee, you must pass on to the recipients the same freedoms that you received. You must make sure that they, too, receive or can get the source code. And you must show them these terms so they know their rights.

Developers that use the GNU GPL protect your rights with two steps: (1) assert copyright on the software, and (2) offer you this License giving you legal permission to copy, distribute and/or modify it.

For the developers' and authors' protection, the GPL clearly explains that there is no warranty for this free software. For both users' and authors' sake, the GPL requires that modified versions be marked as changed, so that their problems will not be attributed erroneously to authors of previous versions.

Some devices are designed to deny users access to install or run modified versions of the software inside them, although the manufacturer can do so. This is fundamentally incompatible with the aim of protecting users' freedom to change the software. The systematic pattern of such abuse occurs in the area of products for individuals to use, which is precisely where it is most unacceptable. Therefore, we have designed this version of the GPL to prohibit the practice for those products. If such problems arise substantially in other domains, we stand ready to extend this provision to those domains in future versions of the GPL, as needed to protect the freedom of users.

Finally, every program is threatened constantly by software patents. States should not allow patents to restrict development and use of software on general-purpose computers, but in those that do, we wish to avoid the special danger that patents applied to a free program could make it effectively proprietary. To prevent this, the GPL assures that patents cannot be used to render the program non-free.

The precise terms and conditions for copying, distribution and modification follow.

URL: https://www.gnu.org/licenses/gpl-3.0.ru.html

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

```

### Example:
```python
>>> import asc
>>> import spacy
>>> import pymorphy2
>>> 
>>> asc.setThreads(0)
>>> asc.setOption(asc.options_t.ascSplit)
>>> asc.setOption(asc.options_t.ascAlter)
>>> asc.setOption(asc.options_t.ascESplit)
>>> asc.setOption(asc.options_t.ascRSplit)
>>> asc.setOption(asc.options_t.ascUppers)
>>> asc.setOption(asc.options_t.ascHyphen)
>>> asc.setOption(asc.options_t.ascWordRep)
>>> asc.setOption(asc.options_t.mixDicts)
>>> asc.setOption(asc.options_t.confidence)
>>> asc.setOption(asc.options_t.stemming)
>>> 
>>> morphRu = pymorphy2.MorphAnalyzer()
>>> morphEn = spacy.load('en', disable=['parser', 'ner'])
>>> 
>>> def status(text, status):
...     print(text, status)
... 
>>> 
>>> def eng(word):
...     global morphEn
...     words = morphEn(word)
...     word = ''.join([token.lemma_ for token in words]).strip()
...     if word[0] != '-' and word[len(word) - 1] != '-':
...         return word
...     else:
...         return ""
... 
>>> 
>>> def rus(word):
...     global morphRu
...     if morphRu != None:
...         word = morphRu.parse(word)[0].normal_form
...         return word
...     else:
...         return ""
... 
>>> 
>>> def run(word, lang):
...     if lang == "ru":
...         return rus(word.lower())
...     elif lang == "en":
...         return eng(word.lower())
... 
>>> 
>>> asc.setStemmingMethod(run)
>>> 
>>> asc.loadIndex("./wittenbell-3-single.asc", "", status)
Loading dictionary 1
Loading dictionary 2
Loading dictionary 3
Loading dictionary 4
Loading dictionary 5
Loading dictionary 6
Loading dictionary 7
Loading dictionary 8
...
Loading Bloom filter 100
Loading stemming 0
Loading stemming 1
Loading stemming 2
Loading stemming 3
...
Loading language model 6
Loading language model 12
Loading language model 18
Loading language model 25
Loading language model 31
Loading language model 37
...
Loading alternative words 1
Loading alternative words 2
Loading alternative words 3
Loading alternative words 4
Loading alternative words 5
Loading alternative words 6
Loading alternative words 7
...
Loading substitutes letters 7
Loading substitutes letters 14
Loading substitutes letters 21
Loading substitutes letters 28
Loading substitutes letters 35
Loading substitutes letters 42
...
>>> 
>>> res = asc.spell("начальнег зажог павзрослому", True)
>>> res
('начальник зажёг по-взрослому', [('начальнег', 'начальник'), ('зажог', 'зажёг'), ('павзрослому', 'по-взрослому')])
>>> 
>>> res = asc.analyze("слзы теут на мрозе")
>>> res
[('теут', ['текут']), ('мрозе', ['мозг', 'мороз', 'морозе', 'моё']), ('слзы', ['слезы', 'слёзы'])]
```

### Example:
```python
>>> import asc
>>> 
>>> asc.setThreads(0)
>>> asc.setOption(asc.options_t.ascSplit)
>>> asc.setOption(asc.options_t.ascAlter)
>>> asc.setOption(asc.options_t.ascESplit)
>>> asc.setOption(asc.options_t.ascRSplit)
>>> asc.setOption(asc.options_t.ascUppers)
>>> asc.setOption(asc.options_t.ascHyphen)
>>> asc.setOption(asc.options_t.ascWordRep)
>>> asc.setOption(asc.options_t.mixDicts)
>>> asc.setOption(asc.options_t.confidence)
>>> 
>>> asc.addAlt("е", "ё")
>>> asc.addAlt("ежик", "ёжик")
>>> asc.addAlt("Легкий", "Лёгкий")
...
>>> asc.setAlphabet("абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz")
>>> 
>>> asc.setPilots(["а","у","в","о","с","к","б","и","я","э","a","i","o","e","g"])
>>> asc.setSubstitutes({'p':'р','c':'с','o':'о','t':'т','k':'к','e':'е','a':'а','h':'н','x':'х','b':'в','m':'м'})
>>> 
>>> asc.idw("Сбербанк")
13236490857
asc.idw("Совкомбанк")
22287680895
>>> 
>>> asc.token("Сбербанк")
'<word>'
>>> asc.token("совкомбанк")
'<word>'
>>> 
>>> asc.setAbbrs({13236490857, 22287680895})
>>> 
>>> asc.addAbbr("США")
>>> asc.addAbbr("Сбер")
>>> 
>>> asc.token("Сбербанк")
'<abbr>'
>>> asc.token("совкомбанк")
'<abbr>'
>>> asc.token("сша")
'<abbr>'
>>> asc.token("СБЕР")
'<abbr>'
...
>>> asc.getAbbrs()
{13236490857, 189243, 22287680895, 26938511}
>>> 
>>> asc.addGoodword("T-34")
>>> asc.addGoodword("АН-25")
...
>>> asc.addBadword("ийти")
>>> asc.addBadword("циган")
>>> asc.addBadword("апичатка")
...
>>> asc.addUWord("Москва")
>>> asc.addUWord("Санкт-Петербург")
...
>>> def statusArpa(status):
...     print("Read arpa", status)
... 
>>> def statusVocab(status):
...     print("Read vocab", status)
... 
>>> def statusIndex(status):
...     print("Build index", status)
... 
>>> asc.readArpa("./words.arpa", statusArpa)
Read arpa 0
Read arpa 1
Read arpa 2
Read arpa 3
Read arpa 4
Read arpa 5
Read arpa 6
Read arpa 7
Read arpa 8
...
>>> asc.readVocab("./words.vocab", statusVocab)
Read vocab 0
Read vocab 1
Read vocab 2
Read vocab 3
Read vocab 4
Read vocab 5
Read vocab 6
...
>>> asc.setEmbedding({
...     "а": 0, "б": 1, "в": 2, "г": 3, "д": 4, "е": 5,
...     "ё": 5, "ж": 6, "з": 7, "и": 8, "й": 8, "к": 9,
...     "л": 10, "м": 11, "н": 12, "о": 0, "п": 13, "р": 14,
...     "с": 15, "т": 16, "у": 17, "ф": 18, "х": 19, "ц": 20,
...     "ч": 21, "ш": 21, "щ": 21, "ъ": 22, "ы": 23, "ь": 22,
...     "э": 5, "ю": 24, "я": 25, "<": 26, ">": 26, "~": 26,
...     "-": 26, "+": 26, "=": 26, "*": 26, "/": 26, ":": 26,
...     "%": 26, "|": 26, "^": 26, "&": 26, "#": 26, "'": 26,
...     "\\": 26, "0": 27, "1": 27, "2": 27, "3": 27, "4": 27,
...     "5": 27, "6": 27, "7": 27, "8": 27, "9": 27, "a": 0,
...     "b": 2, "c": 15, "d": 4, "e": 5, "f": 18, "g": 3,
...     "h": 12, "i": 8, "j": 6, "k": 9, "l": 10, "m": 11,
...     "n": 12, "o": 0, "p": 14, "q": 13, "r": 14, "s": 15,
...     "t": 16, "u": 24, "v": 21, "w": 22, "x": 19, "y": 17, "z": 7
... }, 28)
>>> 
>>> asc.buildIndex(statusIndex)
Build index 0
Build index 1
Build index 2
Build index 3
Build index 4
...
>>> res = asc.spell("начальнег зажог павзрослому", True)
>>> res
('начальник зажег по-взрослому', [('начальнег', 'начальник'), ('зажог', 'зажег'), ('павзрослому', 'по-взрослому')])
>>> 
>>> res = asc.analyze("слзы теут на мрозе")
>>> res
[('теут', ['текут']), ('мрозе', ['мозг', 'мороз', 'морозе', 'моё']), ('слзы', ['слезы', 'слёзы'])]
```

### Example:
```python
>>> import asc
>>> 
>>> asc.setThreads(0)
>>> asc.setOption(asc.options_t.ascSplit)
>>> asc.setOption(asc.options_t.ascAlter)
>>> asc.setOption(asc.options_t.ascESplit)
>>> asc.setOption(asc.options_t.ascRSplit)
>>> asc.setOption(asc.options_t.ascUppers)
>>> asc.setOption(asc.options_t.ascHyphen)
>>> asc.setOption(asc.options_t.ascWordRep)
>>> asc.setOption(asc.options_t.mixDicts)
>>> asc.setOption(asc.options_t.confidence)
>>> 
>>> asc.addAlt("е", "ё")
>>> asc.addAlt("ежик", "ёжик")
>>> asc.addAlt("зажег", "зажёг")
>>> asc.addAlt("Легкий", "Лёгкий")
...
>>> asc.setAlphabet("абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz")
>>> 
>>> asc.setPilots(["а","у","в","о","с","к","б","и","я","э","a","i","o","e","g"])
>>> asc.setSubstitutes({'p':'р','c':'с','o':'о','t':'т','k':'к','e':'е','a':'а','h':'н','x':'х','b':'в','m':'м'})
>>> 
>>> asc.addAbbr("США")
>>> asc.addAbbr("Сбер")
...
>>> asc.addGoodword("T-34")
>>> asc.addGoodword("АН-25")
...
>>> asc.addBadword("ийти")
>>> asc.addBadword("циган")
>>> asc.addBadword("апичатка")
...
>>> asc.idw("Москва")
50387419219
>>> asc.idw("Санкт-Петербург")
68256898625
>>> 
>>> asc.setUWords({50387419219: 1, 68256898625: 1})
>>> 
...
>>> def statusArpa(status):
...     print("Read arpa", status)
... 
>>> def statusIndex(status):
...     print("Build index", status)
... 
>>> asc.readArpa("./words.arpa", statusArpa)
Read arpa 0
Read arpa 1
Read arpa 2
Read arpa 3
Read arpa 4
Read arpa 5
Read arpa 6
Read arpa 7
Read arpa 8
...
>>> asc.setAdCw(38120, 13)
>>> 
>>> asc.setEmbedding({
...     "а": 0, "б": 1, "в": 2, "г": 3, "д": 4, "е": 5,
...     "ё": 5, "ж": 6, "з": 7, "и": 8, "й": 8, "к": 9,
...     "л": 10, "м": 11, "н": 12, "о": 0, "п": 13, "р": 14,
...     "с": 15, "т": 16, "у": 17, "ф": 18, "х": 19, "ц": 20,
...     "ч": 21, "ш": 21, "щ": 21, "ъ": 22, "ы": 23, "ь": 22,
...     "э": 5, "ю": 24, "я": 25, "<": 26, ">": 26, "~": 26,
...     "-": 26, "+": 26, "=": 26, "*": 26, "/": 26, ":": 26,
...     "%": 26, "|": 26, "^": 26, "&": 26, "#": 26, "'": 26,
...     "\\": 26, "0": 27, "1": 27, "2": 27, "3": 27, "4": 27,
...     "5": 27, "6": 27, "7": 27, "8": 27, "9": 27, "a": 0,
...     "b": 2, "c": 15, "d": 4, "e": 5, "f": 18, "g": 3,
...     "h": 12, "i": 8, "j": 6, "k": 9, "l": 10, "m": 11,
...     "n": 12, "o": 0, "p": 14, "q": 13, "r": 14, "s": 15,
...     "t": 16, "u": 24, "v": 21, "w": 22, "x": 19, "y": 17, "z": 7
... }, 28)
>>> 
>>> asc.buildIndex(statusIndex)
Build index 0
Build index 1
Build index 2
Build index 3
Build index 4
...
>>> res = asc.spell("начальнег зажог павзрослому", True)
>>> res
('начальник зажёг по-взрослому', [('начальнег', 'начальник'), ('зажог', 'зажёг'), ('павзрослому', 'по-взрослому')])
>>> 
>>> res = asc.analyze("слзы теут на мрозе")
>>> res
[('теут', ['текут']), ('мрозе', ['мозг', 'мороз', 'морозе', 'моё']), ('слзы', ['слезы', 'слёзы'])]
```

### Example:
```python
>>> import asc
>>> import spacy
>>> import pymorphy2
>>> 
>>> asc.setThreads(0)
>>> asc.setOption(asc.options_t.ascSplit)
>>> asc.setOption(asc.options_t.ascAlter)
>>> asc.setOption(asc.options_t.ascESplit)
>>> asc.setOption(asc.options_t.ascRSplit)
>>> asc.setOption(asc.options_t.ascUppers)
>>> asc.setOption(asc.options_t.ascHyphen)
>>> asc.setOption(asc.options_t.ascWordRep)
>>> asc.setOption(asc.options_t.mixDicts)
>>> asc.setOption(asc.options_t.confidence)
>>> asc.setOption(asc.options_t.stemming)
>>> 
>>> asc.addAlt("е", "ё")
>>> asc.addAlt("ежик", "ёжик")
>>> asc.addAlt("зажег", "зажёг")
>>> asc.addAlt("Легкий", "Лёгкий")
...
>>> asc.setAlphabet("абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz")
>>> 
>>> asc.setPilots(["а","у","в","о","с","к","б","и","я","э","a","i","o","e","g"])
>>> asc.setSubstitutes({'p':'р','c':'с','o':'о','t':'т','k':'к','e':'е','a':'а','h':'н','x':'х','b':'в','m':'м'})
>>> 
>>> asc.addAbbr("США")
>>> asc.addAbbr("Сбер")
...
>>> asc.addGoodword("T-34")
>>> asc.addGoodword("АН-25")
...
>>> asc.addBadword("ийти")
>>> asc.addBadword("циган")
>>> asc.addBadword("апичатка")
...
>>> asc.addUWord("Москва")
>>> asc.addUWord("Санкт-Петербург")
...
>>> morphRu = pymorphy2.MorphAnalyzer()
>>> morphEn = spacy.load('en', disable=['parser', 'ner'])
>>> 
>>> def statusArpa(status):
...     print("Read arpa", status)
... 
>>> def statusIndex(status):
...     print("Build index", status)
... 
>>> def statusStemming(status):
...    print("Build stemming", status)
...
>>> def eng(word):
...     global morphEn
...     words = morphEn(word)
...     word = ''.join([token.lemma_ for token in words]).strip()
...     if word[0] != '-' and word[len(word) - 1] != '-':
...         return word
...     else:
...         return ""
... 
>>> def rus(word):
...     global morphRu
...     if morphRu != None:
...         word = morphRu.parse(word)[0].normal_form
...         return word
...     else:
...         return ""
... 
>>> def run(word, lang):
...     if lang == "ru":
...         return rus(word.lower())
...     elif lang == "en":
...         return eng(word.lower())
... 
>>> asc.readArpa("./words.arpa", statusArpa)
Read arpa 0
Read arpa 1
Read arpa 2
Read arpa 3
Read arpa 4
Read arpa 5
Read arpa 6
Read arpa 7
Read arpa 8
...
>>> asc.setAdCw(38120, 13)
>>> 
>>> asc.setEmbedding({
...     "а": 0, "б": 1, "в": 2, "г": 3, "д": 4, "е": 5,
...     "ё": 5, "ж": 6, "з": 7, "и": 8, "й": 8, "к": 9,
...     "л": 10, "м": 11, "н": 12, "о": 0, "п": 13, "р": 14,
...     "с": 15, "т": 16, "у": 17, "ф": 18, "х": 19, "ц": 20,
...     "ч": 21, "ш": 21, "щ": 21, "ъ": 22, "ы": 23, "ь": 22,
...     "э": 5, "ю": 24, "я": 25, "<": 26, ">": 26, "~": 26,
...     "-": 26, "+": 26, "=": 26, "*": 26, "/": 26, ":": 26,
...     "%": 26, "|": 26, "^": 26, "&": 26, "#": 26, "'": 26,
...     "\\": 26, "0": 27, "1": 27, "2": 27, "3": 27, "4": 27,
...     "5": 27, "6": 27, "7": 27, "8": 27, "9": 27, "a": 0,
...     "b": 2, "c": 15, "d": 4, "e": 5, "f": 18, "g": 3,
...     "h": 12, "i": 8, "j": 6, "k": 9, "l": 10, "m": 11,
...     "n": 12, "o": 0, "p": 14, "q": 13, "r": 14, "s": 15,
...     "t": 16, "u": 24, "v": 21, "w": 22, "x": 19, "y": 17, "z": 7
... }, 28)
>>> 
>>> asc.setCode("ru")
>>> 
>>> asc.buildIndex(statusIndex)
Build index 0
Build index 1
Build index 2
Build index 3
Build index 4
...
>>> asc.setStemmingMethod(run)
>>>
>>> asc.buildStemming(statusStemming)
Build stemming 0
Build stemming 1
Build stemming 2
Build stemming 3
Build stemming 4
Build stemming 5
...
>>> asc.addLemma("говорил")
>>> asc.addLemma("ходить")
...
>>> asc.setNSWLibCount(50000)
>>> 
>>> res = asc.spell("начальнег зажог павзрослому", True)
>>> res
('начальник зажёг по-взрослому', [('начальнег', 'начальник'), ('зажог', 'зажёг'), ('павзрослому', 'по-взрослому')])
>>> 
>>> res = asc.analyze("слзы теут на мрозе")
>>> res
[('теут', ['текут']), ('мрозе', ['мозг', 'мороз', 'морозе', 'моё']), ('слзы', ['слезы', 'слёзы'])]
```

---

### Methods:
- **setOption** - Library options setting method
- **unsetOption** - Disable module option method

### Example:
```python
>>> import asc
>>>
>>> asc.unsetOption(asc.options_t.debug)
>>> asc.unsetOption(asc.options_t.mixDicts)
>>> asc.unsetOption(asc.options_t.onlyGood)
>>> asc.unsetOption(asc.options_t.confidence)
...
```

#### Description
| Options     | Description                                                                              |
|-------------|------------------------------------------------------------------------------------------|
| debug       | Flag debug mode                                                                          |
| bloom       | Flag allowed to use Bloom filter to check words                                          |
| uppers      | Flag that allows you to correct the case of letters                                      |
| stemming    | Flag for stemming activation                                                             |
| onlyGood    | Flag allowing to consider words from the white list only                                 |
| mixDicts    | Flag allowing the use of words consisting of mixed dictionaries                          |
| allowUnk    | Flag allowing to unknown word                                                            |
| resetUnk    | Flag to reset the frequency of an unknown word                                           |
| allGrams    | Flag allowing accounting of all collected n-grams                                        |
| onlyTypos   | Flag to only correct typos                                                               |
| lowerCase   | Flag allowing to case-insensitive                                                        |
| confidence  | Flag arpa file loading without pre-processing the words                                  |
| tokenWords  | Flag that takes into account when assembling N-grams, only those tokens that match words |
| interpolate | Flag allowing to use interpolation in estimating                                         |
| ascSplit    | Flag to allow splitting of merged words                                                  |
| ascAlter    | Flag that allows you to replace alternative letters in words                             |
| ascESplit   | Flag to allow splitting of misspelled concatenated words                                 |
| ascRSplit   | Flag that allows you to combine words separated by a space                               |
| ascUppers   | Flag that allows you to correct the case of letters                                      |
| ascHyphen   | Flag to allow splitting of concatenated words with hyphens                               |
| ascSkipUpp  | Flag to skip uppercase words                                                             |
| ascSkipLat  | Flag allowing words in the latin alphabet to be skipped                                  |
| ascSkipHyp  | Flag to skip hyphenated words                                                            |
| ascWordRep  | Flag that allows you to remove duplicate words                                           |

---

### Methods:
- **erratum** - Method for search typos in text
- **token** - Method for determining the type of the token words
- **split** - Method for performing a split of clumped words
- **splitByHyphens** - Method for performing a split of clumped words by hyphens
- **check** - Method for checking a word for its existence in the dictionary

### Example:
```python
>>> import asc
>>> 
>>> asc.setThreads(0)
>>> asc.setOption(asc.options_t.ascSplit)
>>> asc.setOption(asc.options_t.ascAlter)
>>> asc.setOption(asc.options_t.ascESplit)
>>> asc.setOption(asc.options_t.ascRSplit)
>>> asc.setOption(asc.options_t.ascUppers)
>>> asc.setOption(asc.options_t.ascHyphen)
>>> asc.setOption(asc.options_t.ascWordRep)
>>> asc.setOption(asc.options_t.mixDicts)
>>> asc.setOption(asc.options_t.confidence)
>>> 
>>> def status(text, status):
...     print(text, status)
... 
>>> 
>>> asc.loadIndex("./wittenbell-3-single.asc", "", status)
Loading dictionary 1
Loading dictionary 2
Loading dictionary 3
Loading dictionary 4
Loading dictionary 5
Loading dictionary 6
Loading dictionary 7
Loading dictionary 8
...
Loading Bloom filter 100
Loading stemming 100
Loading language model 6
Loading language model 12
Loading language model 18
Loading language model 25
Loading language model 31
Loading language model 37
...
Loading alternative words 1
Loading alternative words 2
Loading alternative words 3
Loading alternative words 4
Loading alternative words 5
Loading alternative words 6
Loading alternative words 7
...
Loading substitutes letters 7
Loading substitutes letters 14
Loading substitutes letters 21
Loading substitutes letters 28
Loading substitutes letters 35
Loading substitutes letters 42
...
>>> 
asc.erratum("начальнег зажёг павзрослому")
['начальнег', 'павзрослому']
>>> 
asc.token("word")
'<word>'
>>> asc.token("12")
'<num>'
>>> asc.token("127.0.0.1")
'<url>'
>>> asc.token("14-33")
'<range>'
>>> asc.token("14:44:22")
'<time>'
>>> asc.token("08/02/2020")
'<date>'
>>> 
>>> asc.split("приветкакдела")
'привет как Дела'
>>> asc.split("былмастеромпрятатьсянонемогвоспользоватьсясвоимиталантамипотому")
'был мастером прятаться но не мог воспользоваться своими талантами потому'
>>> asc.split("Ябинатакойсоставбысходилеслиб")
'я б и на такой состав бы сходил если б'
>>> asc.split("летчерезXVIретроспективнопросматриватьэтобудет")
'лет через XVI ретроспективно просматривать это будет'
>>> 
>>> asc.splitByHyphens("привет-как-дела")
'привет как дела'
>>> asc.splitByHyphens("как-то-так")
'как то так'
>>> asc.splitByHyphens("как-то")
'как-то'
>>> 
>>> asc.check("hello")
True
>>> asc.check("Шварценеггер")
True
>>> asc.check("прывет")
False
```

---

### Methods:
- **setSize** - Method for set size N-gram
- **setAlmV2** - Method for set the language model type ALMv2
- **unsetAlmV2** - Method for unset the language model type ALMv2
- **setLocale** - Method set locale (Default: en_US.UTF-8)
- **setCode** - Method for set code language
- **setLictype** - Method for set dictionary license information type
- **setName** - Method for set dictionary name
- **setAuthor** - Method for set the dictionary author
- **setCopyright** - Method for set copyright on a dictionary
- **setLictext** - Method for set license information dictionary
- **setContacts** - Method for set contact details of the dictionary author
- **pruneArpa** - Language model pruning method
- **addWord** - Method for add a word to the dictionary
- **generateEmbedding** - Method for generation embedding
- **setSizeEmbedding** - Method for set the embedding size

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
>>> import asc
>>> 
>>> asc.setSize(3)
>>> asc.setAlmV2()
>>> asc.setThreads(0)
>>> asc.setLocale("en_US.UTF-8")
>>> 
>>> asc.setOption(asc.options_t.allowUnk)
>>> asc.setOption(asc.options_t.resetUnk)
>>> asc.setOption(asc.options_t.mixDicts)
>>> asc.setOption(asc.options_t.tokenWords)
>>> asc.setOption(asc.options_t.confidence)
>>> asc.setOption(asc.options_t.interpolate)
>>> 
>>> asc.addAlt("е", "ё")
>>> asc.addAlt("ежик", "ёжик")
>>> asc.addAlt("зажег", "зажёг")
>>> asc.addAlt("Легкий", "Лёгкий")
>>> 
>>> asc.setAlphabet("абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz")
>>> 
>>> asc.setPilots(["а","у","в","о","с","к","б","и","я","э","a","i","o","e","g"])
>>> asc.setSubstitutes({'p':'р','c':'с','o':'о','t':'т','k':'к','e':'е','a':'а','h':'н','x':'х','b':'в','m':'м'})
>>> 
>>> asc.addAbbr("США")
>>> asc.addAbbr("Сбер")
>>> asc.addGoodword("T-34")
>>> asc.addGoodword("АН-25")
>>> 
>>> asc.addBadword("ийти")
>>> asc.addBadword("циган")
>>> asc.addBadword("апичатка")
>>> 
>>> asc.addUWord("Москва")
>>> asc.addUWord("Санкт-Петербург")
>>> 
>>> def statusMap(status):
...     print("Write map", status)
... 
>>> def statusArpa1(status):
...     print("Build arpa", status)
... 
>>> def statusArpa2(status):
...     print("Write arpa", status)
... 
>>> def statusWords(status):
...     print("Write words", status)
... 
>>> def statusVocab(status):
...     print("Write vocab", status)
... 
>>> def statusAbbrs(status):
...     print("Write abbrs", status)
... 
>>> def statusPrune(status):
...     print("Prune vocab", status)
... 
>>> def statusNgram(status):
...     print("Write ngram", status)
... 
>>> def statusIndex(status):
...     print("Build index", status)
... 
>>> def status(text, status):
...     print(text, status)
... 
>>> asc.addText("The future is now", 0)
>>> 
>>> asc.collectCorpus("./corpus/text.txt", asc.smoothing_t.wittenBell, 0.0, False, False, status)
Read text corpora 0
Read text corpora 1
Read text corpora 2
Read text corpora 3
Read text corpora 4
Read text corpora 5
Read text corpora 6
...
>>> asc.pruneVocab(-15.0, 0, 0, statusPrune)
Prune vocab 0
Prune vocab 1
Prune vocab 2
Prune vocab 3
Prune vocab 4
Prune vocab 5
Prune vocab 6
...
# Prune VOCAB or prune ARPA example
>>> asc.pruneArpa(0.015, 3, statusPrune)
Prune arpa 0
Prune arpa 1
Prune arpa 2
Prune arpa 3
Prune arpa 4
Prune arpa 5
Prune arpa 6
...
>>> asc.buildArpa(statusArpa1)
Build arpa 0
Build arpa 1
Build arpa 2
Build arpa 3
Build arpa 4
Build arpa 5
Build arpa 6
...
>>> asc.writeMap("./words.map", statusMap)
Write map 0
Write map 1
Write map 2
Write map 3
Write map 4
Write map 5
Write map 6
...
>>> asc.writeArpa("./words.arpa", statusArpa2)
Write arpa 0
Write arpa 1
Write arpa 2
Write arpa 3
Write arpa 4
Write arpa 5
Write arpa 6
...
>>> asc.writeWords("./words.txt", statusWords)
Write words 0
Write words 1
Write words 2
Write words 3
Write words 4
Write words 5
Write words 6
...
>>> asc.writeVocab("./words.vocab", statusVocab)
Write vocab 0
Write vocab 1
Write vocab 2
Write vocab 3
Write vocab 4
Write vocab 5
Write vocab 6
...
>>> asc.writeAbbrs("./words1.abbr", statusAbbrs)
Write abbrs 50
Write abbrs 100
>>> 
>>> asc.writeSuffix("./words2.abbr", statusAbbrs)
Write abbrs 10
Write abbrs 20
Write abbrs 30
Write abbrs 40
Write abbrs 50
Write abbrs 60
...
>>> asc.writeNgrams("./words.ngram", statusNgram)
Write ngram 0
Write ngram 1
Write ngram 2
Write ngram 3
Write ngram 4
Write ngram 5
Write ngram 6
...
>>> asc.setCode("RU")
>>> asc.setLictype("MIT")
>>> asc.setName("Russian")
>>> asc.setAuthor("You name")
>>> asc.setCopyright("You company LLC")
>>> asc.setLictext("... License text ...")
>>> asc.setContacts("site: https://example.com, e-mail: info@example.com")
>>> 
>>> asc.setEmbedding({
...     "а": 0, "б": 1, "в": 2, "г": 3, "д": 4, "е": 5,
...     "ё": 5, "ж": 6, "з": 7, "и": 8, "й": 8, "к": 9,
...     "л": 10, "м": 11, "н": 12, "о": 0, "п": 13, "р": 14,
...     "с": 15, "т": 16, "у": 17, "ф": 18, "х": 19, "ц": 20,
...     "ч": 21, "ш": 21, "щ": 21, "ъ": 22, "ы": 23, "ь": 22,
...     "э": 5, "ю": 24, "я": 25, "<": 26, ">": 26, "~": 26,
...     "-": 26, "+": 26, "=": 26, "*": 26, "/": 26, ":": 26,
...     "%": 26, "|": 26, "^": 26, "&": 26, "#": 26, "'": 26,
...     "\\": 26, "0": 27, "1": 27, "2": 27, "3": 27, "4": 27,
...     "5": 27, "6": 27, "7": 27, "8": 27, "9": 27, "a": 0,
...     "b": 2, "c": 15, "d": 4, "e": 5, "f": 18, "g": 3,
...     "h": 12, "i": 8, "j": 6, "k": 9, "l": 10, "m": 11,
...     "n": 12, "o": 0, "p": 14, "q": 13, "r": 14, "s": 15,
...     "t": 16, "u": 24, "v": 21, "w": 22, "x": 19, "y": 17, "z": 7
... }, 28)
>>> 
>> asc.saveIndex("./3-wittenbell.asc", "", 128, status)
Read words 1
Read words 2
Read words 3
Read words 4
Read words 5
Read words 6
...
Train dictionary 0
Train dictionary 1
Train dictionary 2
Train dictionary 3
Train dictionary 4
Train dictionary 5
Train dictionary 6
...
Dump dictionary 0
Dump dictionary 1
Dump dictionary 2
Dump dictionary 3
Dump dictionary 4
Dump dictionary 5
Dump dictionary 6
...
Dump alternative letters 100
Dump alternative letters 100
Dump alternative words 200
Dump alternative words 100
Dump language model 0
Dump language model 100
Dump substitutes letters 9
Dump substitutes letters 18
Dump substitutes letters 27
Dump substitutes letters 36
Dump substitutes letters 45
Dump substitutes letters 54
Dump substitutes letters 63
Dump substitutes letters 72
Dump substitutes letters 81
Dump substitutes letters 90
Dump substitutes letters 100
Dump substitutes letters 100
>>>
>>> asc.infoIndex("./3-wittenbell.asc")

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

* Code: RU

* Version: 1.0.0

* Dictionary name: Russian

* Locale: en_US.UTF-8
* Alphabet: абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz

* Build date: 09/14/2020 01:39:50

* Encrypted: NO

* ALM type: ALMv2

* Allow apostrophe: NO

* Count words: 38120
* Count documents: 13

* Only good words: NO
* Mix words in dicts: YES
* Confidence arpa: YES

* Count upper words: 2
* Count pilots words: 15
* Count bad words: 3
* Count good words: 2
* Count substitutes: 11
* Count abbreviations: 12

* Alternatives: е => ё
* Count alternatives words: 1

* Size embedding: 28

* Length n-gram: 1

* Author: You name

* Contacts: site: https://example.com, e-mail: info@example.com

* Copyright ©: You company LLC

* License type: MIT
* License text:
... License text ...

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

```

### Example:
```python
>>> import asc
>>> 
>>> asc.setSize(3)
>>> asc.setThreads(0)
>>> asc.setLocale("en_US.UTF-8")
>>> 
>>> asc.setOption(asc.options_t.allowUnk)
>>> asc.setOption(asc.options_t.resetUnk)
>>> asc.setOption(asc.options_t.mixDicts)
>>> asc.setOption(asc.options_t.tokenWords)
>>> asc.setOption(asc.options_t.confidence)
>>> asc.setOption(asc.options_t.interpolate)
>>> 
>>> asc.addAlt("е", "ё")
>>> asc.addAlt("Легкий", "Лёгкий")
>>> 
>>> asc.setAlphabet("абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz")
>>> 
>>> asc.setPilots(["а","у","в","о","с","к","б","и","я","э","a","i","o","e","g"])
>>> asc.setSubstitutes({'p':'р','c':'с','o':'о','t':'т','k':'к','e':'е','a':'а','h':'н','x':'х','b':'в','m':'м'})
>>> 
>>> asc.addAbbr("США")
>>> asc.addAbbr("Сбер")
>>> asc.addGoodword("T-34")
>>> asc.addGoodword("АН-25")
>>> 
>>> asc.addBadword("ийти")
>>> asc.addBadword("циган")
>>> asc.addBadword("апичатка")
>>> 
>>> asc.addUWord("Москва")
>>> asc.addUWord("Санкт-Петербург")
>>> 
>>> def statusArpa(status):
...     print("Read arpa", status)
... 
>>> def statusVocab(status):
...     print("Read vocab", status)
... 
>>> def statusIndex(status):
...     print("Build index", status)
...
>>> def status(text, status):
...     print(text, status)
... 
>>> asc.readArpa("./words.arpa", statusArpa)
Read arpa 0
Read arpa 1
Read arpa 2
Read arpa 3
Read arpa 4
Read arpa 5
Read arpa 6
...
>>> asc.readVocab("./words.vocab", statusVocab)
Read vocab 0
Read vocab 1
Read vocab 2
Read vocab 3
Read vocab 4
Read vocab 5
Read vocab 6
...
>>> asc.setCode("RU")
>>> asc.setLictype("MIT")
>>> asc.setName("Russian")
>>> asc.setAuthor("You name")
>>> asc.setCopyright("You company LLC")
>>> asc.setLictext("... License text ...")
>>> asc.setContacts("site: https://example.com, e-mail: info@example.com")
>>> 
>>> asc.setEmbedding({
...     "а": 0, "б": 1, "в": 2, "г": 3, "д": 4, "е": 5,
...     "ё": 5, "ж": 6, "з": 7, "и": 8, "й": 8, "к": 9,
...     "л": 10, "м": 11, "н": 12, "о": 0, "п": 13, "р": 14,
...     "с": 15, "т": 16, "у": 17, "ф": 18, "х": 19, "ц": 20,
...     "ч": 21, "ш": 21, "щ": 21, "ъ": 22, "ы": 23, "ь": 22,
...     "э": 5, "ю": 24, "я": 25, "<": 26, ">": 26, "~": 26,
...     "-": 26, "+": 26, "=": 26, "*": 26, "/": 26, ":": 26,
...     "%": 26, "|": 26, "^": 26, "&": 26, "#": 26, "'": 26,
...     "\\": 26, "0": 27, "1": 27, "2": 27, "3": 27, "4": 27,
...     "5": 27, "6": 27, "7": 27, "8": 27, "9": 27, "a": 0,
...     "b": 2, "c": 15, "d": 4, "e": 5, "f": 18, "g": 3,
...     "h": 12, "i": 8, "j": 6, "k": 9, "l": 10, "m": 11,
...     "n": 12, "o": 0, "p": 14, "q": 13, "r": 14, "s": 15,
...     "t": 16, "u": 24, "v": 21, "w": 22, "x": 19, "y": 17, "z": 7
... }, 28)
>>> 
>>> asc.buildIndex(statusIndex)
Build index 0
Build index 1
Build index 2
Build index 3
Build index 4
Build index 5
Build index 6
...
>>> asc.saveIndex("./3-wittenbell.asc", "", 128, status)
Dump dictionary 0
Dump dictionary 1
Dump dictionary 2
Dump dictionary 3
Dump dictionary 4
Dump dictionary 5
Dump dictionary 6
...
Dump alternative letters 100
Dump alternative letters 100
Dump alternative words 200
Dump alternative words 100
Dump language model 0
Dump language model 100
Dump substitutes letters 9
Dump substitutes letters 18
Dump substitutes letters 27
Dump substitutes letters 36
Dump substitutes letters 45
Dump substitutes letters 54
Dump substitutes letters 63
Dump substitutes letters 72
Dump substitutes letters 81
Dump substitutes letters 90
Dump substitutes letters 100
Dump substitutes letters 100
>>>
>>> asc.infoIndex("./3-wittenbell.asc")

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

* Code: RU

* Version: 1.0.0

* Dictionary name: Russian

* Locale: en_US.UTF-8
* Alphabet: абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz

* Build date: 09/14/2020 01:58:52

* Encrypted: NO

* ALM type: ALMv1

* Allow apostrophe: NO

* Count words: 38120
* Count documents: 13

* Only good words: NO
* Mix words in dicts: YES
* Confidence arpa: YES

* Count upper words: 2
* Count pilots words: 15
* Count bad words: 3
* Count good words: 2
* Count substitutes: 11
* Count abbreviations: 2

* Alternatives: е => ё
* Count alternatives words: 1

* Size embedding: 28

* Length n-gram: 3
* Count n-grams: 353

* Author: You name

* Contacts: site: https://example.com, e-mail: info@example.com

* Copyright ©: You company LLC

* License type: MIT
* License text:
... License text ...

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

```

### Example:
```python
>>> import asc
>>> 
>>> asc.setSize(3)
>>> asc.setAlmV2()
>>> asc.setThreads(0)
>>> asc.setLocale("en_US.UTF-8")
>>> 
>>> asc.setOption(asc.options_t.allowUnk)
>>> asc.setOption(asc.options_t.resetUnk)
>>> asc.setOption(asc.options_t.mixDicts)
>>> asc.setOption(asc.options_t.tokenWords)
>>> asc.setOption(asc.options_t.confidence)
>>> asc.setOption(asc.options_t.interpolate)
>>> 
>>> asc.addAlt("е", "ё")
>>> asc.addAlt("Легкий", "Лёгкий")
>>> 
>>> asc.setAlphabet("абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz")
>>> 
>>> asc.setPilots(["а","у","в","о","с","к","б","и","я","э","a","i","o","e","g"])
>>> asc.setSubstitutes({'p':'р','c':'с','o':'о','t':'т','k':'к','e':'е','a':'а','h':'н','x':'х','b':'в','m':'м'})
>>> 
>>> asc.addAbbr("США")
>>> asc.addAbbr("Сбер")
>>> asc.addGoodword("T-34")
>>> asc.addGoodword("АН-25")
>>> 
>>> asc.addBadword("ийти")
>>> asc.addBadword("циган")
>>> asc.addBadword("апичатка")
>>> 
>>> asc.addUWord("Москва")
>>> asc.addUWord("Санкт-Петербург")
>>> 
>>> def statusArpa(status):
...     print("Read arpa", status)
... 
>>> def statusIndex(status):
...     print("Build index", status)
... 
>>> def statusPrune(status):
...     print("Prune arpa", status)
... 
>>> def status(text, status):
...     print(text, status)
... 
>>> asc.readArpa("./words.arpa", statusArpa)
Read arpa 0
Read arpa 1
Read arpa 2
Read arpa 3
Read arpa 4
Read arpa 5
Read arpa 6
...
>>> asc.setAdCw(38120, 13)
>>> 
>>> asc.addWord("министерство")
>>> asc.addWord("возмездие", 0, 1)
>>> asc.addWord("возражение", asc.idw("возражение"), 2)
...
>>> 
>>> asc.setCode("RU")
>>> asc.setLictype("MIT")
>>> asc.setName("Russian")
>>> asc.setAuthor("You name")
>>> asc.setCopyright("You company LLC")
>>> asc.setLictext("... License text ...")
>>> asc.setContacts("site: https://example.com, e-mail: info@example.com")
>>> 
>>> asc.setEmbedding({
...     "а": 0, "б": 1, "в": 2, "г": 3, "д": 4, "е": 5,
...     "ё": 5, "ж": 6, "з": 7, "и": 8, "й": 8, "к": 9,
...     "л": 10, "м": 11, "н": 12, "о": 0, "п": 13, "р": 14,
...     "с": 15, "т": 16, "у": 17, "ф": 18, "х": 19, "ц": 20,
...     "ч": 21, "ш": 21, "щ": 21, "ъ": 22, "ы": 23, "ь": 22,
...     "э": 5, "ю": 24, "я": 25, "<": 26, ">": 26, "~": 26,
...     "-": 26, "+": 26, "=": 26, "*": 26, "/": 26, ":": 26,
...     "%": 26, "|": 26, "^": 26, "&": 26, "#": 26, "'": 26,
...     "\\": 26, "0": 27, "1": 27, "2": 27, "3": 27, "4": 27,
...     "5": 27, "6": 27, "7": 27, "8": 27, "9": 27, "a": 0,
...     "b": 2, "c": 15, "d": 4, "e": 5, "f": 18, "g": 3,
...     "h": 12, "i": 8, "j": 6, "k": 9, "l": 10, "m": 11,
...     "n": 12, "o": 0, "p": 14, "q": 13, "r": 14, "s": 15,
...     "t": 16, "u": 24, "v": 21, "w": 22, "x": 19, "y": 17, "z": 7
... }, 28)
>>> 
>>> asc.buildIndex(statusIndex)
Build index 0
Build index 1
Build index 2
Build index 3
Build index 4
Build index 5
Build index 6
...
>>> asc.saveIndex("./3-wittenbell.asc", "password", 128, status)
Dump dictionary 0
Dump dictionary 1
Dump dictionary 2
Dump dictionary 3
Dump dictionary 4
Dump dictionary 5
Dump dictionary 6
...
Dump alternative letters 100
Dump alternative letters 100
Dump alternative words 200
Dump alternative words 100
Dump language model 0
Dump language model 100
Dump substitutes letters 9
Dump substitutes letters 18
Dump substitutes letters 27
Dump substitutes letters 36
Dump substitutes letters 45
Dump substitutes letters 54
Dump substitutes letters 63
Dump substitutes letters 72
Dump substitutes letters 81
Dump substitutes letters 90
Dump substitutes letters 100
Dump substitutes letters 100
>>>
>>> asc.infoIndex("./3-wittenbell.asc")

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

* Code: RU

* Version: 1.0.0

* Dictionary name: Russian

* Build date: 09/14/2020 02:09:38

* Encrypted: YES

* ALM type: ALMv2

* Allow apostrophe: NO

* Count words: 38120
* Count documents: 13

* Only good words: NO
* Mix words in dicts: YES
* Confidence arpa: YES

* Count upper words: 2
* Count pilots words: 15
* Count bad words: 3
* Count good words: 2
* Count substitutes: 11
* Count abbreviations: 2

* Alternatives: е => ё
* Count alternatives words: 1

* Size embedding: 28

* Length n-gram: 3
* Count n-grams: 353

* Author: You name

* Contacts: site: https://example.com, e-mail: info@example.com

* Copyright ©: You company LLC

* License type: MIT
* License text:
... License text ...

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

```

### Example:
```python
>>> import asc
>>> 
>>> asc.setSize(3)
>>> asc.setAlmV2()
>>> asc.setThreads(0)
>>> asc.setLocale("en_US.UTF-8")
>>> 
>>> asc.setOption(asc.options_t.allowUnk)
>>> asc.setOption(asc.options_t.resetUnk)
>>> asc.setOption(asc.options_t.mixDicts)
>>> asc.setOption(asc.options_t.tokenWords)
>>> asc.setOption(asc.options_t.confidence)
>>> asc.setOption(asc.options_t.interpolate)
>>> 
>>> asc.addAlt("е", "ё")
>>> asc.addAlt("Легкий", "Лёгкий")
>>> 
>>> asc.setAlphabet("абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz")
>>> 
>>> asc.setPilots(["а","у","в","о","с","к","б","и","я","э","a","i","o","e","g"])
>>> asc.setSubstitutes({'p':'р','c':'с','o':'о','t':'т','k':'к','e':'е','a':'а','h':'н','x':'х','b':'в','m':'м'})
>>> 
>>> asc.addAbbr("США")
>>> asc.addAbbr("Сбер")
>>> asc.addGoodword("T-34")
>>> asc.addGoodword("АН-25")
>>> 
>>> asc.addBadword("ийти")
>>> asc.addBadword("циган")
>>> asc.addBadword("апичатка")
>>> 
>>> asc.addUWord("Москва")
>>> asc.addUWord("Санкт-Петербург")
>>> 
>>> def statusArpa(status):
...     print("Read arpa", status)
... 
>>> def statusIndex(status):
...     print("Build index", status)
... 
>>> def statusPrune(status):
...     print("Prune arpa", status)
... 
>>> def status(text, status):
...     print(text, status)
... 
>>> asc.readArpa("./words.arpa", statusArpa)
Read arpa 0
Read arpa 1
Read arpa 2
Read arpa 3
Read arpa 4
Read arpa 5
Read arpa 6
...
>>> asc.setAdCw(38120, 13)
>>> 
>>> asc.addWord("министерство")
>>> asc.addWord("возмездие", 0, 1)
>>> asc.addWord("возражение", asc.idw("возражение"), 2)
...
>>> 
>>> asc.setCode("RU")
>>> asc.setLictype("MIT")
>>> asc.setName("Russian")
>>> asc.setAuthor("You name")
>>> asc.setCopyright("You company LLC")
>>> asc.setLictext("... License text ...")
>>> asc.setContacts("site: https://example.com, e-mail: info@example.com")
>>> 
>>> asc.setSizeEmbedding(32)
>>> asc.generateEmbedding()
>>> 
>>> asc.buildIndex(statusIndex)
Build index 0
Build index 1
Build index 2
Build index 3
Build index 4
Build index 5
Build index 6
...
>>> asc.saveIndex("./3-wittenbell.asc", "password", 128, status)
Dump dictionary 0
Dump dictionary 1
Dump dictionary 2
Dump dictionary 3
Dump dictionary 4
Dump dictionary 5
Dump dictionary 6
...
Dump alternative letters 100
Dump alternative letters 100
Dump alternative words 200
Dump alternative words 100
Dump language model 0
Dump language model 100
Dump substitutes letters 9
Dump substitutes letters 18
Dump substitutes letters 27
Dump substitutes letters 36
Dump substitutes letters 45
Dump substitutes letters 54
Dump substitutes letters 63
Dump substitutes letters 72
Dump substitutes letters 81
Dump substitutes letters 90
Dump substitutes letters 100
Dump substitutes letters 100
>>>
>>> asc.infoIndex("./3-wittenbell.asc")

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

* Code: RU

* Version: 1.0.0

* Dictionary name: Russian

* Build date: 09/14/2020 02:09:38

* Encrypted: YES

* ALM type: ALMv2

* Allow apostrophe: NO

* Count words: 38120
* Count documents: 13

* Only good words: NO
* Mix words in dicts: YES
* Confidence arpa: YES

* Count upper words: 2
* Count pilots words: 15
* Count bad words: 3
* Count good words: 2
* Count substitutes: 11
* Count abbreviations: 2

* Alternatives: е => ё
* Count alternatives words: 1

* Size embedding: 28

* Length n-gram: 3
* Count n-grams: 353

* Author: You name

* Contacts: site: https://example.com, e-mail: info@example.com

* Copyright ©: You company LLC

* License type: MIT
* License text:
... License text ...

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

```

---

### Methods:
- **size** - Method of obtaining the size of the N-gram

### Example:
```python
>>> import asc
>>>
>>> asc.setOption(asc.options_t.confidence)
>>>
>>> asc.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> asc.readArpa('./lm.arpa')
>>>
>>> asc.size()
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
>>> import asc
>>> asc.damerauLevenshtein("привет", "приветик")
2
>>> 
>>> asc.damerauLevenshtein("приевтик", "приветик")
1
>>> 
>>> asc.distanceLevenshtein("приевтик", "приветик")
2
>>> 
>>> asc.tanimoto("привет", "приветик")
0.7142857142857143
>>> 
>>> asc.tanimoto("привеитк", "приветик")
0.4
>>> 
>>> asc.needlemanWunsch("привеитк", "приветик")
4
>>> 
>>> asc.needlemanWunsch("привет", "приветик")
2
>>> 
>>> asc.damerauLevenshtein("acre", "car")
2
>>> asc.distanceLevenshtein("acre", "car")
3
>>> 
>>> asc.damerauLevenshtein("anteater", "theatre")
4
>>> asc.distanceLevenshtein("anteater", "theatre")
5
>>> 
>>> asc.damerauLevenshtein("banana", "nanny")
3
>>> asc.distanceLevenshtein("banana", "nanny")
3
>>> 
>>> asc.damerauLevenshtein("cat", "crate")
2
>>> asc.distanceLevenshtein("cat", "crate")
2
>>>
>>> asc.mulctLevenshtein("привет", "приветик")
4
>>>
>>> asc.mulctLevenshtein("приевтик", "приветик")
1
>>>
>>> asc.mulctLevenshtein("acre", "car")
3
>>>
>>> asc.mulctLevenshtein("anteater", "theatre")
5
>>>
>>> asc.mulctLevenshtein("banana", "nanny")
4
>>>
>>> asc.mulctLevenshtein("cat", "crate")
4
```

---

### Methods:
- **textToJson** - Method to convert text to JSON
- **isAllowApostrophe** - Apostrophe permission check method
- **switchAllowApostrophe** - Method for permitting or denying an apostrophe as part of a word

### Example:
```python
>>> import asc
>>>
>>> def callbackFn(text):
...     print(text)
... 
>>> asc.isAllowApostrophe()
False
>>> asc.switchAllowApostrophe()
>>>
>>> asc.isAllowApostrophe()
True
>>> asc.textToJson("«On nous dit qu'aujourd'hui c'est le cas, encore faudra-t-il l'évaluer» l'astronomie", callbackFn)
[["«","On","nous","dit","qu'aujourd'hui","c'est","le","cas",",","encore","faudra-t-il","l'évaluer","»","l'astronomie"]]
```

---

### Methods:
- **jsonToText** - Method to convert JSON to text

### Example:
```python
>>> import asc
>>>
>>> def callbackFn(text):
...     print(text)
... 
>>> asc.jsonToText('[["«","On","nous","dit","qu\'aujourd\'hui","c\'est","le","cas",",","encore","faudra-t-il","l\'évaluer","»","l\'astronomie"]]', callbackFn)
«On nous dit qu'aujourd'hui c'est le cas, encore faudra-t-il l'évaluer» l'astronomie
```

---

### Methods:
- **restore** - Method for restore text from context

### Example:
```python
>>> import asc
>>>
>>> asc.setOption(asc.options_t.uppers)
>>>
>>> asc.restore(["«","On","nous","dit","qu\'aujourd\'hui","c\'est","le","cas",",","encore","faudra-t-il","l\'évaluer","»","l\'astronomie"])
"«On nous dit qu'aujourd'hui c'est le cas, encore faudra-t-il l'évaluer» l'astronomie"
```

---

### Methods:
- **allowStress** - Method for allow using stress in words
- **disallowStress** - Method for disallow using stress in words

### Example:
```python
>>> import asc
>>>
>>> asc.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> def callbackFn(text):
...     print(text)
... 
>>> asc.textToJson('«Бе́лая стрела́» — согласно распространённой в 1990-е годы в России городской легенде, якобы специально организованная и подготовленная законспирированная правительственная спецслужба, сотрудники которой — бывшие и действовавшие милиционеры и спецназовцы, имеющие право на физическую ликвидацию особо опасных уголовных авторитетов и лидеров орудовавших в России ОПГ, относительно которых не представляется возможным привлечения их к уголовной ответственности законными методами[1][2][3]. Несмотря на отсутствие официальных доказательств существования организации и многочисленные опровержения со стороны силовых структур и служб безопасности[4], в российском обществе легенду считают основанной на подлинных фактах громких убийств криминальных авторитетов, совершённых в 1990-е годы, и не исключают существование реальной спецслужбы[5].', callbackFn)
[["«","Белая","стрела","»","—","согласно","распространённой","в","1990-е","годы","в","России","городской","легенде",",","якобы","специально","организованная","и","подготовленная","законспирированная","правительственная","спецслужба",",","сотрудники","которой","—","бывшие","и","действовавшие","милиционеры","и","спецназовцы",",","имеющие","право","на","физическую","ликвидацию","особо","опасных","уголовных","авторитетов","и","лидеров","орудовавших","в","России","ОПГ",",","относительно","которых","не","представляется","возможным","привлечения","их","к","уголовной","ответственности","законными","методами","[","1","]","[","2","]","[","3","]","."],["Несмотря","на","отсутствие","официальных","доказательств","существования","организации","и","многочисленные","опровержения","со","стороны","силовых","структур","и","служб","безопасности","[","4","]",",","в","российском","обществе","легенду","считают","основанной","на","подлинных","фактах","громких","убийств","криминальных","авторитетов",",","совершённых","в","1990-е","годы",",","и","не","исключают","существование","реальной","спецслужбы","[","5","]","."]]
>>>
>>> asc.jsonToText('[["«","Белая","стрела","»","—","согласно","распространённой","в","1990-е","годы","в","России","городской","легенде",",","якобы","специально","организованная","и","подготовленная","законспирированная","правительственная","спецслужба",",","сотрудники","которой","—","бывшие","и","действовавшие","милиционеры","и","спецназовцы",",","имеющие","право","на","физическую","ликвидацию","особо","опасных","уголовных","авторитетов","и","лидеров","орудовавших","в","России","ОПГ",",","относительно","которых","не","представляется","возможным","привлечения","их","к","уголовной","ответственности","законными","методами","[","1","]","[","2","]","[","3","]","."],["Несмотря","на","отсутствие","официальных","доказательств","существования","организации","и","многочисленные","опровержения","со","стороны","силовых","структур","и","служб","безопасности","[","4","]",",","в","российском","обществе","легенду","считают","основанной","на","подлинных","фактах","громких","убийств","криминальных","авторитетов",",","совершённых","в","1990-е","годы",",","и","не","исключают","существование","реальной","спецслужбы","[","5","]","."]]', callbackFn)
«Белая стрела» — согласно распространённой в 1990-е годы в России городской легенде, якобы специально организованная и подготовленная законспирированная правительственная спецслужба, сотрудники которой — бывшие и действовавшие милиционеры и спецназовцы, имеющие право на физическую ликвидацию особо опасных уголовных авторитетов и лидеров орудовавших в России ОПГ, относительно которых не представляется возможным привлечения их к уголовной ответственности законными методами [1] [2] [3].
Несмотря на отсутствие официальных доказательств существования организации и многочисленные опровержения со стороны силовых структур и служб безопасности [4], в российском обществе легенду считают основанной на подлинных фактах громких убийств криминальных авторитетов, совершённых в 1990-е годы, и не исключают существование реальной спецслужбы [5].
>>>
>>> asc.allowStress()
>>> asc.textToJson('«Бе́лая стрела́» — согласно распространённой в 1990-е годы в России городской легенде, якобы специально организованная и подготовленная законспирированная правительственная спецслужба, сотрудники которой — бывшие и действовавшие милиционеры и спецназовцы, имеющие право на физическую ликвидацию особо опасных уголовных авторитетов и лидеров орудовавших в России ОПГ, относительно которых не представляется возможным привлечения их к уголовной ответственности законными методами[1][2][3]. Несмотря на отсутствие официальных доказательств существования организации и многочисленные опровержения со стороны силовых структур и служб безопасности[4], в российском обществе легенду считают основанной на подлинных фактах громких убийств криминальных авторитетов, совершённых в 1990-е годы, и не исключают существование реальной спецслужбы[5].', callbackFn)
[["«","Бе́лая","стрела́","»","—","согласно","распространённой","в","1990-е","годы","в","России","городской","легенде",",","якобы","специально","организованная","и","подготовленная","законспирированная","правительственная","спецслужба",",","сотрудники","которой","—","бывшие","и","действовавшие","милиционеры","и","спецназовцы",",","имеющие","право","на","физическую","ликвидацию","особо","опасных","уголовных","авторитетов","и","лидеров","орудовавших","в","России","ОПГ",",","относительно","которых","не","представляется","возможным","привлечения","их","к","уголовной","ответственности","законными","методами","[","1","]","[","2","]","[","3","]","."],["Несмотря","на","отсутствие","официальных","доказательств","существования","организации","и","многочисленные","опровержения","со","стороны","силовых","структур","и","служб","безопасности","[","4","]",",","в","российском","обществе","легенду","считают","основанной","на","подлинных","фактах","громких","убийств","криминальных","авторитетов",",","совершённых","в","1990-е","годы",",","и","не","исключают","существование","реальной","спецслужбы","[","5","]","."]]
>>>
>>> asc.jsonToText('[["«","Бе́лая","стрела́","»","—","согласно","распространённой","в","1990-е","годы","в","России","городской","легенде",",","якобы","специально","организованная","и","подготовленная","законспирированная","правительственная","спецслужба",",","сотрудники","которой","—","бывшие","и","действовавшие","милиционеры","и","спецназовцы",",","имеющие","право","на","физическую","ликвидацию","особо","опасных","уголовных","авторитетов","и","лидеров","орудовавших","в","России","ОПГ",",","относительно","которых","не","представляется","возможным","привлечения","их","к","уголовной","ответственности","законными","методами","[","1","]","[","2","]","[","3","]","."],["Несмотря","на","отсутствие","официальных","доказательств","существования","организации","и","многочисленные","опровержения","со","стороны","силовых","структур","и","служб","безопасности","[","4","]",",","в","российском","обществе","легенду","считают","основанной","на","подлинных","фактах","громких","убийств","криминальных","авторитетов",",","совершённых","в","1990-е","годы",",","и","не","исключают","существование","реальной","спецслужбы","[","5","]","."]]', callbackFn)
«Бе́лая стрела́» — согласно распространённой в 1990-е годы в России городской легенде, якобы специально организованная и подготовленная законспирированная правительственная спецслужба, сотрудники которой — бывшие и действовавшие милиционеры и спецназовцы, имеющие право на физическую ликвидацию особо опасных уголовных авторитетов и лидеров орудовавших в России ОПГ, относительно которых не представляется возможным привлечения их к уголовной ответственности законными методами [1] [2] [3].
Несмотря на отсутствие официальных доказательств существования организации и многочисленные опровержения со стороны силовых структур и служб безопасности [4], в российском обществе легенду считают основанной на подлинных фактах громких убийств криминальных авторитетов, совершённых в 1990-е годы, и не исключают существование реальной спецслужбы [5].
>>>
>>> asc.disallowStress()
>>> asc.textToJson('«Бе́лая стрела́» — согласно распространённой в 1990-е годы в России городской легенде, якобы специально организованная и подготовленная законспирированная правительственная спецслужба, сотрудники которой — бывшие и действовавшие милиционеры и спецназовцы, имеющие право на физическую ликвидацию особо опасных уголовных авторитетов и лидеров орудовавших в России ОПГ, относительно которых не представляется возможным привлечения их к уголовной ответственности законными методами[1][2][3]. Несмотря на отсутствие официальных доказательств существования организации и многочисленные опровержения со стороны силовых структур и служб безопасности[4], в российском обществе легенду считают основанной на подлинных фактах громких убийств криминальных авторитетов, совершённых в 1990-е годы, и не исключают существование реальной спецслужбы[5].', callbackFn)
[["«","Белая","стрела","»","—","согласно","распространённой","в","1990-е","годы","в","России","городской","легенде",",","якобы","специально","организованная","и","подготовленная","законспирированная","правительственная","спецслужба",",","сотрудники","которой","—","бывшие","и","действовавшие","милиционеры","и","спецназовцы",",","имеющие","право","на","физическую","ликвидацию","особо","опасных","уголовных","авторитетов","и","лидеров","орудовавших","в","России","ОПГ",",","относительно","которых","не","представляется","возможным","привлечения","их","к","уголовной","ответственности","законными","методами","[","1","]","[","2","]","[","3","]","."],["Несмотря","на","отсутствие","официальных","доказательств","существования","организации","и","многочисленные","опровержения","со","стороны","силовых","структур","и","служб","безопасности","[","4","]",",","в","российском","обществе","легенду","считают","основанной","на","подлинных","фактах","громких","убийств","криминальных","авторитетов",",","совершённых","в","1990-е","годы",",","и","не","исключают","существование","реальной","спецслужбы","[","5","]","."]]
>>>
>>> asc.jsonToText('[["«","Белая","стрела","»","—","согласно","распространённой","в","1990-е","годы","в","России","городской","легенде",",","якобы","специально","организованная","и","подготовленная","законспирированная","правительственная","спецслужба",",","сотрудники","которой","—","бывшие","и","действовавшие","милиционеры","и","спецназовцы",",","имеющие","право","на","физическую","ликвидацию","особо","опасных","уголовных","авторитетов","и","лидеров","орудовавших","в","России","ОПГ",",","относительно","которых","не","представляется","возможным","привлечения","их","к","уголовной","ответственности","законными","методами","[","1","]","[","2","]","[","3","]","."],["Несмотря","на","отсутствие","официальных","доказательств","существования","организации","и","многочисленные","опровержения","со","стороны","силовых","структур","и","служб","безопасности","[","4","]",",","в","российском","обществе","легенду","считают","основанной","на","подлинных","фактах","громких","убийств","криминальных","авторитетов",",","совершённых","в","1990-е","годы",",","и","не","исключают","существование","реальной","спецслужбы","[","5","]","."]]', callbackFn)
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
>>> import asc
>>>
>>> asc.setBadwords(["hello", "world", "test"])
>>>
>>> asc.getBadwords()
{1554834897, 2156498622, 28307030}
>>>
>>> asc.addBadword("test2")
>>>
>>> asc.getBadwords()
{5170183734, 1554834897, 2156498622, 28307030}
```

### Example:
```python
>>> import asc
>>>
>>> asc.setBadwords({24227504, 1219922507, 1794085167})
>>>
>>> asc.getBadwords()
{24227504, 1219922507, 1794085167}
>>>
>>> asc.clear(asc.clear_t.badwords)
>>>
>>> asc.getBadwords()
{}
```

---

### Methods:
- **addGoodword** - Method add good word
- **setGoodwords** - Method set words to whitelist
- **getGoodwords** - Method get words in whitelist

### Example:
```python
>>> import asc
>>>
>>> asc.setGoodwords(["hello", "world", "test"])
>>>
>>> asc.getGoodwords()
{1554834897, 2156498622, 28307030}
>>>
>>> asc.addGoodword("test2")
>>>
>>> asc.getGoodwords()
{5170183734, 1554834897, 2156498622, 28307030}
>>>
>>> asc.clear(asc.clear_t.goodwords)
>>>
>>  asc.getGoodwords()
{}
```

### Example:
```python
>>> import asc
>>>
>>> asc.setGoodwords({24227504, 1219922507, 1794085167})
>>>
>>> asc.getGoodwords()
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
>>> import asc
>>>
>>> asc.setUserToken("usa")
>>>
>>> asc.setUserToken("russia")
>>>
>>> asc.getUserTokenId("usa")
5759809081
>>>
>>> asc.getUserTokenId("russia")
9910674734
>>>
>>> asc.getUserTokens()
['usa', 'russia']
>>>
>>> asc.getUserTokenWord(5759809081)
'usa'
>>>
>>> asc.getUserTokenWord(9910674734)
'russia'
>>>
>> asc.clear(asc.clear_t.utokens)
>>>
>>> asc.getUserTokens()
[]
```

---

### Methods:
- **findNgram** - N-gram search method in text
- **word** - "Method to extract a word by its identifier"

### Example:
```python
>>> import asc
>>> 
>>> def callbackFn(text):
...     print(text)
... 
>>> asc.setOption(asc.options_t.confidence)
>>> asc.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>> asc.readArpa('./lm.arpa')
>>> 
>>> asc.idw("привет")
2487910648
>>> asc.word(2487910648)
'привет'
>>> 
>>> asc.findNgram("Особое место занимает чудотворная икона Лобзание Христа Иудою", callbackFn)
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
>>> import asc
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
>>> asc.setUserToken("usa")
>>>
>>> asc.setUserToken("russia")
>>>
>>> asc.setUserTokenMethod("usa", fn)
>>>
>>> asc.setUserTokenMethod("russia", fn)
>>>
>>> asc.idw("usa")
5759809081
>>>
>>> asc.idw("russia")
9910674734
>>>
>>> asc.getUserTokenWord(5759809081)
'usa'
>>>
>>> asc.getUserTokenWord(9910674734)
'russia'
```

---

### Methods:
- **setWordPreprocessingMethod** - Method for set the word preprocessing function

### Example:
```python
>>> import asc
>>>
>>> def run(word, context):
...     if word == "возле": word = "около"
...     return word
... 
>>> asc.setOption(asc.options_t.debug)
>>>
>>> asc.setOption(asc.options_t.confidence)
>>>
>>> asc.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> asc.readArpa('./lm.arpa')
>>>
>>> asc.setWordPreprocessingMethod(run)
>>>
>>> a = asc.perplexity("неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор???с лязгом выкатился и остановился возле мальчика....")
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
>>> import asc
>>>
>>> asc.setLogfile("./log.txt")
>>>
>>> asc.setOOvFile("./oov.txt")
```

---

### Methods:
- **perplexity** - Perplexity calculation
- **pplConcatenate** - Method of combining perplexia
- **pplByFiles** - Method for reading perplexity calculation by file or group of files

### Example:
```python
>>> import asc
>>>
>>> asc.setOption(asc.options_t.confidence)
>>>
>>> asc.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> asc.readArpa('./lm.arpa')
>>>
>>> a = asc.perplexity("неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор???с лязгом выкатился и остановился возле мальчика....")
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
>>> b = asc.pplByFiles("./text.txt")
>>>
>>> c = asc.pplConcatenate(a, b)
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
>>> import asc
>>>
>>> def tokensFn(word, context, reset, stop):
...     print(word, " => ", context)
...     return True
...
>>> asc.switchAllowApostrophe()
>>>
>>> asc.tokenization("«On nous dit qu'aujourd'hui c'est le cas, encore faudra-t-il l'évaluer» l'astronomie", tokensFn)
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
>>> import asc
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
>>> asc.setTokenizerFn(tokenizerFn)
>>>
>>> asc.tokenization("Hello World today!", tokensFn)
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
>>> import asc
>>>
>>> def sentencesFn(text):
...     print("Sentences:", text)
...     return True
...
>>> asc.setOption(asc.options_t.confidence)
>>>
>>> asc.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> asc.readArpa('./lm.arpa')
>>>
>>> asc.sentences(sentencesFn)
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
>>> asc.sentencesToFile(5, "./result.txt")
```

---

### Methods:
- **fixUppers** - Method for correcting registers in the text
- **fixUppersByFiles** - Method for correcting text registers in a text file

### Example:
```python
>>> import asc
>>>
>>> asc.setOption(asc.options_t.confidence)
>>>
>>> asc.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> asc.readArpa('./lm.arpa')
>>>
>>> asc.fixUppers("неожиданно из подворотни в олега ударил яркий прожектор патрульный трактор???с лязгом выкатился и остановился возле мальчика....")
'Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор??? С лязгом выкатился и остановился возле мальчика....'
>>>
>>> asc.fixUppersByFiles("./corpus", "./result.txt", "txt")
```

---

### Methods:
- **checkHypLat** - Hyphen and latin character search method

### Example:
```python
>>> import asc
>>>
>>> asc.checkHypLat("Hello-World")
(True, True)
>>>
>>> asc.checkHypLat("Hello")
(False, True)
>>>
>>> asc.checkHypLat("Привет")
(False, False)
>>>
>>> asc.checkHypLat("так-как")
(True, False)
```

---

### Methods:
- **getUppers** - Method for extracting registers for each word
- **countLetter** - Method for counting the amount of a specific letter in a word

### Example:
```python
>>> import asc
>>>
>>> asc.setOption(asc.options_t.confidence)
>>>
>>> asc.readArpa('./lm.arpa')
>>>
>>> asc.idw("Living")
10493385932
>>>
>>> asc.idw("in")
3301
>>>
>>> asc.idw("the")
217280
>>>
>>> asc.idw("USA")
188643
>>>
>>> asc.getUppers([10493385932, 3301, 217280, 188643])
[1, 0, 0, 7]
>>> 
>>> asc.countLetter("hello-world", "-")
1
>>>
>>> asc.countLetter("hello-world", "l")
3
```

---

### Methods:
- **urls** - Method for extracting URL address coordinates in a string

### Example:
```python
>>> import asc
>>>
>>> asc.urls("This website: example.com was designed with ...")
{14: 25}
>>>
>>> asc.urls("This website: https://a.b.c.example.net?id=52#test-1 was designed with ...")
{14: 52}
>>>
>>> asc.urls("This website: https://a.b.c.example.net?id=52#test-1 and 127.0.0.1 was designed with ...")
{14: 52, 57: 66}
```

---

### Methods:
- **roman2Arabic** - Method for translating Roman numerals to Arabic

### Example:
```python
>>> import asc
>>>
>>> asc.roman2Arabic("XVI")
16
```

---

### Methods:
- **rest** - Method for correction and detection of words with mixed alphabets
- **setSubstitutes** - Method for set letters to correct words from mixed alphabets
- **getSubstitutes** - Method of extracting letters to correct words from mixed alphabets

### Example:
```python
>>> import asc
>>>
>>> asc.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> asc.setSubstitutes({'p':'р','c':'с','o':'о','t':'т','k':'к','e':'е','a':'а','h':'н','x':'х','b':'в','m':'м'})
>>>
>>> asc.getSubstitutes()
{'a': 'а', 'b': 'в', 'c': 'с', 'e': 'е', 'h': 'н', 'k': 'к', 'm': 'м', 'o': 'о', 'p': 'р', 't': 'т', 'x': 'х'}
>>>
>>> str = "ПPИBETИК"
>>>
>>> str.lower()
'пpиbetик'
>>>
>>> asc.rest(str)
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
>>> import asc
>>>
>>> asc.idw("<date>")
6
>>>
>>> asc.idw("<time>")
7
>>>
>>> asc.idw("<abbr>")
5
>>>
>>> asc.idw("<math>")
9
>>>
>>> asc.setTokenDisable("date|time|abbr|math")
>>>
>>> asc.getTokensDisable()
{9, 5, 6, 7}
>>>
>>> asc.setTokensDisable({6, 7, 5, 9})
>>>
>>> asc.setTokenUnknown("date|time|abbr|math")
>>>
>>> asc.getTokensUnknown()
{9, 5, 6, 7}
>>>
>>> asc.setTokensUnknown({6, 7, 5, 9})
>>>
>>> asc.setAllTokenDisable()
>>>
>>> asc.getTokensDisable()
{2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23}
>>>
>>> asc.setAllTokenUnknown()
>>>
>>> asc.getTokensUnknown()
{2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23}
```

---

### Methods:
- **countAlphabet** - Method of obtaining the number of letters in the dictionary

### Example:
```python
>>> import asc
>>>
>>> asc.getAlphabet()
'abcdefghijklmnopqrstuvwxyz'
>>>
>>> asc.countAlphabet()
26
>>>
>>> asc.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> asc.countAlphabet()
59
```

---

### Methods:
- **countBigrams** - Method get count bigrams
- **countTrigrams** - Method get count trigrams
- **countGrams** - Method get count N-gram by lm size

### Example:
```python
>>> import asc
>>>
>>> asc.setOption(asc.options_t.confidence)
>>>
>>> asc.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> asc.readArpa('./lm.arpa')
>>>
>>> asc.countBigrams("неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор???с лязгом выкатился и остановился возле мальчика....")
12
>>>
>>> asc.countTrigrams("неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор???с лязгом выкатился и остановился возле мальчика....")
10
>>>
>>> asc.size()
3
>>>
>>> asc.countGrams("неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор???с лязгом выкатился и остановился возле мальчика....")
10
>>>
>>> asc.idw("неожиданно")
3263936167
>>>
>>> asc.idw("из")
5134
>>>
>>> asc.idw("подворотни")
12535356101
>>>
>>> asc.idw("в")
53
>>>
>>> asc.idw("Олега")
2824508300
>>>
>>> asc.idw("ударил")
24816796913
>>>
>>> asc.countBigrams([3263936167, 5134, 12535356101, 53, 2824508300, 24816796913])
5
>>>
>>> asc.countTrigrams([3263936167, 5134, 12535356101, 53, 2824508300, 24816796913])
4
>>>
>>> asc.countGrams([3263936167, 5134, 12535356101, 53, 2824508300, 24816796913])
4
```

---

### Methods:
- **arabic2Roman** - Convert arabic number to roman number

### Example:
```python
>>> import asc
>>>
>>> asc.arabic2Roman(23)
'XXIII'
>>>
>>> asc.arabic2Roman("33")
'XXXIII'
```

---

### Methods:
- **setThreads** - Method for set the number of threads (0 - all threads)

### Example:
```python
>>> import asc
>>>
>>> asc.setOption(asc.options_t.confidence)
>>>
>>> asc.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> asc.readArpa('./lm.arpa')
>>>
>>> asc.setThreads(3)
>>>
>>> a = asc.pplByFiles("./text.txt")
>>>
>>> print(a.logprob)
-48201.29481399994
```

---

### Methods:
- **fti** - Method for removing the fractional part of a number

### Example:
```python
>>> import asc
>>>
>>> asc.fti(5892.4892)
5892489200000
>>>
>>> asc.fti(5892.4892, 4)
58924892
```

---

### Methods:
- **context** - Method for assembling text context from a sequence

### Example:
```python
>>> import asc
>>>
>>> asc.setOption(asc.options_t.confidence)
>>>
>>> asc.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> asc.readArpa('./lm.arpa')
>>>
>>> asc.idw("неожиданно")
3263936167
>>>
>>> asc.idw("из")
5134
>>>
>>> asc.idw("подворотни")
12535356101
>>>
>>> asc.idw("в")
53
>>>
>>> asc.idw("Олега")
2824508300
>>>
>>> asc.idw("ударил")
24816796913
>>>
>>> asc.context([3263936167, 5134, 12535356101, 53, 2824508300, 24816796913])
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
>>> import asc
>>>
>>> asc.setOption(asc.options_t.confidence)
>>>
>>> asc.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> asc.readArpa('./lm.arpa')
>>>
>>> asc.addAbbr("США")
>>>
>>> asc.isAbbr("сша")
True
>>>
>>> asc.addSuffix("1-я")
>>>
>>> asc.isSuffix("1-я")
True
>>>
>>> asc.isToken(asc.idw("США"))
True
>>>
>>> asc.isToken(asc.idw("1-я"))
True
>>>
>>> asc.isToken(asc.idw("125"))
True
>>>
>>> asc.isToken(asc.idw("<s>"))
True
>>>
>>> asc.isToken(asc.idw("Hello"))
False
>>>
>>> asc.isIdWord(asc.idw("https://anyks.com"))
True
>>>
>>> asc.isIdWord(asc.idw("Hello"))
True
>>>
>>> asc.isIdWord(asc.idw("-"))
False
```

---

### Methods:
- **findByFiles** - Method search N-grams in a text file

### Example:
```python
>>> import asc
>>>
>>> asc.setOption(asc.options_t.debug)
>>>
>>> asc.setOption(asc.options_t.confidence)
>>>
>>> asc.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> asc.readArpa('./lm.arpa')
>>>
>>> asc.findByFiles("./text.txt", "./result.txt")
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
>>> import asc
>>>
>>> asc.setOption(asc.options_t.debug)
>>>
>>> asc.setOption(asc.options_t.confidence)
>>>
>>> asc.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> asc.readArpa('./lm.arpa')
>>>
>>> asc.addAbbr("США")
>>>
>>> asc.isAbbr("сша")
>>>
>>> asc.checkSequence("Неожиданно из подворотни в олега ударил")
True
>>>
>>> asc.checkSequence("Сегодня сыграл и в Олега ударил яркий прожектор патрульный трактор с корпоративным сектором")
True
>>>
>>> asc.checkSequence("Сегодня сыграл и в Олега ударил яркий прожектор патрульный трактор с корпоративным сектором", True)
True
>>>
>>> asc.checkSequence("в Олега ударил яркий")
True
>>>
>>> asc.checkSequence("в Олега ударил яркий", True)
True
>>>
>>> asc.checkSequence("от госсекретаря США")
True
>>>
>>> asc.checkSequence("от госсекретаря США", True)
True
>>>
>>> asc.checkSequence("Неожиданно из подворотни в олега ударил", 2)
True
>>>
>>> asc.checkSequence(["Неожиданно","из","подворотни","в","олега","ударил"], 2)
True
>>>
>>> asc.existSequence("<s> Сегодня сыграл и в, Олега ударил яркий прожектор, патрульный трактор - с корпоративным сектором </s>", 2)
(True, 0)
>>>
>>> asc.existSequence(["<s>","Сегодня","сыграл","и","в",",","Олега","ударил","яркий","прожектор",",","патрульный","трактор","-","с","корпоративным","сектором","</s>"], 2)
(True, 2)
>>>
>>> asc.idw("от")
6086
>>>
>>> asc.idw("госсекретаря")
51273912082
>>>
>>> asc.idw("США")
5
>>>
>>> asc.checkSequence([6086, 51273912082, 5])
True
>>>
>>> asc.checkSequence([6086, 51273912082, 5], True)
True
>>>
>>> asc.checkSequence(["от", "госсекретаря", "США"])
True
>>>
>>> asc.checkSequence(["от", "госсекретаря", "США"], True)
True
>>>
>>> asc.checkByFiles("./text.txt", "./result.txt")
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
>>> asc.checkByFiles("./corpus", "./result.txt", False, "txt")
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
>>> asc.checkByFiles("./corpus", "./result.txt", True, "txt")
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
>>> import asc
>>> 
>>> asc.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>> asc.setSubstitutes({'p':'р','c':'с','o':'о','t':'т','k':'к','e':'е','a':'а','h':'н','x':'х','b':'в','m':'м'})
>>> 
>>> asc.check("Дом-2", asc.check_t.home2)
True
>>> 
>>> asc.check("Дом2", asc.check_t.home2)
False
>>> 
>>> asc.check("Дом-2", asc.check_t.latian)
False
>>> 
>>> asc.check("Hello", asc.check_t.latian)
True
>>> 
>>> asc.check("прiвет", asc.check_t.latian)
True
>>> 
>>> asc.check("Дом-2", asc.check_t.hyphen)
True
>>> 
>>> asc.check("Дом2", asc.check_t.hyphen)
False
>>> 
>>> asc.check("Д", asc.check_t.letter)
True
>>> 
>>> asc.check("$", asc.check_t.letter)
False
>>> 
>>> asc.check("-", asc.check_t.letter)
False
>>> 
>>> asc.check("просtоквaшино", asc.check_t.similars)
True
>>> 
>>> asc.match("my site http://example.ru, it's true", asc.match_t.url)
True
>>> 
>>> asc.match("по вашему ip адресу 46.40.123.12 проводится проверка", asc.match_t.url)
True
>>> 
>>> asc.match("мой адрес в формате IPv6: http://[2001:0db8:11a3:09d7:1f34:8a2e:07a0:765d]/", asc.match_t.url)
True
>>> 
>>> asc.match("13-я", asc.match_t.abbr)
True
>>> 
asc.match("13-я-й", asc.match_t.abbr)
False
>>> 
asc.match("т.д", asc.match_t.abbr)
True
>>> 
asc.match("т.п.", asc.match_t.abbr)
True
>>> 
>>> asc.match("С.Ш.А.", asc.match_t.abbr)
True
>>> 
>>> asc.addAbbr("сша")
>>> asc.match("США", asc.match_t.abbr)
True
>>> 
>>> asc.addSuffix("15-летия")
>>> asc.match("15-летия", asc.match_t.abbr)
True
>>> 
>>> asc.getSuffixes()
{3139900457}
>>> 
>>> asc.idw("лет")
328041
>>> 
>>> asc.idw("тых")
352214
>>> 
>>> asc.setSuffixes({328041, 352214})
>>> 
>>> asc.getSuffixes()
{328041, 352214}
>>> 
>>> def status(status):
...     print(status)
... 
>>> asc.readSuffix("./suffix.abbr", status)
>>> 
>>> asc.match("15-лет", asc.match_t.abbr)
True
>>> 
>>> asc.match("20-тых", asc.match_t.abbr)
True
>>> 
>>> asc.match("15-летия", asc.match_t.abbr)
False
>>> 
>>> asc.match("Hello", asc.match_t.latian)
True
>>> 
>>> asc.match("прiвет", asc.match_t.latian)
False
>>> 
>>> asc.match("23424", asc.match_t.number)
True
>>> 
>>> asc.match("hello", asc.match_t.number)
False
>>> 
>>> asc.match("23424.55", asc.match_t.number)
False
>>> 
>>> asc.match("23424", asc.match_t.decimal)
False
>>> 
>>> asc.match("23424.55", asc.match_t.decimal)
True
>>> 
>>> asc.match("23424,55", asc.match_t.decimal)
True
>>> 
>>> asc.match("-23424.55", asc.match_t.decimal)
True
>>> 
>>> asc.match("+23424.55", asc.match_t.decimal)
True
>>> 
>>> asc.match("+23424.55", asc.match_t.anumber)
True
>>> 
>>> asc.match("15T-34", asc.match_t.anumber)
True
>>> 
>>> asc.match("hello", asc.match_t.anumber)
False
>>> 
>>> asc.match("hello", asc.match_t.allowed)
True
>>> 
>>> asc.match("évaluer", asc.match_t.allowed)
False
>>> 
>>> asc.match("13", asc.match_t.allowed)
True
>>> 
>>> asc.match("Hello-World", asc.match_t.allowed)
True
>>> 
>>> asc.match("Hello", asc.match_t.math)
False
>>> 
>>> asc.match("+", asc.match_t.math)
True
>>> 
>>> asc.match("=", asc.match_t.math)
True
>>> 
>>> asc.match("Hello", asc.match_t.upper)
True
>>> 
>>> asc.match("hello", asc.match_t.upper)
False
>>> 
>>> asc.match("hellO", asc.match_t.upper)
False
>>> 
>>> asc.match("a", asc.match_t.punct)
False
>>> 
>>> asc.match(",", asc.match_t.punct)
True
>>> 
>>> asc.match(" ", asc.match_t.space)
True
>>> 
>>> asc.match("a", asc.match_t.space)
False
>>> 
>>> asc.match("a", asc.match_t.special)
False
>>> 
>>> asc.match("±", asc.match_t.special)
False
>>> 
>>> asc.match("[", asc.match_t.isolation)
True
>>> 
>>> asc.match("a", asc.match_t.isolation)
False
>>> 
>>> asc.match("a", asc.match_t.greek)
False
>>> 
>>> asc.match("Ψ", asc.match_t.greek)
True
>>> 
>>> asc.match("->", asc.match_t.route)
False
>>> 
>>> asc.match("⇔", asc.match_t.route)
True
>>> 
>>> asc.match("a", asc.match_t.letter)
True
>>> 
>>> asc.match("!", asc.match_t.letter)
False
>>> 
>>> asc.match("!", asc.match_t.pcards)
False
>>> 
>>> asc.match("♣", asc.match_t.pcards)
True
>>> 
>>> asc.match("p", asc.match_t.currency)
False
>>> 
>>> asc.match("$", asc.match_t.currency)
True
>>> 
>>> asc.match("€", asc.match_t.currency)
True
>>> 
>>> asc.match("₽", asc.match_t.currency)
True
>>> 
>>> asc.match("₿", asc.match_t.currency)
True
```

---

### Methods:
- **delInText** - Method for delete letter in text

### Example:
```python
>>> import asc
>>>
>>> asc.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> asc.delInText("неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор??? с лязгом выкатился и остановился возле мальчика....", asc.wdel_t.punct)
'неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор с лязгом выкатился и остановился возле мальчика'
>>>
>>> asc.delInText("hello-world-hello-world", asc.wdel_t.hyphen)
'helloworldhelloworld'
>>>
>>> asc.delInText("неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор??? с лязгом выкатился и остановился возле мальчика....", asc.wdel_t.broken)
'неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор с лязгом выкатился и остановился возле мальчика'
>>>
>>> asc.delInText("«On nous dit qu'aujourd'hui c'est le cas, encore faudra-t-il l'évaluer» l'astronomie", asc.wdel_t.broken)
"On nous dit qu'aujourd'hui c'est le cas encore faudra-t-il l'valuer l'astronomie"
```

---

### Methods:
- **countsByFiles** - Method for counting the number of n-grams in a text file

### Example:
```python
>>> import asc
>>>
>>> asc.setOption(asc.options_t.debug)
>>>
>>> asc.setOption(asc.options_t.confidence)
>>>
>>> asc.setAlphabet("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
>>>
>>> asc.readArpa('./lm.arpa')
>>>
>>> asc.countsByFiles("./text.txt", "./result.txt", 3)
info: 0 | Сегодня яичницей никто не завтракал как впрочем и вчера на ближайшем к нам рынке мы ели фруктовый салат со свежевыжатым соком как в старые добрые времена в Бразилии

info: 10 | Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор?С лязгом выкатился и остановился возле мальчика.

info: 10 | Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор!С лязгом выкатился и остановился возле мальчика.

info: 0 | Так как эти яйца жалко есть а хочется все больше любоваться их можно покрыть лаком даже прозрачным лаком для ногтей

info: 10 | Неожиданно из подворотни в Олега ударил яркий прожектор патрульный трактор???С лязгом выкатился и остановился возле мальчика....

Counts 3grams: 471
>>>
>>> asc.countsByFiles("./corpus", "./result.txt", 2, "txt")
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
