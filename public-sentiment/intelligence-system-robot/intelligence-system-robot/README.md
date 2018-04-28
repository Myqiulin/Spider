# intelligence system Robot

## Robot workflow

Redis Pop ==> Robot Core ==> A Spider(==>Internet) ==> Kafka Pipeline ==> Kafka Brokers ==> Storm handler service ==> ES and HBase

## Version define

> Python 2.7.x
> Redis 3.x.x
> Kafka 0.8.x +

## Needs libs

```
pip install scrapy
pip install scrapy-redis
pip install kafka-python
pip install feedparser
pip install jieba
pip install BeautifulSoup4
pip install selenium

```

## Create spider

```
scrapy genspider <NAME> <DOMAIN>

```

## Start the spider

```
scrapy crawl <NAME>

```