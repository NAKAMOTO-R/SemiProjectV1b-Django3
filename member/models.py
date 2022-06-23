from datetime import datetime

from django.db import models

# Create your models here.
# member 테이블 구조와 유사하게 member 모델 정의
class Member(models.Model):
    id=models.AutoField(primary_key=True)
    userid=models.CharField(max_length=18, unique=True)
    pwd=models.CharField(max_length=18) #유니크 아님
    name=models.CharField(max_length=5)
    email=models.CharField(max_length=100)
    regdate=models.DateTimeField(default=datetime.now)

    #DB테이블 이름 지정
    class Meta:
        db_table = 'member'
        ordering = ['-regdate'] #- DESC +ASC

    def __str__(self):
        return self.userid  #객체출력시 출력형태 정의
