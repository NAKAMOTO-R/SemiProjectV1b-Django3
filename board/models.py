from datetime import datetime
from django.db import models
from member.models import Member
# Create your models here.

#on_delete : CASCADE, DO_NOTHING
class Board(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    member=models.ForeignKey(Member, related_name='board', on_delete=models.DO_NOTHING) # on_delete=models.CASCADE 회원정보 지우면 게시물 삭제
    regdate=models.DateTimeField(default=datetime.now)
    views=models.IntegerField(default=0)
    contents=models.TextField(null=False, blank=False) #false는 not null이라는 뜻

    class Meta:
        db_table = 'board'
        ordering = ['-regdate']

    def __srt__(self):
        return self.title