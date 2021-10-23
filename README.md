<p align="center">
  <img src="https://raw.githubusercontent.com/samreachyan /TeleGram/master/.image/20191203_205322.jpg" width="470" height="150">
</p>

<p align="center"><img src="https://img.shields.io/badge/Version-3.1-brightgreen"></p>
<p align="center">
  <a href="https://github.com/th3unkn0n">
    <img src="https://img.shields.io/github/followers/th3unkn0n?label=Follow&style=social">
  </a>
  <a href="https://github.com/th3unkn0n/TeleGram-Group-Scraper">
    <img src="https://img.shields.io/github/stars/th3unkn0n/TeleGram-Group-Scraper?style=social">
  </a>
</p>
<p align="center">
  ការប្រើប្រាស់ API តេលេក្រាមដើម្បីយកទិន្នន័យធ្វើការងារ
</p>
<p align="center">
</p>

---

## API Setup

- ចុចចូលវេបសាយនេះ [http://my.telegram.org](http://my.telegram.org) និង log in ជាមួយលេខទូរសព្ទរបស់លោកអ្នក ។
- បំពេញពត៌មានចាំបាច់សម្រាប់តេលេក្រាម និង ជ្រើសយកតាម website ដែលបានកំណត់ ។
- លោកអ្នកនឹងទទួលឃើញ `api_id`, `api_hash` ។​ ចូលចម្លងវាដើម្បីយកមកប្រើប្រាស់ក្នុងការប្រើប្រាស់ក្នុង កូដរបស់យើង `setup.py` ។​

## How To Install and Use

```py
git clone https://github.com/samreachyan/teleGram.git
```

អ្នកត្រូវទាញយក [Python](https://www.python.org/downloads/) តាមតំណភ្ជាប់នេះ រួចដំឡើងវាតាមដំណាក់កាល។

- លោកអ្នកត្រូវដំឡើង Library មួយចំនួនដែលពាក់ព័ន្ធ

```py
cd TeleGram
python3 setup.py -i
```

- ធ្វើបច្ចុប្បន្នភាពកម្មវិធី

```py
python3 setup.py -u
```

- លោកអ្នកត្រូវបញ្ចូល `api_id`,​ `api_hash` និង លេខទូរសព្ទរបស់លោកអ្នកដើម្បីចាប់ផ្តើមវា ។

```py
python3 setup.py -c
```

- ក្រោយពេលលោកអ្នកបានដំឡើងចប់អស់ហើយ លោកអ្នកអាចទាញយកទិន្នន័យអ្នកប្រើប្រាស់ ក្នុង Group ឬ ​Channel បាន។
  **_ត្រូវចំណាំ៖ សម្រាប់ Group ជាក្រុមណាដែលសមាជិកអាច Chat បានដោយសេរីឬក្រុមណាដែលអ្នកជា admin។ សម្រាប់ Channel អ្នកត្រូវតែជា admin ទើបអាចទាញយកទិន្នន័យអ្នកប្រើប្រាស់បាន។_**

```
python3 scraper.py
```

- ពេលទាញយកទិន្នន័យអ្នកប្រើប្រាស់អ្នកអាច រក្សាទុកក្នុង members.csv (ក្រោយពេលអ្នកទាញយកឈ្មោះហើយ អាចប្តូរឈ្មោះ file បាន)

- ដើម្បីអ្នកអាចផ្ញើសារទៅអ្នកប្រើប្រាស់ច្រើនអ្នកក្នុងពេលតែមួយ អ្នកត្រូវពិនិត្យមើល file ប្រភេទ csv ។ file នេះជាពត៌មានអ្នកប្រើប្រាស់អ្នកបានទាញយកពី Group or Channel ។ File នេះអ្នកអាចកែឬលុបចេញអ្នកប្រើប្រាស់ណាមួយក៏បានជាមួយកម្មវិធី Microsoft Excel (Open with Excel) ។

```py
python3 smsbot.py [filename] [text_file]
```

ឧទាហរណ៍៖ ផ្ញើអត្ថបទសារទៅ អ្នកប្រើប្រាស់ទាំងអស់ក្នុង `members.csv` ជាមួយនឹងសារអត្ថបទក្នុង `text.txt` ។

```py
python3 smsbot.py members.csv text.txt
```

- សម្រាប់លោកអ្នកចង់ផ្ញើសារទៅអ្នកប្រើប្រាស់ជាមួយ file [Video \ Audio \ File] សូមចុចដូចខាងក្រោម
  ទៅកែកូដនៅក្នុង `chat.py` ជាមួយនឹង file បន្ទាប់ដូចជា `members.csv`, `text.txt` និង​ `file_name.extension` ។

```py
python3 chat.py members.csv text.txt video.mp4
or
python3 chat.py members.csv text.txt audio.mp3
or
python3 chat.py members.csv text.txt sakcode.png
```

## Contribute to this project

> Yan Samreach - Web Developer at [Sak Code](https://sakcode.net/) - [GitHub](https://github.com/samreachyan/TeleGram) - [@samreachyan](https://t.me/samreachyan)
