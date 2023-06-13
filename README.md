# VoiceComparator

<p>Adli bilişim ve osint alanında varolan seslerin aynı kişiye ait olup olmadıklarını kontrol etmek için eğitimsel bir araç. Python3 resemblyzer kütüphanesine dayanmakta olan araç desteklenen formatlarda verilen sesleri (çok kısa sürelerde olsa) analiz ederek kosinüs benzerliğini kullanarak benzerliklerini hesaplamaktadır ve sonuçları verir.
<br>
<hr>
<br>
<h2>Desteklenen ses formatları:</h2>

`["MP3","OGG","FLAC","AAC","AIFF","WMA","WAV"]`


<br>
<h2>Gerekli kütüpahaneler:</h2> 

```bash
# Linux & MacOS
python3.11 -m pip install pydub numpy resemblyzer argparse time colorama

```

```bash
# Windows
pip install install pydub numpy resemblyzer argparse time colorama

```

<h2>Kullanımı:</h2>
<br>
Gerekli kütüphaneler kurulduktan sonra kullanımı gayet basittir.

```bash
cd VoiceComparator
python3.11 main.py --voice1 denemeSes1.mp3 --voice2 denemeKisi2.ogg

```

<h2>ÖRNEK:</h2>

### AYNI KİŞİYE AİT SES KARŞILAŞTIRMASI:
<img src="img/ayni.png">


<br>
<br>

### FARKLI KİŞİLERE AİT SES KARŞILAŞTIRMASI:
<img src="img/farkli.png">



<h2>Teşekkürler </h2>
<br>
Ses örnekleri sağladıkları için teşekkürler:<br>
<br>

<a href="https://t.me/sudodr"> `https://t.me/sudodr` </a><br>
<a href="https://t.me/araskargo_resmi"> `https://t.me/araskargo_resmi` </a> <br>
<a href="https://t.me/araskargo_resmi"> `https://t.me/setpassunlock`</a> <br>
</p>