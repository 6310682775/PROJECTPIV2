# PRESENTATION

    https://www.canva.com/design/DAFeThtjG8c/AnsO1vqNt7F0DJOZPgFKLA/view?utm_content=DAFeThtjG8c&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

# FIGMA

    https://www.figma.com/file/t3o0QNkdDYcnV6YdEa2dCn/Genius-Traffic?node-id=0%3A1&t=ILtPIDOHGxczQxPy-1

# ClASS DIAGRAM

[classDiagram1](https://drive.google.com/file/d/1Sg4zGttQImzb1w7bDk8rh1rHCBDMk3ls/view?usp=sharing)
[classDiagram2](https://drive.google.com/file/d/1C0NK-yBUCDKMyh1pVtj6CSCLyBVNNJMe/view?usp=sharing)


# SETUP

## DOCKER
run redis  ผ่าน commandline 
```
docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest
```
## GIT REPO
1.  สร้าง folder ชื่อ App(หรืออะไรก็ได้)
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
6.  ลบmigrations/0001_initial.py เเละ 0002_alter_loop_orientation.py
7.  migrate 
```
python manage.py makemigrations
python manage.py migrate
```
8.  โหลดไฟล์.pt ใส่ในproject (ถ้ามีของเก่าให้ลบของเก่าออกก่อน)
https://drive.google.com/file/u/3/d/1kQXQBYLxLERxmlfCHzK52U5w_INUYKqV/view?usp=sharing

## RUN PROCESS
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

## SETUP for editloop
1.  pip install
```
pip install imageio\[ffmpeg\]
pip install "imageio[pyav]"
```
2.  mac brew install
```
brew install ffmpeg
```
3.  แก้import view.py
```
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
```

## เตรียมข้อมูล
1.  newtask
2.  ใส่ video
https://drive.google.com/file/d/1DVvWf2upGc639TE5jEZTMNSrJlJiD2ex/view
3.  เข้าedit loopของtaskนั้น เเล้วกด new loop
4.  ใส่ข้อมูล loop ตามนี้
```
{
    "loops":[
        {
            "name":"loop1",
            "id":"0",
            "points":[
                {"x":900,"y":600},
                {"x":900,"y":300},
                {"x":400,"y":300},
                {"x":400,"y":600}
            ],
            "orientation":"counterclockwise",
            "summary_location":{"x":20,"y":"20"}
        },
        {
            "name":"loop2",
            "id":"1",
            "points":[
                {"x":280,"y":450},
                {"x":280,"y":200},
                {"x":600,"y":200},
                {"x":600,"y":450}
                
            ],
            "orientation":"clockwise",
            "summary_location":{"x":20,"y":"380"}
        }
        ,
        {
            "name":"loop3",
            "id":"2",
            "points":[
                {"x":600,"y":80},
                {"x":850,"y":80},
                {"x":900,"y":600},
                {"x":600,"y":600}
                
            ],
            "orientation":"clockwise",
            "summary_location":{"x":950,"y":"20"}
        }
    ]
}
```
5.  สร้าง loop มา3 loop ตามข้อมูล
6.  Test กด send task หน้า celery terminal จะรันขึ้น
7.  ติดตามstatus ที่ django admin



