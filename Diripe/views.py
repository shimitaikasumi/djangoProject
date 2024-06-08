from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Employee, Shiiregyosya


def login(request):
    if request.method == "POST":
        empid = request.POST.get('empid')
        emppasswd = request.POST.get('emppasswd')
        try:
            employee = Employee.objects.get(empid=empid)
        except Employee.DoesNotExist:
            messages.error(request, "利用者IDが違います")
            return render(request, 'login.html')

        if employee.emppasswd == emppasswd:
            request.session['empid'] = employee.empid
            if employee.emprole == 1:
                return render(request, 'admin/home.html')
            elif employee.emprole == 2:
                return render(request, 'reception/home.html')
            elif employee.emprole == 3:
                return render(request, 'doctor/home.html')
        else:
            messages.error(request, "パスワードが違います")
            return render(request, 'login.html')
    return render(request, 'login.html')


def empregistration(request):
    if request.method == 'GET':
        employee = Employee.objects.all()
        return render(request, 'admin/empregistration.html', {'employee': employee})

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
                emplname=emplname, emppasswd=emppasswd,
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

        if Shiiregyosya.objects.filter(shiireid=shiireid, shiiremei=shiiremei,
                                       shiireaddress=shiireaddress, shiiretel=shiiretel,
                                       shihonkin=shihonkin, nouki=nouki
                                       ).exists():
            messages.error(request, 'この仕入先はすでに登録してあります。')
        else:
            shiiregyosya = Shiiregyosya(
                shiireid=shiireid, shiiremei=shiiremei,
                shiireaddress=shiireaddress, shiiretel=shiiretel,
                shihonkin=shihonkin, nouki=nouki
            )
            shiiregyosya.save()
            return redirect('shiire_success')

    return render(request, 'admin/vendor.html')


def vendor_search(request):
    if request.method == 'GET':
        shiiregyosya = Shiiregyosya.objects.all()
        return render(request, 'admin/vendor.html', {'shiiregyosya': shiiregyosya})

    address = request.GET.get('address', '')
    vendors = []

    if address:
        vendors = Shiiregyosya.objects.filter(shiireaddress__icontains=address)

    return render(request, 'admin/vendor.html', {'address': address, 'vendors': vendors})


def vendor_list(request):
    if request.method == 'GET':
        shiiregyosyas = Shiiregyosya.objects.all()
        return render(request, 'admin/vendor.html', {'shiiregyosyas': shiiregyosyas})


def shiire_success(request):
    return render(request, 'shiire_success.html')
def employee_success(request):
    return render(request, 'employee_success.html')


def main(request):
    return render(request, 'main.html')
