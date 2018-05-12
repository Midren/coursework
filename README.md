# E-book reader

## Description
This project allows you to read books in English without looking at vocabulary constantly. You can get a definition of word for this sentence, considering context. It also says you if it is part of idiom and give definition of this idiom. There is example of using after every definition, so you can easily use it in future.
## Installation
```bash
$ git clone https://github.com/Momka45/coursework
$ cd coursework/stage_4/ebook_server
$ virutalenv -p python3 venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```
## Usage
This will server on your local machine
```bash
$ cd .../ebook_server
$ source venv/bin/activate
$ python3 run.py
```
Next you need to sent data to server using POST request 
### Input data
**word** - word that you want get definition  
**sentence** - sentence which word is part of  
**word_order** - order of this word in this sentence  
**Example:**  
In this town and in _this_ region we are happy.  
"word" : "this", "sentence" : "In this town and in this region we are happy.", "word_order" : "2"  
### Output data
Json file with such structure:
```html
{  
  "senses": {  
    "idiom_sense": {  
      "category": "",   
      "definitions":  
        {  
          "definition": "",   
          "example": ""  
        },  
        {  
          "definition": "",   
          "example": ""  
        },  
        {  
          "definition": "",   
          "example": ""  
        }  
      ],   
      "idiom_name": ""  
    },   
    "word_sense": {  
      "category": "",   
      "definitions": [  
        {  
          "definition": ""  
        },   
        {  
          "definition": ""  
        },   
        {  
          "definition": ""  
        }  
      ]  
    }  
  },   
  "word": ""  
}  
```
## Structure of project
```
├── app
│   ├── __init__.py
│   └── routes.py (Routes of server)
├── config.py (Config server)
├── expressions.json (File with all idioms)
├── requirements.txt (Libraries that you need to installl)
├── run.py (Module that start server)
└── sentence_processing (Packet with modules that find senses)
    ├── auxiliar_functions.py (Auxiliar functuatians that are used to make essential NLP algorithms)
    ├── definitions.py (Find definitions of word)
    ├── graph_word_wsd.py (Builds graph of words(idioms) and find pagerank)
    ├── idiom_processing.py (Find idiom in sentences)
    ├── idiom_senses.py (Find best sense for idiom)
    └── __init__.py
```
## Contributing
- Fork it (https://github.com/Momka45/coursework/fork)
- Create your feature branch (git checkout -b feature/fooBar)
- Commit your changes (git commit -am 'Add some fooBar')
- Push to the branch (git push origin feature/fooBar)
- Create a new Pull Request

## Credits
This project is contributed by Roman Milishchuk(@Momka45)
