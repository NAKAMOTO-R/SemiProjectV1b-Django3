from django.shortcuts import render
from member.models import Member
from django.contrib.auth.hashers import make_password

# Create your views here.
#회원가입 처리함수
def join(request):
    returnPage = 'member/join.html'

    if request.method == 'GET':
        return render(request, returnPage)

    elif request.method == 'POST':
        form = request.POST.dict() #폼 데이터 다 들고 와서 dict형태로 저장
        # print(form, form['userid'])

        #유효성 검사

        error = ''
        if not (form['userid'] and form['pwd'] and form['pwd2'] and form['name'] and form['email']):
            error = '<li>입력값을 다시 확인해라</li>'
        elif form['pwd'] != form['pwd2']:
            error = '<li>비밀번호가 일치하지 않긔</li>'
        else:
            member = Member( #클래스 생성자. 빨간줄 alr Enter로
                userid=form['userid'], pwd=make_password(form['pwd']), name=form['name'], email=form['email'],
            )

            member.save()

            returnPage = 'member/joinok.html'


        context = {'form':form, 'error': error} #오류를 보내기 위해 dict 변수에 저장

        return render(request, returnPage, context)



def login(request):
    return render(request, 'member/login.html')


def myinfo(request):
    return render(request, 'member/myinfo.html')