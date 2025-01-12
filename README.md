# BCI Task
## وصف المشروع
ده مشروع معمول باستخدام **Django** وبيعمل عملية التسجيل للمستخدم وتسجيل الدخول.
في البداية يتم استخدام core/lib لتخزين serializers , models, views خاص بنا لتسهيل العمل لدينا 

---

## متطلبات التشغيل

- Python 3.10+ (أو أي إصدار شغال معاك)
- Virtual Environment (اختياري)
- مكتبات Python المطلوبة موجودة في ملف `requirements.txt`
- قاعدة بيانات (SQLite )

---

## خطوات تشغيل المشروع

### 1. نسخ المشروع
قم بعمل Clone للريبو باستخدام:

```
bash
git clone https://github.com/Omarsanosy24/BCI.git
cd BCI
```
2. إنشاء بيئة افتراضية (اختياري لكن مستحسن)
قم بإنشاء وتفعيل بيئة افتراضية:
```
# على أنظمة Linux/MacOS
python3 -m venv env
source env/bin/activate

# على Windows
python -m venv env
env\Scripts\activate
```
3. تثبيت المتطلبات
قم بتثبيت المكتبات المطلوبة من ملف requirements.txt:
```
pip install -r requirements.txt
```
5. تشغيل السيرفر المحلي
لتشغيل المشروع على السيرفر المحلي:
```
./start
```
ثم افتح المتصفح على العنوان التالي:

```
http://127.0.0.1:8000/
```
## إضافات مهمة
اختبار الكود
شغلها باستخدام:
```
pytest
```
بيانات مسؤول الموقع (Admin)
لو بتستخدم Django Admin، أنشئ مستخدم مسؤول:
```
python manage.py createsuperuser
```
للوصول الى لعمل register 
```
/auth/register/
```
لعمل login 
```
/auth/login/
```
