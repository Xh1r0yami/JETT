# JETT – Job Portal Web Application

Proyek ini adalah aplikasi job portal yang memungkinkan pengguna untuk mendaftar akun, login, melamar pekerjaan, dan bagi perusahaan untuk memposting lowongan.
Backend dibangun menggunakan **Django**, database menggunakan **MySQL (Docker)**, dan frontend menggunakan template bawaan Django.

## Instalasi Dependencies

Sebelum menjalankan project, install library Python berikut:

```bash
pip install pymysql
```

## Menjalankan MySQL dengan Docker

1. Pastikan Docker sudah ter-install.
2. Jalankan perintah berikut di folder project:


```bash
docker compose up -d
```

Cek status:

```bash
docker ps
```

---


## Cara Collaborator Menjalankan Project

Team yang melakukan `git clone` harus melakukan:

1. `pip install pymysql`
2. `docker compose up -d`
3. `python manage.py migrate`
4. `python manage.py runserver`


---


## Teknologi yang Digunakan

* Django 5+
* MySQL 8 (Docker)
* Python 3.10+

---
