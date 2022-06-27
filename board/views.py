from django.db.models import F
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.cache import cache_control

from member.models import Member
from board.models import Board

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def list(request):
    # Board와 Member테이블이 userid id 컬럼 기준으로 inner join 수행
    # bdlist.get(0).member.userid
    # bdlist = board.objects.values('id','title','userid','regdate','views').order_by('-id')
    # 쿼리셋 select 'id','title','userid','regdate','views' from borad order by id desc
    bdlist = Board.objects.select_related('member')

    context = {'bds':bdlist}
    return render(request, 'board/list.html', context)

def view(request):
    if request.method == 'GET':
        form = request.GET.dict()

        # 조회수 처리 장고 ORM사용
        # update board set views = views + 1 where id = 글번호..

        # b = Board.objects.get(id=form['bno'])
        # b.views = b.views + 1
        # b.save()
        Board.objects.filter(id=form['bno']).update(views=F('views') + 1)

        bd = Board.objects.select_related('member').get(id=form['bno'])

        # select * from board inner join member using(id) where id = bno..
    # print(form['bno'])
    elif request.method == 'POST':
        pass

    context = {'bd': bd}

    return render(request, 'board/view.html', context)


def write(request):
    returnPage = 'board/write.html'
    form = ''
    error = ''


    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        form = request.POST.dict()

        if not (form['title'] and form['contents']):
            error = '제목이나 본문 작성혀라'
        else:
            bd = Board(title=form['title'], contents=form['contents'], member=Member.objects.get(pk=form['memberid']))

            bd.save()

            return redirect('/list')

    context = {'form': form, 'error': error}

    return render(request, returnPage, context)

#/remove?bno= 를 받아서 삭제하면 됨
def remove(request):
    if request.method == 'GET':
        form = request.GET.dict()
        Board.objects.filter(id=form['bno']).delete()
        # delete from board where bno = 글번호..

    return redirect('/list')


def modify(request):
    if request.method == 'GET':
        form = request.GET.dict()
        bd = Board.objects.get(id=form['bno'])
        # select * from board where bno = 글번호..


    elif request.method == 'POST':
        form = request.POST.dict()
        Board.objects.filter(id=form['bno']).update(title=form['title'], contents=form['contents'])

        # update board set title = ???, contents = ?? where bno = 글번호
        # b = Board.objects.get(id=form['bno'])
        # b.title = form['title']
        # b.contents = form['contents']
        # b.save()


        return redirect('/view?bno=' + form['bno'])


    context = {'bd': bd}
    return render(request, 'board/modify.html', context)
