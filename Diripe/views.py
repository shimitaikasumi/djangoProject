from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Employee


def login(request):
    if request.method == "POST":
        empid = request.POST('empid')
        emppasswd = request.POST('emppasswd')
        try:
            employee = Employee.objects.get(empid=empid)
        except Employee.DoesNotExist:
            messages.error(request,"利用者IDが違います")
            return render(request,'login.html')

        if employee.emppassed == emppasswd:
            request.session['empid'] = employee.empid
            if employee.emprole == 1:
                return render(request,'admin/home.html')
            elif employee.emprole == 2:
                return render(request,'reception/home.html')
            elif employee.emprole == 3:
                return render(request,'reception/home.html')
        else:
            messages.error(request, "パスワードが違います")
            return render(request, 'login.html')
    return render(request, 'login.html')

def empregistration(request):
    if request.method == 'POST':
        empid = request.POST.get('empid')
        empfname = request.POST.get('empfname')
        emplname = request.POST.get('emplname')
        emppasswd = request.POST.get('emppasswd')
        emprole = request.POST.get('emprole')

        if Employee.objects.filter(empid=empid).exists():
            messages.error(request, 'このIDはすでに登録してあります。')
        else:
            employee = Employee(
                empid=empid, empfname=empfname,
                emplname=emplname,emppasswd=emppasswd,
                emprole=emprole
            )
            employee.save()
            messages.success(request, '従業員が登録されました。')
            return redirect('admin_empregistration.html')

    return render(request, 'admin/empregistration.html')

def vendor(request):
    if request.method == "POST":



def employee_success(request):
    return render(request, 'success.html')





