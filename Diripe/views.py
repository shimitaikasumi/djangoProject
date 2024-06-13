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
            shiiregyosya = Shiiregyosya.objects.create(
                shiireid=shiireid, shiiremei=shiiremei,
                shiireaddress=shiireaddress, shiiretel=shiiretel,
                shihonkin=shihonkin, nouki=nouki
            )
            return render(request, 'shiire_success.html', {'shiiregyosya': shiiregyosya})

    return render(request, 'admin/vendor.html')


def vendor_search(request):
    if request.method == 'GET':
        shiiregyosya = Shiiregyosya.objects.all()
        return render(request, 'admin/vendor.html', {'shiiregyosya': shiiregyosya})
    elif request.method == 'POST':
        address = request.POST.get('shiireaddress')
        if address:
            shiiregyosya = Shiiregyosya.objects.filter(shiireaddress__icontains=address)
        else:
            shiiregyosya = Shiiregyosya.objects.none()

        return render(request, 'admin/vendor.html', {'shiiregyosya': shiiregyosya})


def vendor_list(request):
    if request.method == 'GET':
        shiiregyosyas = Shiiregyosya.objects.all()
        return render(request, 'admin/vendor.html', {'shiiregyosyas': shiiregyosyas})


def nachange_search(request):
    if request.method == 'GET':
        employees = Employee.objects.all()
        return render(request, 'admin/nachange.html', {'employees': employees})
    elif request.method == 'POST':
        id = request.POST.get('empid')
        if id:
            employees = Employee.objects.filter(empid=id)
        else:
            employees = Employee.objects.none()

        return render(request, 'admin/nachange.html', {'employees': employees})


def nachange_list(request):
    if request.method == 'GET':
        employees = Employee.objects.all()
        return render(request, 'admin/nachange.html', {'employees': employees})


def confirmation(request, empid):
    employee = Employee.objects.get(empid=empid)

    if request.method == 'GET':
        employee = Employee.objects.filter(empid=empid)
        return render(request, 'admin/confirmation.html', {'employee': employee})

    if request.method == 'POST':
        new_emplname = request.POST.get('newemplname')
        new_empfname = request.POST.get('newempfname')

        # 入力が空かどうかをチェック
        if not new_emplname or not new_empfname:
            messages.error(request, '姓と名を入力してください。')
            return render(request, 'admin/confirmation.html', {'employee': employee})

        # フォームが有効な場合、データベースを更新
        employee.emplname = new_emplname
        employee.empfname = new_empfname
        employee.save()

        messages.success(request, '従業員情報が更新されました。')
        return redirect('admin/nachange.html', {'employee': employee})# 成功時のリダイレクト先を指定

    return render(request, 'admin/confirmation.html')

def employeeinfchg_search(request):
    if request.method == 'GET':
        employees = Employee.objects.all()
        return render(request, 'reception/employeeinfchg.html', {'employees': employees})
    elif request.method == 'POST':
        id = request.POST.get('empid')
        if id:
            employees = Employee.objects.filter(empid=id)
        else:
            employees = Employee.objects.none()

        return render(request, 'reception/employeeinfchg.html', {'employees': employees})


def employeeinfchg_list(request):
    if request.method == 'GET':
        employees = Employee.objects.all()
        return render(request, 'reception/employeeinfchg.html', {'employees': employees})


def confirmation_re(request, empid):
    employee = Employee.objects.get(empid=empid)

    if request.method == 'GET':
        employee = Employee.objects.filter(empid=empid)
        return render(request, 'reception/confirmation_re.html', {'employee': employee})

    if request.method == 'POST':
        new_emppass_r = request.POST.get('newemppass_r')
        new_emppass_e = request.POST.get('newemppass_e')

        # 入力が空かどうかをチェック
        if not new_emppass_r or not new_emppass_e:
            messages.error(request, '変更するパスワードを入力してください。')
            return render(request, 'reception/confirmation_re.html', {'employee': employee})

        if not new_emppass_r == new_emppass_e:
            messages.error(request, '入力したパスワードが一致しません。')
            return render(request, 'reception/confirmation_re.html', {'employee': employee})

        # フォームが有効な場合、データベースを更新
        employee.emppasswd = new_emppass_r
        employee.save()

        messages.success(request, '従業員情報が更新されました。')
        return redirect('reception/employeeinfchg.html', {'employee': employee})# 成功時のリダイレクト先を指定

    return render(request, 'reception/confirmation_re.html')




def shiire_success(request):
    return render(request, 'shiire_success.html')


def employee_success(request):
    return render(request, 'employee_success.html')


def main(request):
    return render(request, 'main.html')
