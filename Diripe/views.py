from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import json
from .models import Employee, Shiiregyosya


def login(request):
    Employee.objects.all()
    for i in Employee.objects.all():
        print(i.empid)

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
            return redirect('admin/empregistration.html')

    return render(request, 'admin/empregistration.html')

def vendor_toroku(request):
    if request.method == "POST":
        shiireid = request.POST.get('shiireid')
        shiiremei = request.POST.get('shiiremei')
        shiireaddress = request.POST.get('shiireaddress')
        shiiretel = request.POST.get('shiiretel')
        shihonkin = request.POST.get('shihonkin')
        nouki = request.POST.get('nouki')

        if Shiiregyosya.objects.filter(shiireid=shiireid).exists():
            messages.error(request, 'このIDを持つ仕入先はすでに登録してあります。')
        else:
            shiiregyosya = Shiiregyosya(
            shiireid=shiireid, shiiremei=shiiremei,
            shiireaddress=shiireaddress, shiiretel=shiiretel,
            shihonkin=shihonkin, nouki=nouki
            )
            shiiregyosya.save()
            messages.success(request, '仕入先が登録されました。')
            return redirect('admin/vendor.html')

    return render(request, 'admin/vendor.html')

def vendor_list(request):
    shiiregyosya = Shiiregyosya.objects.all()
    for i in shiiregyosya:
        print(i.shiireaddress)

    shiiregyosyas_json = json.dumps(
        list(shiiregyosya.values('shiireid', 'shiiremei', 'shiireaddress', 'shiiretel', 'shihonkin', 'nouki')))
    return render(request, 'admin/vendor.html')

def employee_success(request):
    return render(request, 'success.html')

def main(request):
    return render(request, 'main.html')







