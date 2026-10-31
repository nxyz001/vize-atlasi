Warning: truncated output (original token count: 23490)
Total output lines: 1519

"""Etkilesimli 3B gezegen, Gunes Sistemi ve kure yogunluk hesaplayicisi.

Gereksinim: Python 3 + tkinter.
Girdi birimleri: kutle kg, yari cap m; belirsizlikler ayni birimlerde.
Sistem haritasi şematik; NASA arşiv fotoğrafları çevrimiçi olarak isteğe bağlı yüklenir.
"""

import math
import random
import time
from pathlib import Path
import tkinter as tk
from tkinter import ttk
AU_M = 149_597_870_700.0
GEZEGENLER = [
    {"ad": "Merkür", "m": 3.3011e23, "r": 2.4397e6, "au": 0.387, "ac": 0.70,
     "renk": (158, 157, 151), "bilgi": "Güneş'e en yakın gezegen. Kraterli, küçük ve kayalık bir yüzeye sahiptir."},
    {"ad": "Venüs", "m": 4.8675e24, "r": 6.0518e6, "au": 0.723, "ac": 2.55,
     "renk": (224, 178, 99), "bilgi": "Yoğun bulutlarla örtülü, sıcak bir kayalık gezegendir."},
    {"ad": "Dünya", "m": 5.9722e24, "r": 6.3710e6, "au": 1.0, "ac": 0.0,
     "renk": (45, 126, 207), "bilgi": "Sıvı su, atmosfer ve yaşam barındıran gezegenimiz."},
    {"ad": "Mars", "m": 6.4171e23, "r": 3.3895e6, "au": 1.524, "ac": 4.20,
     "renk": (198, 91, 61), "bilgi": "İnce atmosferli kızıl gezegen; yüzeyinde büyük volkanlar ve kanyonlar bulunur."},
    {"ad": "Jüpiter", "m": 1.8982e27, "r": 6.9911e7, "au": 5.203, "ac": 5.35,
     "renk": (207, 163, 123), "bilgi": "En büyük gezegen. Bulut bantları ve Büyük Kırmızı Leke ile tanınır."},
    {"ad": "Satürn", "m": 5.6834e26, "r": 5.8232e7, "au": 9.537, "ac": 3.35,
     "renk": (219, 197, 143), "bilgi": "Belirgin halka sistemine sahip bir gaz devidir."},
    {"ad": "Uranüs", "m": 8.6810e25, "r": 2.5362e7, "au": 19.191, "ac": 1.95,
     "renk": (116, 193, 198), "bilgi": "Mavi-yeşil buz devi; dönme ekseni yörünge düzlemine çok yatıktır."},
    {"ad": "Neptün", "m": 1.02413e26, "r": 2.4622e7, "au": 30.07, "ac": 4.75,
     "renk": (66, 111, 218), "bilgi": "Güneş'e en uzak gezegen; çok hızlı rüzgârlarıyla bilinir."},
]
for _gezegen in GEZEGENLER:
    _gezegen["kategori"] = "Gezegen"

# Hızlı erişim kataloğu. Yıldızlar ve küçük cisimlerde bazı ölçüler yaklaşık değerdir.
EK_CISIMLER = [
    {"ad": "Güneş", "m": 1.9885e30, "r": 6.957e8, "renk": (255, 190, 72), "au": 0, "ac": 0,
     "kategori": "Yıldız", "bilgi": "Güneş Sistemi'nin merkezindeki yıldız."},
    {"ad": "Proxima Centauri", "m": 2.43e29, "r": 1.0e8, "renk": (235, 105, 83), "ly": 4.24,
     "kategori": "Yıldız", "bilgi": "Güneş'e en yakın yıldız; değerler yaklaşık."},
    {"ad": "Sirius A", "m": 4.02e30, "r": 1.19e9, "renk": (161, 198, 255), "ly": 8.6,
     "kategori": "Yıldız", "bilgi": "Gece göğünün en parlak yıldızlarından biri; değerler yaklaşık."},
    {"ad": "Plüton", "m": 1.303e22, "r": 1.1883e6, "renk": (177, 151, 126),
     "kategori": "Cüce gezegen", "bilgi": "Kuiper Kuşağı'ndaki cüce gezegen."},
    {"ad": "Ceres", "m": 9.3835e20, "r": 4.76e5, "renk": (157, 159, 164),
     "kategori": "Cüce gezegen", "bilgi": "Asteroit kuşağındaki cüce gezegen."},
    {"ad": "Eris", "m": 1.6466e22, "r": 1.163e6, "renk": (203, 207, 214),
     "kategori": "Cüce gezegen", "bilgi": "Uzak Kuiper Kuşağı cüce gezegeni."},
    {"ad": "Haumea", "m": 4.006e21, "r": 7.8e5, "renk": (208, 195, 169),
     "kategori": "Cüce gezegen", "bilgi": "Hızlı dönen, basık şekilli cüce gezegen; yarıçap yaklaşık."},
    {"ad": "Makemake", "m": 3.1e21, "r": 7.15e5, "renk": (190, 129, 91),
     "kategori": "Cüce gezegen", "bilgi": "Kuiper Kuşağı'nda bulunan cüce gezegen; değerler yaklaşık."},
    {"ad": "Ay", "m": 7.342e22, "r": 1.7374e6, "renk": (185, 189, 196),
     "kategori": "Uydu", "bilgi": "Dünya'nın doğal uydusu; kraterli yüzey."},
    {"ad": "Ganymede", "m": 1.4819e23, "r": 2.6312e6, "renk": (163, 157, 150),
     "kategori": "Uydu", "bilgi": "Jüpiter'in ve Güneş Sistemi'nin en büyük uydusu."},
    {"ad": "Europa", "m": 4.8e22, "r": 1.5608e6, "renk": (195, 177, 147),
     "kategori": "Uydu", "bilgi": "Jüpiter'in buzlu uydusu; yüzeyinde uzun çatlak izleri var."},
    {"ad": "Io", "m": 8.9319e22, "r": 1.8216e6, "renk": (216, 184, 95),
     "kategori": "Uydu", "bilgi": "Jüpiter'in volkanik açıdan etkin uydusu."},
    {"ad": "Titan", "m": 1.3452e23, "r": 2.5747e6, "renk": (207, 153, 86),
     "kategori": "Uydu", "bilgi": "Satürn'ün yoğun atmosferli büyük uydusu."},
    {"ad": "Callisto", "m": 1.0759e23, "r": 2.4103e6, "renk": (140, 133, 126),
     "kategori": "Uydu", "bilgi": "Jüpiter'in yoğun kraterli uydusu."},
    {"ad": "Triton", "m": 2.14e22, "r": 1.3534e6, "renk": (176, 196, 207),
     "kategori": "Uydu", "bilgi": "Neptün'ün büyük, buzlu uydusu."},
    {"ad": "Vesta", "m": 2.59e20, "r": 2.627e5, "renk": (170, 151, 133),
     "kategori": "Küçük cisim", "bilgi": "Asteroit kuşağındaki büyük kayalık cisim."},
    {"ad": "Eros", "m": 6.69e15, "r": 8.5e3, "renk": (184, 137, 105),
     "kategori": "Küçük cisim", "bilgi": "Uzunlamasına, düzensiz şekilli yakın-Dünya asteroidi; küre görünümü yaklaşık."},
    {"ad": "Halley Kuyruklu Yıldızı", "m": 2.2e14, "r": 5.5e3, "renk": (176, 194, 201),
     "kategori": "Küçük cisim", "bilgi": "Buz ve tozdan oluşan kuyruklu yıldız çekirdeği; boyut yaklaşık."},
    {"ad": "Pallas", "m": 2.04e20, "r": 2.56e5, "renk": (150, 156, 166),
     "kategori": "Küçük cisim", "au": 2.77, "ac": 2.15, "bilgi": "Asteroit kuşağındaki büyük cisim; ölçüler yaklaşık."},
    {"ad": "Hygiea", "m": 8.6e19, "r": 2.17e5, "renk": (127, 147, 148),
     "kategori": "Küçük cisim", "au": 3.14, "ac": 5.1, "bilgi": "Asteroit kuşağının büyük cisimlerinden; ölçüler yaklaşık."},
    {"ad": "Psyche", "m": 2.3e19, "r": 1.13e5, "renk": (174, 143, 115),
     "kategori": "Küçük cisim", "au": 2.92, "ac": 4.0, "bilgi": "Metalce zengin olduğu düşünülen asteroit; ölçüler yaklaşık."},
    {"ad": "Bennu", "m": 7.33e10, "r": 2.46e2, "renk": (184, 133, 93),
     "kategori": "Küçük cisim", "au": 1.13, "ac": 1.55, "bilgi": "Yakın-Dünya asteroidi; küre ve yörünge gösterimi şematiktir."},
    {"ad": "Itokawa", "m": 3.51e10, "r": 1.65e2, "renk": (184, 151, 119),
     "kategori": "Küçük cisim", "au": 1.32, "ac": 5.65, "bilgi": "Düzensiz biçimli yakın-Dünya asteroidi; küre gösterimi yaklaşık."},
]
# Güneş Sistemi'ndeki hedeflerin yaklaşık yörünge konumları (AU); uydular ebeveynleriyle bağlanır.
_AU = {"Plüton": 39.48, "Ceres": 2.77, "Eris": 67.7, "Haumea": 43.1,
       "Makemake": 45.4, "Vesta": 2.36, "Eros": 1.46,
       "Halley Kuyruklu Yıldızı": 17.8}
