# getTweet

## Install
  python setup.py Install

## Uninstall
For unix

    python setup.py install --record files.txt
    cat files.txt | xargs rm -rf

For Windows

    python setup.py install --record files.txt
    Get-Content files.txt | ForEach-Object {Remove-Item $_ -Recurse -Force}

How to use

    getTweets TwitterJP -s 2019/12/15 -t 2019/12/16 -o out.txt

Preparation

    Place a json file named .dw-tweets in your home directory.
    The contents of .dw-tweets is as follows:

    {
    "APP_NAME": "YOUR APP'S NAME",
    "CONSUMER_KEY": "YOUR APP'S KEY",
    "CONSUMER_SECRET": "YOUR APP'S CONSUMER_SECRET"
    }
