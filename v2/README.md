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
  <br>How to Deploy TeleGram Scrapper API
</p>
<p align="center">
</p>

---

## API Setup

- Sign in web telegram: [https://web.telegram.org](https://web.telegram.org) and get your `api_id` and `api_hash`
- Use terminal command line: in folder `v2` and run command `python setup.py`

## How To Install and Use

```py
git clone https://github.com/samreachyan/teleGram.git
cd v2
```

Download environment [Python](https://www.python.org/downloads/) and install it.

- install some libraries:

```py
python -m pip install --upgrade pip
pip install cython telethon requests touch configparser numpy pandas dataframe_image
```

- Setup environment:

```py
python setup.py
```

- Using Python Thread (asyncio support with sending message regularly to Group or Channel) ៖

```py
python threadTelegram.py
```

## Contribute to this project

> Yan Samreach - Web Developer at [Sak Code](https://sakcode.net/) - [GitHub](https://github.com/samreachyan/TeleGram) - [@samreachyan](https://t.me/samreachyan)
