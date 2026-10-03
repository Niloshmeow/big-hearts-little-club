import { fetch } from 'wix-fetch';

const API_URL = 'https://SIZIN-PROJENIZ.onrender.com';

$w.onReady(async function () {
    $w('#leadRepeater').onItemReady(($item, itemData) => {
        $item('#isimText').text = itemData.isim;
        $item('#telefonText').text = itemData.telefon;
        $item('#yasText').text = itemData.cocuk_yasi || '–';
        $item('#hizmetText').text = itemData.hizmet || '–';
        $item('#mesajText').text = itemData.mesaj || '–';
        $item('#tarihText').text = itemData.tarih;
    });

    await leadleriYukle();
});

async function leadleriYukle() {
    try {
        const yanit = await fetch(`${API_URL}/api/leads`, { method: 'get' });
        const veri = await yanit.json();
        if (veri.basari) {
            $w('#leadRepeater').data = veri.leadler;
            $w('#toplamText').text = `Toplam ${veri.toplam} talep`;
        } else {
            $w('#toplamText').text = veri.hata;
        }
    } catch (hata) {
        $w('#toplamText').text = 'Sunucuya ulaşılamadı.';
    }
}
