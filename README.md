# K-AutoBook

## Overview

Web comics downloader. Target is _commercial_ web comics site, especially for _free_ comics.
Policy is _images as original as possible_.

## Description

Downloadable sites available,

|site|method|image|note|sample url|
|----|------|-----|----|----------|
|[alphapolis](http://www.alphapolis.co.jp/)|meta|direct file| |[📖](http://www.alphapolis.co.jp/manga/viewManga/46) [📖](http://www.alphapolis.co.jp/manga/viewOpening/138000030/)|
|[ebookjapan](http://ebookjapan.yahoo.co.jp/)|paging|screen capture|login available, cookie doesn't work |[📖](https://ebookjapan.yahoo.co.jp/books/145222/A000100547)|
|[bookpass](https://bookpass.auone.jp/)|paging|canvas data| |[📖](https://bookpass.auone.jp/pack/detail/?iid=BT000069318400100101&cs=top_freecomics_reco_670&pos=2&tab=1&ajb=3)|
|[bookwalker](https://bookwalker.jp/)|paging|canvas data| |[📖](https://viewer.bookwalker.jp/browserWebApi/03/view?cid=57c84cf2-7062-4ef9-9071-45fb249c926e)|
|[comicdays](https://comic-days.com/)|meta|direct file (re-rendered)|coreview|[📖](https://comic-days.com/volume/13932016480030155016)|
|[comicwalker](https://comic-walker.com/)|meta|direct file (decrypted)| |[📖](https://comic-walker.com/viewer/?tw=2&dlcl=ja&cid=KDCW_MF09000001010005_68)|
|[ganganonline](https://www.ganganonline.com/)|paging|direct file (blob)| |[📖](https://viewer.ganganonline.com/manga/?chapterId=15502)|
|[linemanga](https://manga.line.me/)|paging|screen capture|cookie available|[📖](https://manga.line.me/book/viewer?id=92dc0b4e-c5d4-4518-9fba-d78fb1e6b0f0)|
|[webace](https://web-ace.jp/)|meta|direct file| |[📖](https://web-ace.jp/youngaceup/contents/1000053/episode/1092/)|
|[zebrackcomic](https://zebrack-comic.com/)|paging|direct file (blob)| |[📖](https://zebrack-comic.com/title/37/volume/1498/viewer)|
|[booklive](https://booklive.jp/)|paging|direct file (blob, re-rendered)|BinB |[📖](https://booklive.jp/bviewer/s/?cid=208562_003&rurl=https%3A%2F%2Fbooklive.jp%2Findex%2Fno-charge%2Fcategory_id%2FC)|
|[jumpplus](https://shonenjumpplus.com/)|meta|direct file (re-rendered)|coreview|[📖](https://shonenjumpplus.com/episode/13932016480031086197)|
|[magazinepocket](https://pocket.shonenmagazine.com/)|meta|direct file (re-rendered)|coreview|[📖](https://pocket.shonenmagazine.com/episode/13933686331610373465)|
|[kuragebunch](https://kuragebunch.com/)|meta|direct file (re-rendered)|coreview|[📖](https://kuragebunch.com/episode/10834108156630826048)|
|[cmoa](https://www.cmoa.jp/)|paging|direct file (blob, re-rendered)|uses booklive manager, BinB, cookie available|[📖](https://www.cmoa.jp/bib/speedreader/speed.html?cid=0000101745_jp_0002&u0=1&u1=0&rurl=https%3A%2F%2Fwww.cmoa.jp%2Ftitle%2F101745%2Fvol%2F2%2F)|
|[comicaction](https://comic-action.com/)|meta|direct file (re-rendered)|coreview|[📖](https://https://comic-action.com/episode/13933686331636733009)|
|[piccoma](https://piccoma.com/)|paging|canvas data| |[📖](https://piccoma.com/web/viewer/4267/1471900)|
|[dmmbooks](https://book.dmm.com/)|paging|canvas data|cookie available|[📖](https://book.dmm.com/library/?age_limit=all&expired=0&item_id=b900pkds04308)|
|[sukima](https://www.sukima.me/)|paging|canvas data| |[📖](https://www.sukima.me/bv/t/BT0000185480/v/1/s/1/p/0)|
|[tonarinoyj](https://tonarinoyj.jp/)|meta|direct file (re-rendered)|coreview|[📖](https://tonarinoyj.jp/episode/13933686331663810200)|
|[amazon](https://amazon.co.jp/)|paging|canvas data|headless doesn't work, uses profile for login|[📖](https://read.amazon.co.jp/manga/B00JR0Q0YO?ref_=dbs_ebk_wr_lft)|

BinB ... 講談社コミックプラス, 集英社S-MANGA

## Requirement

* `Python` Python 3 (tested with 3.9.1)
* `pip` (tested with 20.3.3)
* [`ChromeDriver`](https://chromedriver.chromium.org/downloads) (tested with 91.0.4472.19)

## Install

```shell
    $ git clone https://github.com/umjammer/K-AutoBook.git
    $ cd K-AutoBook
    $ pip install -r requirements.txt
```

## Usage

```shell
    $ pwd
    .../K-AutoBook
    $ cp config.json.sample config.json
    $ ./k_auto_book.py
    Input URL > <specify the url or python script starts with '?'> <option>
```

or

```shell
    $ ./k_auto_book.py <specify the url or python script starts with '?'> <option>
```

### Examples

As input data

```shell
Input URL > https://manga.line.me/book/viewer?id=001si9is
 ︙
Input URL > https://ebookjapan.yahoo.co.jp/books/154784/A002338262/
 ︙
Input URL > ?[f'https://web-ace.jp/youngaceup/contents/1000032/episode/{n}/' for n in range(615, 655)]
```

As a command line argument

```shell
$ ./k_auto_book.py 'https://zebrack-comic.com/title/1591/volume/9727' 
︙
$ ./k_auto_book.py '?[f"https://booklive.jp/bviewer/s/?cid=731240_00{n}" for n in range(2, 6)]'
```

### How To

#### how do i specify download directory
 * add `base_directory` in `config.json`

```
    "base_directory": "/Users/you/Downloads",
```

#### how do i set cookie automatically (currently mac only?)
 * remove `site.cookie` in `config.json`
 * add `chrome_cookie_db` in `config.json`
 * add `site.host_key` and `site.top_url` in `config.json`

```
    "chrome_cookie_db": "/Users/you/Library/Application Support/Google/Chrome/Default/Cookies",
     ︙
    "cmoa": {
         ︙
        "host_key": ".cmoa.jp",
        "top_url": "https://www.cmoa.jp"
    },
```

#### how do i set cookie (for windows)

 * add `site.cookie` and `site.host_key` and `site.top_url` in `config.json`

```
     ︙
    "cmoa": {
         ︙
        "cookie": "how to get cookie: see 'https://github.com/xuzhengyi1995/Bookwalker_Downloader'",
        "host_key": ".cmoa.jp",
        "top_url": "https://www.cmoa.jp"
    },
```

#### list coreview urls

at the developer console on a browser

```ecmascript
var elements = document.getElementsByClassName("series-episode-list-container");
for (var i = 0; i < elements.length; i++) {
  console.log(elements[i].getAttribute('href'));
}
```

## TODO

 * update cookie automatically on windows
 * yahoo! japan (ebookjapan) cookie

## Author

[kuroneko](https://github.com/amu-kuroneko),
umjammer (modifier)
