## reddit-stalker

Reddit Stalker, bir Python uygulamasıdır ve belirli bir alt dizindeki gönderileri tarar. Bu gönderileri bir SQLite veritabanında saklar. Aynı zamanda, taranan gönderileri almak ve filtrelemek için bir API sunucusu da sunar.

## Nasıl kullanılır

Reddit Stalker adlı Python uygulamasının stalker.py dosyasının stalker klasörü içinde bulunduğu indirilmiş repo içerisinde, (api_info) bölümünü kendi Reddit API bilgilerinizle güncellemeniz gerekmektedir.

```code

python3 main.py

```

main.py yi çalıştırmanız yeterlidir

## Docker Build

```code

docker build -t dockerfile .
docker run -p 1453:1453 dockerfile

```

## Gerekenler

Python 3.9 veya daha yüksek python sürümü

SQLite database

## Kurulum

1 -) Repoyu inidirin.

```code

git clone <repo url>

```

2 -) indirdiğimiz klasör'e giriş yapalım.

```code

cd <repo ismi>

```

3 -) Gerekli paketlerin kurulumu.

```code

pip3 install -r requirements.txt

```
