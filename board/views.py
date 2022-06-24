from django.shortcuts import render, redirect

# Create your views here.
from board.models import board
from member.models import Member


def list(request):
    bdlist = board.objects.values('id','title','userid','regdate','views').order_by('-id')

    context = {'bds':bdlist}
    return render(request, 'board/list.html', context)

def view(request):
    return render(request, 'board/view.html')


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
            bd = board(title=form['title'], contents=form['contents'], userid=Member.objects.get(pk=form['userid']))

            bd.save()

            return redirect('/list')

    context = {'form': form, 'error': error}

    return render(request, returnPage, context)
