# PRESENTATION

    https://www.canva.com/design/DAFeThtjG8c/AnsO1vqNt7F0DJOZPgFKLA/view?utm_content=DAFeThtjG8c&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

# FIGMA

    https://www.figma.com/file/t3o0QNkdDYcnV6YdEa2dCn/Genius-Traffic?node-id=0%3A1&t=ILtPIDOHGxczQxPy-1

# ClASS DIAGRAM

https://drive.google.com/file/d/1Uq4LzrP7XZmpJR2l_A1Mtasie4Oipar_/view?usp=share_link
https://drive.google.com/file/d/1Uq4LzrP7XZmpJR2l_A1Mtasie4Oipar_/view?usp=share_link


# SETUP

## DOCKER
run redis  ผ่าน commandline 
```
docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest
```
## GIT REPO
1.  สร้าง folder ชื่อ App(หรืออะไรก็ได้
2.  เปิด VS code ด้วย folder นั้น
3.  clone 
```
git clone https://github.com/6310682775/PROJECTPIV2
```
4.  สร้าง env และ install package
MAC
```
python3 -m venv env
. env/bin/activate
pip install -r requirements.txt
(ย้ายfile requirementออกมาจากmysite) 
```
5.  เข้า PROJECTPIV2 directory
```
cd PROJECTPIV2
```
6.  ลบmigrations/001_initial.py
7.  migrate 
```
python manage.py makemigrations
python manage.py migrate
```
8.  โหลดไฟล์.pt ใส่ในproject (ถ้ามีของเก่าให้ลบของเก่าออกก่อน)
https://drive.google.com/file/u/3/d/1kQXQBYLxLERxmlfCHzK52U5w_INUYKqV/view?usp=sharing

# RUN PROCESS
1.  Django
```
python manage.py runserver
```
ACCESS
```
http://localhost:8000
```
3.  Celery
```
celery -A mysite.celery worker --pool=solo -l info
```
