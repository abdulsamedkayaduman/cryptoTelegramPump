# Crypto Telegram Pump ![ds](https://www.resimyukle.org/images/2021/06/07/50b1d840e1608846b2c98c1b9a3cfa1a.png)
## Amaç

Telegram grupları aracılığı ile [MXC](https://www.mxcio.co/auth/signup?inviteCode=19afq) veya [Gate.io](https://www.gate.io/ref/3924862) borsalarında pumpa katılamak.
Şuanda uygulama telegramda bulunan [turkiye_pump_grup](https://t.me/turkiye_pump_grup)'nu takip etmekte.
Gelen mesajlarda "COIN ADI"  bulunan mesajlarda coin adını alıp spot işlemleri yapmakta.
Alım yapıldıktan 30 saniye sonra satım işlemi gerçekleşmekte.
Yapılan işlemlerde loglama işlemi yapılmakta. Hata alındığı taktirde loglarda görünmekte.

    Yapılan işlemler tamamen kullanıcının insiyatifindedir. Kar veya zararlarınızda her hangi bir sorumluluk kabul edilmemektedir.


## Kullanım

Adımları şu şekilde:

```bash

$ pip clone https://github.com/abdulsamedkayaduman/cryptoTelegramPump.git
$ lib klasörü içinde bulunan config.ini dosyasına api key ve secretlerin girilmesi
$ pipenv shell
$ pipenv install -r requirements.txt
$ python main.py

```

## Yapılacak Geliştirmeler
- Konfigurasyon düzenlemeleri.

## License
[MIT](https://choosealicense.com/licenses/mit/)