for _i, _cisim in enumerate(EK_CISIMLER):
    if _cisim["ad"] in _AU:
        _cisim["au"] = _AU[_cisim["ad"]]
        _cisim["ac"] = (_i * 2.399) % (2 * math.pi)
_uydular = {"Ay": ("Dünya", .25), "Ganymede": ("Jüpiter", .38), "Europa": ("Jüpiter", -.28),
            "Io": ("Jüpiter", .18), "Callisto": ("Jüpiter", -.48),
            "Titan": ("Satürn", .4), "Triton": ("Neptün", -.3)}
for _cisim in EK_CISIMLER:
    if _cisim["ad"] in _uydular:
        _cisim["parent"], _cisim["offset"] = _uydular[_cisim["ad"]]
KATALOG = GEZEGENLER + EK_CISIMLER
# Galaktik görünüm şematiktir; Güneş Sistemi ve yakın çevre aynı sahnede ölçek atlar.
GALAKSI_ISARETLERI = [
    {"ad": "Samanyolu merkezi", "kategori": "Galaksi", "pos": (660, 0, 70), "renk": "#f2b16b",
     "renk_rgb": (242, 177, 107), "boyut": 11, "gorunum_r": 16, "mesafe": "yaklaşık 26.000 ışık yılı",
     "image_query": "Milky Way Galactic Center NASA", "bilgi": "Samanyolu'nun yoğun yıldızlı merkez bölgesi.",
     "cevresi": "Yay A* süper kütleli kara deliği, yıldız kümeleri ve yoğun gaz bulutları."},
    {"ad": "Büyük Macellan Bulutu", "kategori": "Galaksi", "pos": (-520, 80, 120), "renk": "#94b9e8",
     "renk_rgb": (148, 185, 232), "boyut": 10, "gorunum_r": 14, "mesafe": "yaklaşık 160.000 ışık yılı",
     "image_query": "Large Magellanic Cloud NASA Hubble", "bilgi": "Samanyolu çevresinde dolanan düzensiz cüce gökada.",
     "cevresi": "Tarantula Bulutsusu ve yoğun yıldız oluşum bölgeleri."},
    {"ad": "Küçük Macellan Bulutu", "kategori": "Galaksi", "pos": (-590, -80, 180), "renk": "#a8c4e9",
     "renk_rgb": (168, 196, 233), "boyut": 8, "gorunum_r": 11, "mesafe": "yaklaşık 200.000 ışık yılı",
     "image_query": "Small Magellanic Cloud NASA", "bilgi": "Samanyolu'nun küçük uydu gökadalarından biri.",
     "cevresi": "Yıldız kümeleri, gaz ve toz bulutları."},
    {"ad": "Andromeda (M31)", "kategori": "Galaksi", "pos": (1420, 120, -160), "renk": "#d1c4ec",
     "renk_rgb": (209, 196, 236), "boyut": 15, "gorunum_r": 20, "mesafe": "yaklaşık 2,5 milyon ışık yılı",
     "image_query": "Andromeda Galaxy NASA Hubble", "bilgi": "Yerel Gökada Grubu'nun büyük sarmal gökadalarından.",
     "cevresi": "M32 ve M110 uydu gökadaları, yıldız oluşum bölgeleri ve toz kolları."},
    {"ad": "Üçgen Gökadası (M33)", "kategori": "Galaksi", "pos": (920, -100, -230), "renk": "#b7a5e4",
     "renk_rgb": (183, 165, 228), "boyut": 10, "gorunum_r": 15, "mesafe": "yaklaşık 2,7 milyon ışık yılı",
     "image_query": "Triangulum Galaxy M33 NASA", "bilgi": "Yerel Gökada Grubu'ndaki sarmal gökada.",
     "cevresi": "Andromeda ve Samanyolu'nun oluşturduğu yerel gökada çevresi."},
    {"ad": "Girdap Gökadası (M51)", "kategori": "Galaksi", "pos": (2050, 280, 260), "renk": "#c9a9e8",
     "renk_rgb": (201, 169, 232), "boyut": 13, "gorunum_r": 18, "mesafe": "yaklaşık 30 milyon ışık yılı",
     "image_query": "Whirlpool Galaxy M51 NASA Hubble", "bilgi": "Belirgin sarmal kolları olan etkileşen gökada.",
     "cevresi": "Yakınındaki NGC 5195 ile kütleçekimsel etkileşim."},
    {"ad": "Sombrero Gökadası (M104)", "kategori": "Galaksi", "pos": (2350, -220, 380), "renk": "#d4b98e",
     "renk_rgb": (212, 185, 142), "boyut": 12, "gorunum_r": 16, "mesafe": "yaklaşık 29 milyon ışık yılı",
     "image_query": "Sombrero Galaxy NASA Hubble", "bilgi": "Parlak çekirdeği ve geniş toz bandıyla tanınan gökada.",
     "cevresi": "Başak Gökada Kümesi yönündeki yoğun gökada alanı."},
    {"ad": "Orion Bulutsusu (M42)", "kategori": "Bulutsu", "pos": (150, 120, -90), "renk": "#e79ac4",
     "renk_rgb": (231, 154, 196), "boyut": 10, "gorunum_r": 12, "mesafe": "yaklaşık 1.350 ışık yılı",
     "image_query": "Orion Nebula NASA Hubble", "bilgi": "Yakın çevremizdeki parlak yıldız doğumevlerinden.",
     "cevresi": "Trapezium yıldız kümesi, yeni yıldızlar, gaz ve toz."},
    {"ad": "Carina Bulutsusu", "kategori": "Bulutsu", "pos": (-190, 220, -140), "renk": "#e8a66c",
     "renk_rgb": (232, 166, 108), "boyut": 13, "gorunum_r": 16, "mesafe": "yaklaşık 7.500 ışık yılı",
     "image_query": "Carina Nebula NASA Webb", "bilgi": "Devasa yıldız oluşum bölgesi; Webb'in Kozmik Uçurumları burada.",
     "cevresi": "Genç ve büyük yıldızlar, gaz sütunları ve yeni yıldız oluşum alanları."},
    {"ad": "Kartal Bulutsusu (M16)", "kategori": "Bulutsu", "pos": (330, -200, 260), "renk": "#b889db",
     "renk_rgb": (184, 137, 219), "boyut": 11, "gorunum_r": 14, "mesafe": "yaklaşık 6.500 ışık yılı",
     "image_query": "Eagle Nebula Pillars of Creation NASA", "bilgi": "Yaratılış Sütunları ile tanınan yıldız oluşum bölgesi.",
     "cevresi": "Sütun biçimli soğuk gaz ve toz; çevresinde genç, sıcak yıldızlar."},
    {"ad": "Yengeç Bulutsusu (M1)", "kategori": "Süpernova kalıntısı", "pos": (420, 260, -210), "renk": "#e47f83",
     "renk_rgb": (228, 127, 131), "boyut": 9, "gorunum_r": 11, "mesafe": "yaklaşık 6.500 ışık yılı",
     "image_query": "Crab Nebula NASA Hubble Chandra", "bilgi": "Tarihi bir süpernova patlamasından geriye kalan genişleyen kalıntı.",
     "cevresi": "Merkezde hızla dönen nötron yıldızı ve enerjik parçacık bulutu."},
    {"ad": "Ülker (Pleiades, M45)", "kategori": "Yıldız kümesi", "pos": (220, -120, 180), "renk": "#91b8ed",
     "renk_rgb": (145, 184, 237), "boyut": 9, "gorunum_r": 11, "mesafe": "yaklaşık 440 ışık yılı",
     "image_query": "Pleiades star cluster NASA", "bilgi": "Gökyüzünde çıplak gözle görülebilen genç yıldız kümesi.",
     "cevresi": "Mavi yıldızlar ve onları çevreleyen yansıma bulutsusu."},
    {"ad": "Omega Centauri", "kategori": "Yıldız kümesi", "pos": (-300, 380, 210), "renk": "#f1c77b",
     "renk_rgb": (241, 199, 123), "boyut": 10, "gorunum_r": 13, "mesafe": "yaklaşık 17.000 ışık yılı",
     "image_query": "Omega Centauri NASA Hubble", "bilgi": "Samanyolu'ndaki en büyük ve en parlak küresel yıldız kümelerinden.",
     "cevresi": "Çok sıkışık bir alanda yüz binlerce yıldız."},
    {"ad": "Alpha Centauri sistemi", "kategori": "Yıldız sistemi", "pos": (277, 5, 60), "renk": "#f5dc9b",
     "renk_rgb": (245, 220, 155), "boyut": 8, "gorunum_r": 9, "mesafe": "yaklaşık 4,37 ışık yılı",
     "image_query": "Alpha Centauri NASA", "bilgi": "Üç yıldızlı yakın sistem; Alpha Centauri A ve B ile Proxima'yı içerir.",
     "cevresi": "Proxima Centauri ve bilinen yakın yörüngeli gezegen adayları."},
    {"ad": "TRAPPIST-1 sistemi", "kategori": "Yıldız sistemi", "pos": (1880, 240, -330), "renk": "#e88d72",
     "renk_rgb": (232, 141, 114), "boyut": 8, "gorunum_r": 9, "mesafe": "yaklaşık 40 ışık yılı",
     "image_query": "TRAPPIST-1 NASA planets", "bilgi": "Soğuk bir kırmızı cücenin çevresinde yedi Dünya boyutlu gezegen bulunuyor.",
     "cevresi": "Birbirine yakın yörüngelerde dönen yedi kayalık gezegen."},
    {"ad": "Kepler-186 sistemi", "kategori": "Yıldız sistemi", "pos": (1250, -330, -420), "renk": "#e6b77e",
     "renk_rgb": (230, 183, 126), "boyut": 8, "gorunum_r": 9, "mesafe": "yaklaşık 580 ışık yılı",
     "image_query": "Kepler-186 system NASA", "bilgi": "Kırmızı cüce yıldız çevresinde birden fazla gezegen keşfedilen sistem.",
     "cevresi": "Kepler-186f, yıldızın yaşanabilir bölgesinde yer alan Dünya boyutlu gezegen."},
    {"ad": "Pinwheel Gökadası (M101)", "kategori": "Galaksi", "pos": (2240, 420, -380), "renk": "#9ebbe6",
     "renk_rgb": (158, 187, 230), "boyut": 14, "gorunum_r": 18, "mesafe": "yaklaşık 21 milyon ışık yılı",
     "image_query": "Pinwheel Galaxy M101 NASA Hubble", "bilgi": "Geniş, belirgin sarmal kollara sahip gökada.",
     "cevresi": "Sarmal kollarda parlak yıldız oluşum bölgeleri ve komşu küçük gökadalar."},
    {"ad": "Bode Gökadası (M81)", "kategori": "Galaksi", "pos": (2140, -480, -220), "renk": "#d3b7e6",
     "renk_rgb": (211, 183, 230), "boyut": 12, "gorunum_r": 16, "mesafe": "yaklaşık 12 milyon ışık yılı",
     "image_query": "Bode Galaxy M81 NASA Hubble", "bilgi": "Yakın büyük sarmal gökadalardan biri.",
     "cevresi": "M82 ve NGC 3077 ile aynı etkileşen gökada grubunda."},
    {"ad": "Centaurus A", "kategori": "Galaksi", "pos": (-2450, 420, -520), "renk": "#c49d84",
     "renk_rgb": (196, 157, 132), "boyut": 13, "gorunum_r": 17, "mesafe": "yaklaşık 12 milyon ışık yılı",
     "image_query": "Centaurus A NASA Hubble Chandra", "bilgi": "Toz bandı ve etkin çekirdeğiyle tanınan eliptik gökada.",
     "cevresi": "Merkezindeki etkin kara delikten çıkan radyo jetleri."},
    {"ad": "Başak Kümesi (M87)", "kategori": "Galaksi", "pos": (2780, 650, 430), "renk": "#d9c5a8",
     "renk_rgb": (217, 197, 168), "boyut": 14, "gorunum_r": 18, "mesafe": "yaklaşık 55 milyon ışık yılı",
     "image_query": "Messier 87 M87 NASA Hubble", "bilgi": "Başak Gökada Kümesi'nin dev eliptik gökadalarından.",
     "cevresi": "M87* kara deliğinin güçlü jetleri ve binlerce küme üyesi gökada."},
    {"ad": "Lagün Bulutsusu (M8)", "kategori": "Bulutsu", "pos": (180, -250, 170), "renk": "#db83ae",
     "renk_rgb": (219, 131, 174), "boyut": 10, "gorunum_r": 12, "mesafe": "yaklaşık 4.000 ışık yılı",
     "image_query": "Lagoon Nebula M8 NASA Hubble", "bilgi": "Yay Takımyıldızı yönünde görülen yıldız oluşum bulutsusu.",
     "cevresi": "Genç yıldız kümeleri, iyonlaşmış gaz ve karanlık toz şeritleri."},
    {"ad": "Rozet Bulutsusu", "kategori": "Bulutsu", "pos": (290, 280, 230), "renk": "#d889b9",
     "renk_rgb": (216, 137, 185), "boyut": 11, "gorunum_r": 14, "mesafe": "yaklaşık 5.000 ışık yılı",
     "image_query": "Rosette Nebula NASA", "bilgi": "Merkezinde genç bir yıldız kümesi bulunan büyük gaz bulutu.",
     "cevresi": "NGC 2244 yıldız kümesi ve yıldız rüzgârlarının açtığı merkez boşluğu."},
    {"ad": "Atbaşı Bulutsusu", "kategori": "Bulutsu", "pos": (125, 180, -150), "renk": "#a776a5",
     "renk_rgb": (167, 118, 165), "boyut": 9, "gorunum_r": 11, "mesafe": "yaklaşık 1.300 ışık yılı",
     "image_query": "Horsehead Nebula NASA Hubble", "bilgi": "Yoğun karanlık gaz ve tozun arka plan ışığını kestiği bulutsu.",
     "cevresi": "Orion moleküler bulutu ve parlak yıldız oluşum bölgeleri."},
    {"ad": "Halka Bulutsusu (M57)", "kategori": "Bulutsu", "pos": (310, -360, 230), "renk": "#86bad4",
     "renk_rgb": (134, 186, 212), "boyut": 8, "gorunum_r": 10, "mesafe": "yaklaşık 2.300 ışık yılı",
     "image_query": "Ring Nebula M57 NASA Webb", "bilgi": "Ömrünün sonundaki bir yıldızın dış katmanlarından oluşan gezegenimsi bulutsu.",
     "cevresi": "Merkezde sıcak beyaz cüce ve genişleyen gaz kabuğu."},
    {"ad": "Tarantula Bulutsusu", "kategori": "Bulutsu", "pos": (-545, 135, 145), "renk": "#e48b83",
     "renk_rgb": (228, 139, 131), "boyut": 12, "gorunum_r": 15, "mesafe": "yaklaşık 160.000 ışık yılı",
     "image_query": "Tarantula Nebula NASA Webb", "bilgi": "Yerel gökada çevresinin en parlak yıldız doğumevlerinden.",
     "cevresi": "Büyük Macellan Bulutu içindeki genç ve çok büyük yıldız kümeleri."},
    {"ad": "Arı Kovanı Kümesi (M44)", "kategori": "Yıldız kümesi", "pos": (185, 160, 210), "renk": "#f0d38c",
     "renk_rgb": (240, 211, 140), "boyut": 8, "gorunum_r": 10, "mesafe": "yaklaşık 600 ışık yılı",
     "image_query": "Beehive Cluster M44 NASA", "bilgi": "Yakın ve parlak açık yıldız kümelerinden biri.",
     "cevresi": "Birbirine gevşekçe bağlı genç yıldızlar ve çevresindeki galaktik alan."},
    {"ad": "Çift Küme (NGC 869/884)", "kategori": "Yıldız kümesi", "pos": (310, 400, -240), "renk": "#9bb8ee",
     "renk_rgb": (155, 184, 238), "boyut": 10, "gorunum_r": 12, "mesafe": "yaklaşık 7.500 ışık yılı",
     "image_query": "Double Cluster NGC 869 884 NASA", "bilgi": "Gökyüzünde yan yana görünen iki genç açık yıldız kümesi.",
     "cevresi": "Perseus kolundaki parlak mavi yıldızlar ve yıldızlararası gaz."},
    {"ad": "Tau Ceti sistemi", "kategori": "Yıldız sistemi", "pos": (590, 130, -180), "renk": "#f5dda6",
     "renk_rgb": (245, 221, 166), "boyut": 7, "gorunum_r": 8, "mesafe": "yaklaşık 12 ışık yılı",
     "image_query": "Tau Ceti NASA exoplanet", "bilgi": "Güneş'e yakın, Güneş benzeri bir yıldız sistemi.",
     "cevresi": "Yıldız çevresinde toz diski ve aday gezegenler."},
    {"ad": "Beta Pictoris sistemi", "kategori": "Yıldız sistemi", "pos": (-760, -250, 370), "renk": "#d9e6f0",
     "renk_rgb": (217, 230, 240), "boyut": 8, "gorunum_r": 9, "mesafe": "yaklaşık 63 ışık yılı",
     "image_query": "Beta Pictoris NASA disk", "bilgi": "Genç yıldızı çevreleyen belirgin enkaz diskiyle bilinen sistem.",
     "cevresi": "Toz ve kaya parçalarından oluşan disk, gezegenler ve kuyruklu yıldızlar."},
    {"ad": "Kepler-452 sistemi", "kategori": "Yıldız sistemi", "pos": (2460, -650, 200), "renk": "#ecc88d",
     "renk_rgb": (236, 200, 141), "boyut": 8, "gorunum_r": 9, "mesafe": "yaklaşık 1.800 ışık yılı",
     "image_query": "Kepler-452 NASA system", "bilgi": "Güneş benzeri yıldız çevresindeki gezegenleriyle incelenen sistem.",
     "cevresi": "Kepler-452b; gezegenin gerçek yüzeyi doğrudan görüntülenmiş değildir."},
    {"ad": "LHS 1140 sistemi", "kategori": "Yıldız sistemi", "pos": (-1920, 470, 360), "renk": "#e4a98b",
     "renk_rgb": (228, 169, 139), "boyut": 7, "gorunum_r": 8, "mesafe": "yaklaşık 49 ışık yılı",
     "image_query": "LHS 1140 NASA exoplanet", "bilgi": "Kırmızı cüce yıldız çevresindeki gezegenleri atmosfer çalışmalarıyla araştırılıyor.",
     "cevresi": "LHS 1140 b; atmosferi ve olası su durumu teleskop gözlemleriyle inceleniyor."},
]
# Keşif kataloğunu Güneş Sistemi dışına taşır: uzaklık koordinatları harita için sıkıştırılmıştır.
GALAKSI_ISARETLERI.extend([
    {"ad": "Heykeltıraş Cüce Gökadası", "kategori": "Galaksi", "pos": (-680, -130, 240), "renk": "#b2c7e4",
     "renk_rgb": (178, 199, 228), "boyut": 7, "gorunum_r": 10, "mesafe": "yaklaşık 290.000 ışık yılı",
     "image_query": "Sculptor Dwarf Galaxy NASA", "bilgi": "Samanyolu çevresindeki yakın cüce gökadalardan.",
     "cevresi": "Samanyolu'nun kütleçekimsel etkisindeki yaşlı yıldızlar."},
    {"ad": "Fornax Cüce Gökadası", "kategori": "Galaksi", "pos": (-760, 250, 300), "renk": "#c5b9dc",
     "renk_rgb": (197, 185, 220), "boyut": 7, "gorunum_r": 10, "mesafe": "yaklaşık 460.000 ışık yılı",
     "image_query": "Fornax Dwarf Galaxy NASA", "bilgi": "Samanyolu'nun uydu gökadalarından biri.",
     "cevresi": "Birden fazla küresel yıldız kümesi ve eski yıldız toplulukları."},
    {"ad": "Leo I", "kategori": "Galaksi", "pos": (-840, 160, -280), "renk": "#aebfe0",
     "renk_rgb": (174, 191, 224), "boyut": 7, "gorunum_r": 10, "mesafe": "yaklaşık 820.000 ışık yılı",
     "image_query": "Leo I Dwarf Galaxy NASA Hubble", "bilgi": "Aslan takımyıldızı yönündeki sönük küresel cüce gökada.",
     "cevresi": "Samanyolu'nun dış halesinde seyrek yıldızlar."},
    {"ad": "NGC 6822 (Barnard Gökadası)", "kategori": "Galaksi", "pos": (1050, 290, 200), "renk": "#c89bb4",
     "renk_rgb": (200, 155, 180), "boyut": 9, "gorunum_r": 12, "mesafe": "yaklaşık 1,6 milyon ışık yılı",
     "image_query": "NGC 6822 Barnard Galaxy NASA", "bilgi": "Yerel Gökada Grubu'ndaki düzensiz cüce gökada.",
     "cevresi": "Hidrojen gazı bulutları ve yıldız oluşum bölgeleri."},
    {"ad": "Heykeltıraş Gökadası (NGC 253)", "kategori": "Galaksi", "pos": (-2860, -450, 700), "renk": "#d7aa92",
     "renk_rgb": (215, 170, 146), "boyut": 13, "gorunum_r": 17, "mesafe": "yaklaşık 11 milyon ışık yılı",
     "image_query": "Sculptor Galaxy NGC 253 NASA Webb", "bilgi": "Yakın ve parlak, kenardan görülen sarmal gökada.",
     "cevresi": "Merkezinde yoğun yıldız oluşumu ve dışarı akan sıcak gaz."},
    {"ad": "Güney Fırıldak Gökadası (M83)", "kategori": "Galaksi", "pos": (-3100, 380, -760), "renk": "#d3b3d9",
     "renk_rgb": (211, 179, 217), "boyut": 13, "gorunum_r": 17, "mesafe": "yaklaşık 15 milyon ışık yılı",
     "image_query": "Southern Pinwheel Galaxy M83 NASA Hubble", "bilgi": "Parlak çekirdeği ve belirgin sarmal kollarıyla bilinen gökada.",
     "cevresi": "Sarmal kollara yayılmış yıldız kümeleri ve süpernova kalıntıları."},
    {"ad": "NGC 1300", "kategori": "Galaksi", "pos": (3240, -420, 760), "renk": "#b9a6de",
     "renk_rgb": (185, 166, 222), "boyut": 12, "gorunum_r": 16, "mesafe": "yaklaşık 61 milyon ışık yılı",
     "image_query": "NGC 1300 barred spiral NASA Hubble", "bilgi": "Merkezinden uzanan çubuğu ve sarmal kollarıyla çubuklu gökada.",
     "cevresi": "Yıldız oluşum bölgeleri ve gökada diskinin toz şeritleri."},
    {"ad": "Anten Gökadaları", "kateg…11490 tokens truncated…a_secimi is None and ilerleme < 0.60 else
                      f"HEDEF KONUMU: {self.harita_secimi['ad'].upper()}" if self.harita_secimi else
                      "YILDIZLAR VE GÖKADALAR" if gorunum_mesafesi > 500 else
                      "GÜNEŞ SİSTEMİ" if gorunum_mesafesi > 35 else (
                          f"{self.gezegen['ad'].upper()} YÖRÜNGESİ" if self.gezegen else "KÜRESEL CİSİM"))
            c.create_text(w / 2, 19, text=baslik + "  •  Sürükleyerek kamerayı döndürün",
                          fill="#e2eaf5", font=("Segoe UI", 10, "bold"))
            if self.nav_stage == "yaklasma":
                c.create_text(w / 2, h - 14,
                              text=f"Hedefe doğru ilerleniyor: {self.nav_target['ad']}  •  {self.nav_progress*100:.0f}%",
                              fill="#c9d9ee", font=("Segoe UI", 9))
            elif self.harita_secimi:
                c.create_text(w / 2, h - 14,
                              text="İşaretli cisme yakından bakmak için sahnedeki simgesine tıklayın",
                              fill="#ffe5aa", font=("Segoe UI", 9, "bold"))
            elif ilerleme > 0.45:
                c.create_text(w / 2, h - 14,
                              text="Bir gezegene tıklayarak ona yolculuk edin  •  Tekerlek: yaklaş / uzaklaş",
                              fill="#b1c0d5", font=("Segoe UI", 9))
            else:
                c.create_text(w / 2, h - 14,
                              text="Yakınlaşmak veya uzaklaşmak için fare tekerleğini kullanın",
                              fill="#b1c0d5", font=("Segoe UI", 9))
        finally:
            self.cizim_suruyor = False

    def projekte_et(self, nokta, hedef, olcek, cx, cy):
        x, y, z = (nokta[i] - hedef[i] for i in range(3))
        xr, yr, _zr = self.donustur(x, y, z)
        return cx + xr * olcek, cy - yr * olcek

    def gunes_sistemini_ciz(self, c, w, h, ilerleme):
        cx, cy = w / 2, h / 2
        hedef = self.gezegen_konumu(self.hedeflenen_gezegen) if self.hedeflenen_gezegen else (1.0, 0.0, 0.0)
        if hedef is None:
            hedef = (0.0, 0.0, 0.0)
        if self.nav_stage == "yaklasma":
            hedef = self.nav_focus
        else:
            hedef = tuple(v * (1 - ilerleme) for v in hedef)
        mesafe = math.exp(self.log_mesafe)
        olcek = min(w * 0.48, h * 0.43) / mesafe
        orbit_rengi = karistir("#050914", "#293b55", min(1, ilerleme * 1.5))
        gorunenler = []

        # Iç yörüngeleri ekranda ayırmak için sahne içinde sıkıştırılmış uzaklıklar kullanılır.
        for gezegen in GEZEGENLER:
            pos = self.gezegen_konumu(gezegen)
            yaricap = math.hypot(pos[0], pos[2])
            noktalar = []
            for step in range(73):
                a = 2 * math.pi * step / 72
                nokta = (yaricap * math.cos(a), 0.0, yaricap * math.sin(a))
                px, py = self.projekte_et(nokta, hedef, olcek, cx, cy)
                noktalar.extend((px, py))
            c.create_line(noktalar, fill=orbit_rengi, width=1, smooth=True)

        gunes_xy = self.projekte_et((0, 0, 0), hedef, olcek, cx, cy)
        gunes_r = 3.0 + 5.0 * ilerleme
        for katsayi, renk in ((1.8, "#382b1b"), (1.35, "#79552a"), (1.0, "#ffd16b")):
            rr = gunes_r * katsayi
            c.create_oval(gunes_xy[0] - rr, gunes_xy[1] - rr, gunes_xy[0] + rr,
                          gunes_xy[1] + rr, fill=renk, outline="")

        self.vuruslar = []
        etiket_kaymalari = {
            "Merkür": (-22, -15), "Venüs": (19, -16), "Dünya": (20, 16), "Mars": (-22, 17),
            "Jüpiter": (18, -17), "Satürn": (-18, 17), "Uranüs": (18, -16), "Neptün": (-18, 17),
        }
        for gezegen in GEZEGENLER:
            pos = self.gezegen_konumu(gezegen)
            x, y = self.projekte_et(pos, hedef, olcek, cx, cy)
            if x < -35 or x > w + 35 or y < -35 or y > h + 35:
                continue
            fiziksel = self.cisim_gorunum_yaricapi(gezegen) * olcek
            en_kucuk = 3.5 + max(0, math.log10(gezegen["r"]) - 6) * 1.25
            rr = max(fiziksel, en_kucuk * ilerleme)
            rr = min(rr, min(w, h) * 0.08)
            renk = "#%02x%02x%02x" % gezegen["renk"]
            # Gezegen diski ve ince aydinlik kenar, arka plandan ayrilmasini saglar.
            c.create_oval(x - rr - 2, y - rr - 2, x + rr + 2, y + rr + 2,
                          fill="#101a2b", outline="")
            c.create_oval(x - rr, y - rr, x + rr, y + rr,
                          fill=renk, outline="#e0d5bd", width=1)
            if rr > 18:
                self.gezegen_kuresini_ciz(c, gezegen, x, y, rr)
            if ilerleme > 0.73 and rr < 16:
                dx, dy = etiket_kaymalari[gezegen["ad"]]
                tx, ty = x + dx, y + dy
                c.create_line(x, y, tx, ty, fill="#a8b8ce", width=1)
                c.create_text(tx, ty, text=gezegen["ad"], fill="#edf3fb",
                              font=("Segoe UI", 8, "bold"))
            self.vuruslar.append((x, y, rr, gezegen))
            gorunenler.append(gezegen["ad"])

        # Yakın yıldızlar ve galaksiler, uzaklaştırdıkça aynı döndürülebilir sahnede belirir.
        if mesafe > 85:
            for cisim in EK_CISIMLER:
                if cisim.get("kategori") != "Yıldız" or "ly" not in cisim:
                    continue
                pos = self.gezegen_konumu(cisim)
                x, y = self.projekte_et(pos, hedef, olcek, cx, cy)
                if -24 < x < w+24 and -24 < y < h+24:
                    col = "#%02x%02x%02x" % cisim["renk"]
                    c.create_oval(x-5, y-5, x+5, y+5, fill=col, outline="#fff1d0", width=1)
                    c.create_text(x+9, y-8, anchor="w", text=f"{cisim['ad']} · {cisim['ly']} ışık yılı",
                                  fill="#dce8f8", font=("Segoe UI", 8))
                    self.vuruslar.append((x, y, 7, cisim))
            for galaksi in GALAKSI_ISARETLERI:
                x, y = self.projekte_et(galaksi["pos"], hedef, olcek, cx, cy)
                if -35 < x < w+35 and -35 < y < h+35:
                    r = galaksi["boyut"]
                    if galaksi["kategori"] == "Galaksi":
                        c.create_oval(x-r, y-r*.62, x+r, y+r*.62,
                                      fill=galaksi["renk"], outline="#e2dcf0", width=1)
                        c.create_oval(x-r*.48, y-r*.3, x+r*.48, y+r*.3,
                                      fill="#f5e9ce", outline="")
                    elif galaksi["kategori"] == "Yıldız sistemi":
                        for scale in (.55, .85):
                            c.create_oval(x-r*scale, y-r*.35*scale, x+r*scale, y+r*.35*scale,
                                          outline="#687c9a")
                        c.create_oval(x-3, y-3, x+3, y+3, fill=galaksi["renk"], outline="#fff1c4")
                    elif galaksi["kategori"] == "Yıldız kümesi":
                        rng = random.Random(sum(ord(ch) for ch in galaksi["ad"]))
                        for _ in range(18):
                            dx, dy = rng.uniform(-r, r), rng.uniform(-r*.5, r*.5)
                            c.create_oval(x+dx-1, y+dy-1, x+dx+1, y+dy+1,
                                          fill=galaksi["renk"], outline="")
                    elif galaksi["kategori"] == "Bulutsu":
                        for scale, col in ((1, "#28203c"), (.65, galaksi["renk"]), (.28, "#efd4e8")):
                            c.create_oval(x-r*scale, y-r*.62*scale, x+r*scale, y+r*.62*scale,
                                          fill=col, outline="")
                    else:
                        c.create_oval(x-r, y-r*.62, x+r, y+r*.62,
                                      outline=galaksi["renk"], width=2)
                    c.create_text(x, y-r-8, text=galaksi["ad"], fill="#e4e9f4",
                                  font=("Segoe UI", 8, "bold"))
                    self.vuruslar.append((x, y, max(9, r), galaksi))

        # Seçili cüce gezegen/uydu/asteroit, ana gezegenlerin yörünge düzenini kalabalıklaştırmadan işaretlenir.
        hedef_cisim = self.harita_secimi or self.nav_target or (
            self.gezegen if self.gezegen and self.gezegen.get("kategori") != "Gezegen" else None)
        if hedef_cisim:
            pos = self.gezegen_konumu(hedef_cisim)
            if hedef_cisim.get("kategori") == "Yıldız":
                if pos:
                    x, y = self.projekte_et(pos, hedef, olcek, cx, cy)
                    if -30 < x < w+30 and -30 < y < h+30:
                        c.create_oval(x-10, y-10, x+10, y+10, outline="#ffe08a", width=2)
                        c.create_text(x+14, y-13, anchor="w", text=hedef_cisim["ad"],
                                      fill="#fff0bd", font=("Segoe UI", 8, "bold"))
                        self.vuruslar.append((x, y, 10, hedef_cisim))
            elif pos:
                x, y = self.projekte_et(pos, hedef, olcek, cx, cy)
                if -30 < x < w+30 and -30 < y < h+30:
                    c.create_oval(x-10, y-10, x+10, y+10, outline="#ffe08a", width=2)
                    c.create_text(x+14, y-13, anchor="w", text=hedef_cisim["ad"],
                                  fill="#fff0bd", font=("Segoe UI", 8, "bold"))
                    self.vuruslar.append((x, y, 10, hedef_cisim))

        # Yakın görünümde seçilen gezegeni kadrajda tutan küçük yön göstergesi.
        if ilerleme < 0.16 and self.gezegen:
            c.create_text(cx, h * 0.82, text=f"{self.gezegen['ad']}  •  {self.gezegen['bilgi']}",
                          fill="#d6e2f1", font=("Segoe UI", 9))

    def gezegen_gorunumunu_ciz(self, c, w, h):
        merkez = (w / 2, h / 2 + 2)
        gezegen = self.gezegen
        rad = self.gezegen_ekran_yaricapi(w, h)
        if gezegen:
            renk = gezegen["renk"]
        else:
            renk = (48, 127, 198)
        # Hafif atmosfer parlamasi.
        for i, factor in enumerate((1.16, 1.08, 1.02)):
            rr = rad * factor
            col = ("#10243b", "#17304b", "#233d58")[i]
            c.create_oval(merkez[0] - rr, merkez[1] - rr, merkez[0] + rr,
                          merkez[1] + rr, fill=col, outline="")
        if gezegen and gezegen["ad"] == "Satürn" and rad > 24:
            self.saturn_halkalari(c, merkez, rad, sadece_arka=True)
        self.gezegen_kuresini_ciz(c, gezegen, merkez[0], merkez[1], rad)
        if gezegen and gezegen["ad"] == "Satürn" and rad > 24:
            self.saturn_halkalari(c, merkez, rad, sadece_arka=False)
        if self.guncel_r and self.guncel_dr > 0:
            d = rad * (1 + min(self.guncel_dr / self.guncel_r, 0.35))
            c.create_oval(merkez[0] - d, merkez[1] - d, merkez[0] + d, merkez[1] + d,
                          outline="#ffd166", dash=(4, 4), width=1)

    def derin_uzay_gorunumunu_ciz(self, c, w, h, nesne, scale=1.0, center=None):
        """Derin uzay hedefini kamera döndükçe perspektif değiştiren 3B noktalarla çizer."""
        cx, cy = center or (w / 2, h / 2 + 8)
        r = max(2.0, min(w, h) * .245 * max(.02, min(5.0, scale)))
        renk = nesne["renk"]
        rng = random.Random(sum(ord(ch) for ch in nesne["ad"]))
        tip = nesne["kategori"]

        def ekran(x, y, z):
            xr, yr, _ = self.donustur(x, y, z)
            return cx + xr * r, cy - yr * r

        def elips(rx, ry, z, color, width=1, fill=None):
            pts = []
            for i in range(65):
                a = 2 * math.pi * i / 64
                pts.extend(ekran(rx * math.cos(a), ry * math.sin(a), z))
            if fill:
                c.create_polygon(pts, fill=fill, outline=color, smooth=True, splinesteps=12)
            else:
                c.create_line(pts, fill=color, width=width, smooth=True)

        if tip == "Galaksi":
            elips(1.0, .30, 0, "", fill="#111525")
            elips(.72, .21, .015, "", fill=renk)
            arms = 2 if "Andromeda" in nesne["ad"] else 3
            if "Macellan" in nesne["ad"]:
                arms = 0
                for _ in range(240):
                    x, y, z = rng.gauss(0, .38), rng.gauss(0, .2), rng.uniform(-.16, .16)
                    if x*x + y*y*2.3 < 1:
                        px, py = ekran(x, y, z)
                        dot = rng.choice((1, 1, 2, 3))
                        c.create_oval(px-dot, py-dot, px+dot, py+dot,
                                      fill=rng.choice((renk, "#f4d8b5", "#bac8e2")), outline="")
            for arm in range(arms):
                for i in range(110):
                    t = i / 109
                    a = t * 4.8 * math.pi + arm * 2 * math.pi / arms
                    rr = .12 + .84 * t
                    x, y = rr * math.cos(a), rr * math.sin(a) * .30
                    z = .10 * math.sin(a * .55 + arm) * t
                    px, py = ekran(x, y, z)
                    dot = 1 if i % 4 else 2
                    c.create_oval(px-dot, py-dot, px+dot, py+dot,
                                  fill="#f4d9b4" if i % 5 else renk, outline="")
            sx, sy = ekran(0, 0, .08)
            c.create_oval(sx-r*.12, sy-r*.12, sx+r*.12, sy+r*.12,
                          fill="#fff0c6", outline="")
        elif tip == "Bulutsu":
            # Derinlikte dağılmış gaz düğümleri, sürüklemeyle birbirine göre kayarak hacim hissi verir.
            for i in range(20):
                x, y, z = rng.gauss(0, .34), rng.gauss(0, .20), rng.uniform(-.42, .42)
                px, py = ekran(x, y, z)
                size = r * rng.uniform(.10, .27)
                col = ("#201a38", renk, "#643d79", "#9d5b87")[i % 4]
                c.create_oval(px-size, py-size*.68, px+size, py+size*.68,
                              fill=col, outline="")
            for _ in range(125):
                x, y, z = rng.gauss(0, .38), rng.gauss(0, .23), rng.uniform(-.5, .5)
                px, py = ekran(x, y, z)
                dot = rng.choice((1, 1, 2))
                c.create_oval(px-dot, py-dot, px+dot, py+dot,
                              fill=rng.choice(("#fff1d4", "#d8d7ef", renk)), outline="")
        elif tip == "Yıldız sistemi":
            for i, factor in enumerate((.34, .55, .76, .97)):
                elips(factor, factor*.42, (i-1.5)*.018, "#536884")
                a = self.yaw * .35 + i * 1.71
                px, py = ekran(math.cos(a)*factor, math.sin(a)*factor*.42, (i-1.5)*.018)
                c.create_oval(px-3, py-3, px+3, py+3, fill="#a9c8f5", outline="")
            sx, sy = ekran(0, 0, 0)
            c.create_oval(sx-13, sy-13, sx+13, sy+13, fill=renk, outline="#fff0c4", width=2)
        elif tip == "Yıldız kümesi":
            for _ in range(280):
                x, y, z = rng.gauss(0, .31), rng.gauss(0, .21), rng.gauss(0, .16)
                px, py = ekran(x, y, z)
                dot = rng.choice((1, 1, 1, 2, 3))
                c.create_oval(px-dot, py-dot, px+dot, py+dot,
                              fill=rng.choice(("#fff1d4", renk, "#9db9e5")), outline="")
        else:
            for factor in (1.0, .78, .52):
                elips(factor, factor*.57, 0, renk, width=2)
            sx, sy = ekran(0, 0, 0)
            c.create_oval(sx-r*.12, sy-r*.12, sx+r*.12, sy+r*.12,
                          fill="#eaf1ff", outline="")
            for _ in range(100):
                a, rr = rng.random()*2*math.pi, math.sqrt(rng.random())
                px, py = ekran(math.cos(a)*rr, math.sin(a)*rr*.55, rng.uniform(-.08, .08))
                c.create_oval(px-1, py-1, px+1, py+1, fill=renk, outline="")
        c.create_text(cx, h-55, text=nesne.get("mesafe", "Derin uzay hedefi"),
                      fill="#cad8ec", font=("Segoe UI", 9))
        c.create_text(cx, h-37, text=nesne.get("cevresi", ""), width=w*.82,
                      fill="#aebed3", font=("Segoe UI", 8))

    def gezegen_kuresini_ciz(self, c, gezegen, cx, cy, rad):
        ad = gezegen["ad"] if gezegen else ""
        renk = gezegen["renk"] if gezegen else (48, 127, 198)
        if gezegen and gezegen.get("kategori") == "Yıldız":
            col = "#%02x%02x%02x" % renk
            for factor, glow in ((1.75, "#201b28"), (1.42, "#493328"), (1.16, "#9b6741")):
                rr = rad * factor
                c.create_oval(cx-rr, cy-rr, cx+rr, cy+rr, fill=glow, outline="")
            c.create_oval(cx-rad, cy-rad, cx+rad, cy+rad, fill=col,
                          outline="#fff0c4", width=2)
            for angle in range(0, 360, 45):
                a = math.radians(angle)
                c.create_line(cx + math.cos(a)*rad*1.1, cy + math.sin(a)*rad*1.1,
                              cx + math.cos(a)*rad*1.35, cy + math.sin(a)*rad*1.35,
                              fill="#ffdda0", width=1)
            return
        if rad < 5:
            c.create_oval(cx - rad, cy - rad, cx + rad, cy + rad,
                          fill="#%02x%02x%02x" % renk, outline="#dbe9f6")
            return
        # Dusuk poligonlu, on-yuz isiklandirmali kure; surekli animasyonda da hafiftir.
        n_lat, n_lon = (12, 24) if rad > 50 else (8, 16)
        rows = []
        for i in range(n_lat + 1):
            lat = -math.pi / 2 + math.pi * i / n_lat
            row = []
            for j in range(n_lon + 1):
                lon = 2 * math.pi * j / n_lon
                row.append(self.donustur(math.cos(lat) * math.cos(lon),
                                         math.cos(lat) * math.sin(lon), math.sin(lat)))
            rows.append(row)
        lamp = (0.30, -0.42, 0.86)
        ln = math.sqrt(sum(v * v for v in lamp))
        lamp = tuple(v / ln for v in lamp)
        yuzeyler = []
        for i in range(n_lat):
            enlem = -90 + 180 * (i + .5) / n_lat
            for j in range(n_lon):
                a, b = rows[i][j], rows[i][j + 1]
                d, e = rows[i + 1][j], rows[i + 1][j + 1]
                boylam = (360 * (j + .5) / n_lon + 180) % 360 - 180
                kara = ad == "Dünya" and any(self.nokta_poligon_icinde(boylam, enlem, k) for k in KITALAR)
                for tri in ((a, b, e), (a, e, d)):
                    z = sum(p[2] for p in tri) / 3
                    if z <= 0:
                        continue
                    nx, ny, nz = (sum(p[q] for p in tri) / 3 for q in range(3))
                    nl = math.sqrt(nx * nx + ny * ny + nz * nz) or 1
                    lum = max(0, (nx * lamp[0] + ny * lamp[1] + nz * lamp[2]) / nl)
                    base = (69, 151, 81) if kara else renk
                    band = 0.78 if ad in ("Jüpiter", "Satürn") and int((enlem + 90) / 10) % 2 else 1
                    factor = max(.2, (0.30 + 0.70 * lum) * band)
                    col = "#%02x%02x%02x" % tuple(int(min(255, v * factor)) for v in base)
                    pts = []
                    for x, y, _ in tri:
                        pts.extend((cx + rad * x, cy - rad * y))
                    yuzeyler.append((z, pts, col))
        for _z, pts, col in sorted(yuzeyler, key=lambda f: f[0]):
            c.create_polygon(pts, fill=col, outline=col)
        c.create_oval(cx - rad, cy - rad, cx + rad, cy + rad, outline="#a8c6de", width=1)

        # Kureyi gercek bir cisim gibi gosteren enlem-boylam cizgileri.
        enlemler = range(-75, 76, 15) if ad == "Dünya" and rad > 70 else (-60, 0, 60)
        for enlem_deg in enlemler:
            enlem = math.radians(enlem_deg)
            self.kure_egrisi(c, cx, cy, rad,
                             lambda boylam: (math.cos(enlem) * math.cos(boylam),
                                             math.cos(enlem) * math.sin(boylam), math.sin(enlem)))
        meridyenler = range(24) if ad == "Dünya" and rad > 70 else range(8)
        for meridyen in meridyenler:
            lon = 2 * math.pi * meridyen / len(meridyenler)
            self.kure_egrisi(c, cx, cy, rad,
                             lambda lat, lon=lon: (math.cos(lat) * math.cos(lon),
                                                   math.cos(lat) * math.sin(lon), math.sin(lat)))
        if self.dunya_modu and rad > 20:
            lat, lon = math.radians(self.enlem), math.radians(self.boylam)
            p = self.donustur(math.cos(lat) * math.cos(lon), math.cos(lat) * math.sin(lon), math.sin(lat))
            if p[2] > 0.015:
                x, y = cx + rad * p[0], cy - rad * p[1]
                c.create_oval(x-5, y-5, x+5, y+5, fill="#ffe08a", outline="#111827", width=2)
                c.create_text(x+8, y-10, anchor="w", text=f"{self.enlem:.1f}°, {self.boylam:.1f}°",
                              fill="#fff0bd", font=("Segoe UI", 8, "bold"))
        if ad == "Mars" and rad > 65:
            self.mars_kraterleri(c, cx, cy, rad)
        if ad == "Jüpiter" and rad > 65:
            # Buyuk Kirmizi Leke'yi stilize oval olarak goster.
            p = self.donustur(-.66, .05, .75)
            if p[2] > 0.05:
                x, y = cx + rad * p[0], cy - rad * p[1]
                c.create_oval(x - rad * .12, y - rad * .055, x + rad * .12,
                              y + rad * .055, fill="#a95d47", outline="#e3ad75")

    def kure_egrisi(self, c, cx, cy, rad, nokta_fonksiyonu):
        parcalar, pts = [], []
        for step in range(37):
            angle = -math.pi + 2 * math.pi * step / 36
            xyz = nokta_fonksiyonu(angle)
            x, y, z = self.donustur(*xyz)
            if z >= 0.015:
                pts.extend((cx + rad * x, cy - rad * y))
            elif len(pts) >= 4:
                parcalar.append(pts)
                pts = []
            else:
                pts = []
        if len(pts) >= 4:
            parcalar.append(pts)
        for parca in parcalar:
            c.create_line(parca, fill="#bed7e9", width=1, smooth=True)

    def mars_kraterleri(self, c, cx, cy, rad):
        # Sabit enlem-boylamdagi krater izleri, Mars donerken kureyle beraber hareket eder.
        kraterler = [(-.42, .30, .045), (.18, -.13, .065), (.53, .23, .035),
                     (-.12, -.47, .04), (.35, -.52, .03), (-.62, -.08, .025)]
        for lat, lon, boyut in kraterler:
            p = self.donustur(math.cos(lat) * math.cos(lon), math.cos(lat) * math.sin(lon), math.sin(lat))
            if p[2] > 0.08:
                x, y = cx + rad * p[0], cy - rad * p[1]
                rr = max(2, rad * boyut)
                c.create_oval(x - rr, y - rr * .65, x + rr, y + rr * .65,
                              outline="#713d32", width=max(1, int(rad / 100)))

    def saturn_halkalari(self, c, merkez, rad, sadece_arka):
        # Halkalar, gezegen kureciginden once/sonra iki parcada cizilerek hacim hissi verir.
        cx, cy = merkez
        for dis, ic, renk in ((1.72, 1.48, "#c8b58c"), (1.43, 1.28, "#e1cf9f")):
            onceki = None
            for i in range(49):
                a = 2 * math.pi * i / 48
                p = self.donustur(math.cos(a), math.sin(a), 0)
                if (p[2] < 0) != sadece_arka:
                    onceki = None
                    continue
                q = self.donustur(math.cos(a) * ic, math.sin(a) * ic, 0)
                d = self.donustur(math.cos(a) * dis, math.sin(a) * dis, 0)
                pts = (cx + rad * q[0], cy - rad * q[1],
                       cx + rad * d[0], cy - rad * d[1])
                if onceki is not None:
                    c.create_line(onceki[2], onceki[3], pts[2], pts[3], fill=renk, width=2)
                onceki = pts


if __name__ == "__main__":
    root = tk.Tk()
    app = YogunlukUygulamasi(root)
    root.mainloop()

