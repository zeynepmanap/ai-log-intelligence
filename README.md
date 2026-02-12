# AI Log Explainer 🧠

AI Log Explainer, sistem loglarını analiz eden ve olası kritik hataları, uyarıları ve bilgi mesajlarını sınıflandıran bir Python/Flask uygulamasıdır.  
AI destekli analiz sayesinde hataların olası root cause’larını tahmin eder, risk seviyesini belirler ve öneriler sunar.

---

## Özellikler
- Logları dört seviyede sınıflandırır: **CRITICAL, ERROR, WARNING, INFO**
- AI destekli root cause analizi ve risk değerlendirmesi
- AI Confidence Score ile tahmin güvenilirliğini gösterir
- Web tabanlı dashboard ile logları ve AI önerilerini görselleştirir
- İsteğe bağlı retry logic ile başarısız API çağrılarını tekrar dener
- Sistem risk değerlendirmesi ve güvenlik tehditlerini raporlar

---

## Kurulum ve Çalıştırma

### 1️⃣ Projeyi klonla
Terminal veya CMD aç ve şu komutu çalıştır:
```bash
git clone <REPO_LINKI>
cd ai-log-explainer

2️⃣ Gereksinimleri yükle
pip install -r requirements.txt
Not: Python 3.9 veya üstü önerilir.

3️⃣ Uygulamayı başlat
python app.py

4️⃣ Web dashboard’a eriş
Tarayıcıda aç: http://127.0.0.1:5000/
Buradan logları, AI summary, root cause ve risk önerilerini görebilirsin.

5️⃣ Örnek Çıktı
ERROR
CRITICAL
WARNING
INFO

AI Summary: Payment processing failure due to connection timeouts
AI Root Cause: Connection timeout errors while connecting to https://payment-api.com
AI Risk Level: High
AI Confidence Score: 65%
Recommendations:
- Verify payment gateway connectivity
- Implement retry logic for failed requests

6️⃣ Geliştirme Notları
logs.py dosyasındaki örnek loglar değiştirilebilir.
Dashboard tasarımı templates/dashboard.html üzerinden özelleştirilebilir.
Kritik loglar için e-posta veya Slack bildirim entegrasyonu eklenebilir.
AI modelini ileride gerçek log verileriyle besleyip doğruluk artırabilirsiniz.

7️⃣ Lisans
Bu proje MIT lisansı ile korunmaktadır. Daha fazla bilgi için LICENSE dosyasına bakabilirsiniz.


