# Devlet Kurumu Corpus Platformu

Güvenli, büyük ölçekli Django tabanlı corpus derleme web sitesi.

## Özellikler

- ✅ **Güvenlik**: Modern güvenlik başlıkları, veri şifreleme, Argon2 password hashing
- ✅ **Kullanıcı Yönetimi**: Rol tabanlı erişim kontrolü (RBAC), 2FA desteği
- ✅ **Corpus Yönetimi**: Doküman yükleme, kategorizasyon, derleme koleksiyonları
- ✅ **Audit Logging**: Tüm kullanıcı işlemlerinin detaylı kaydı (KVKK uyumlu)
- ✅ **API**: RESTful API with JWT authentication

## Teknoloji Stack

- **Framework**: Django 4.2.11 LTS
- **Veritabanı**: MySQL
- **Security**: django-axes, django-ratelimit, cryptography
- **API**: Django REST Framework + SimpleJWT
- **Password Hashing**: Argon2

## Kurulum

### 1. Gereksinimler

```bash
pip install -r requirements.txt
```

### 2. Veritabanı Kurulumu

MySQL'de veritabanı oluşturun:

```sql
CREATE DATABASE corpus_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Environment Ayarları

`.env.example` dosyasını `.env` olarak kopyalayın ve düzenleyin:

```bash
cp .env.example .env
```

`.env` dosyasında MySQL şifrenizi ayarlayın.

### 4. Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Süper Kullanıcı Oluştur

```bash
python manage.py createsuperuser
```

### 6. Sunucuyu Başlat

```bash
python manage.py runserver
```

Admin paneline `http://localhost:8000/admin` adresinden erişebilirsiniz.

## Güvenlik Özellikleri

### Password Policy
- Minimum 12 karakter
- Argon2 hashing
- Kullanıcı bilgilerine benzememe kontrolü

### Session Security
- HTTP-only cookies
- SameSite=Strict
- 1 saatlik timeout

### Brute Force Protection
- 5 başarısız denemeden sonra hesap kilidi
- 1 saat lockout süresi

### Audit Logging
- Tüm kullanıcı işlemleri loglanır
- IP adresi ve user agent kaydı
- KVKK/GDPR uyumlu

### File Security
- Dosya tipi validasyonu
- Şifreleme desteği
- SHA256 hash verification

## Kullanıcı Rolleri

1. **Admin**: Tam yetki, kullanıcı onaylama
2. **Editor**: Corpus düzenleme yetkisi
3. **Researcher**: Arama ve analiz
4. **Viewer**: Sadece görüntüleme

## Proje Yapısı

```
openCorpus/
├── gov_compilation/      # Ana proje ayarları
├── accounts/             # Kullanıcı yönetimi
├── corpus/               # Corpus doküman yönetimi
├── security/             # Güvenlik utilities
├── static/               # Static dosyalar
├── media/                # Yüklenen dosyalar
├── templates/            # HTML templates
└── logs/                 # Log dosyaları
```

## Lisans

MIT License