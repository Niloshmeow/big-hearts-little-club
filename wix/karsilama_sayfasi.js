import { fetch } from 'wix-fetch';

const API_URL = 'https://SIZIN-PROJENIZ.onrender.com';

let gecmis = [];

$w.onReady(function () {
    $w('#sorButton').onClick(() => soruSor());
    $w('#kaydetButton').onClick(() => leadKaydet());
});

async function soruSor() {
    const mesaj = $w('#mesajInput').value.trim();
    if (!mesaj) {
        $w('#cevapText').text = 'Lütfen bir soru yazın.';
        return;
    }
    $w('#sorButton').disable();
    $w('#cevapText').text = 'Yazıyor…';

    try {
        const yanit = await fetch(`${API_URL}/api/sohbet`, {
            method: 'post',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mesaj: mesaj, gecmis: gecmis })
        });
        const veri = await yanit.json();
        if (veri.basari) {
            $w('#cevapText').text = veri.cevap;
            gecmis.push({ role: 'user', content: mesaj });
            gecmis.push({ role: 'assistant', content: veri.cevap });
            $w('#mesajInput').value = '';
        } else {
            $w('#cevapText').text = veri.hata;
        }
    } catch (hata) {
        $w('#cevapText').text = 'Sunucuya ulaşılamadı. Lütfen tekrar deneyin.';
    } finally {
        $w('#sorButton').enable();
    }
}

async function leadKaydet() {
    const govde = {
        isim: $w('#isimInput').value.trim(),
        telefon: $w('#telefonInput').value.trim(),
        cocuk_yasi: $w('#yasInput').value || '',
        hizmet: $w('#hizmetInput').value || '',
        mesaj: $w('#mesajInput').value.trim()
    };
    $w('#kaydetButton').disable();

    try {
        const yanit = await fetch(`${API_URL}/api/leads`, {
            method: 'post',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(govde)
        });
        const veri = await yanit.json();
        $w('#durumText').text = veri.basari ? veri.mesaj : veri.hata;
        if (veri.basari) {
            $w('#isimInput').value = '';
            $w('#telefonInput').value = '';
        }
    } catch (hata) {
        $w('#durumText').text = 'Sunucuya ulaşılamadı. Lütfen tekrar deneyin.';
    } finally {
        $w('#kaydetButton').enable();
    }
}
