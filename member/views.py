from django.shortcuts import render, redirect
from member.models import Member
from django.contrib.auth.hashers import make_password, check_password


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
        if not (form['userid'] and form['passwd'] and form['pwd2'] and form['name'] and form['email']):
            error = '<li>입력값을 다시 확인해라</li>'
        elif form['passwd'] != form['pwd2']:
            error = '<li>비밀번호가 일치하지 않긔</li>'
        else:
            member = Member( #클래스 생성자. 빨간줄 alr Enter로
                userid=form['userid'], passwd=make_password(form['passwd']), name=form['name'], email=form['email'],
            )

            member.save()

            returnPage = 'member/joinok.html'


        context = {'form':form, 'error': error} #오류를 보내기 위해 dict 변수에 저장

        return render(request, returnPage, context)



def login(request):
    returnPage = 'member/login.html'

    if request.method == "GET":
        return render(request, returnPage)

    elif request.method == "POST":
        form = request.POST.dict()

        error = ''
        if not (form['userid'] and form['passwd']):
            error = '아이디나 비밀번호를 확인해주세요'
        else:
            # 입력한 아이디로 회원정보가 테이블에 있는지 확인
            try:
                member = Member.objects.get(userid=form['userid'])
            except Member.DoesNotExist:
                member = None

            if member and check_password(form['passwd'], member.passwd):
                # 세션변수에 인증정보 저장해둠
                request.session['userid'] = form['userid']

                return redirect('/') #index로 이동
            else:
                error = '아이디나 비밀번호가 틀립니다'

        context = {'error': error}
        return render(request, returnPage, context)

def logout(request):
    if request.session.get('userid'):
        del(request.session['userid'])

    return redirect('/')



def myinfo(request):

    member = {}
    if request.session.get('userid'):
        userid = request.session.get('userid')

        member = Member.objects.get(userid=userid)

    context = {'member': member}

    return render(request, 'member/myinfo.html', context)

    # 마이인포 뜨게 만들어줌

