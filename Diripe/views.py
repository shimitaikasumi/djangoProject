from datetime import datetime, date
from itertools import count

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from .models import Employee, Shiiregyosya, Patient, Medicine, Treatment


def login(request):
    if request.method == "POST":
        empid = request.POST.get('empid')
        emppasswd = request.POST.get('emppasswd')

        if not empid or not emppasswd:
            messages.error(request, "IDまたはパスワードを入力してください")
            return render(request, 'login.html')

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
        emppass = request.POST.get('emppass')
        empwd = request.POST.get('empwd')
        emprole = request.POST.get('emprole')

        # チェックリスト
        required_fields = [empid, empfname, emplname, emppass, empwd, emprole]
        if not all(required_fields):
            messages.error(request, 'すべての項目を入力してください。')
        elif emppass != empwd:
            messages.error(request, 'パスワードが一致しません。')
        elif Employee.objects.filter(empid=empid).exists():
            messages.error(request, 'このIDはすでに登録してあります。')
        else:
            employee = Employee(
                empid=empid, empfname=empfname,
                emplname=emplname, emppasswd=emppass,
                emprole=emprole
            )
            employee.save()
            messages.success(request, '従業員が登録されました。')
            return render(request, 'admin/toroku.html')

    return render(request, 'admin/empregistration.html')

def vendor_toroku(request):
    if request.method == "POST":
        shiireid = request.POST.get('shiireid')
        shiiremei = request.POST.get('shiiremei')
        shiireaddress = request.POST.get('shiireaddress')
        shiiretel = request.POST.get('shiiretel')
        shihonkin = request.POST.get('shihonkin')
        nouki = request.POST.get('nouki')

        # チェックリスト
        required_fields = [shiireid, shiiremei, shiireaddress, shiiretel, shihonkin, nouki]
        if not all(required_fields):
            messages.error(request, 'すべての項目を入力してください。')
        elif Shiiregyosya.objects.filter(
            shiireid=shiireid, shiiremei=shiiremei,
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
            messages.success(request, '仕入先が登録されました。')
            return render(request, 'shiire_success.html', {'shiiregyosya': shiiregyosya})

    return render(request, 'admin/record_pras.html')

def vendor_search(request):
    if request.method == 'GET':
        shiiregyosyas = Shiiregyosya.objects.all()
        return render(request, 'admin/vendor.html', {'shiiregyosyas': shiiregyosyas})
    elif request.method == 'POST':
        address = request.POST.get('shiireaddress')
        if address:
            shiiregyosyas = Shiiregyosya.objects.filter(shiireaddress=address)
        else:
            shiiregyosyas = Shiiregyosya.objects.none()

        return render(request, 'admin/vendor.html', {'shiiregyosyas': shiiregyosyas})


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


def confirmation(request):
    employee = Employee.objects.get(empid=request.POST.get('empid'))

    if request.method == 'GET':
        employee = Employee.objects.filter(empid=request.POST.get('empid'))
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
        return render(request,'toroku.success.html', {'employee': employee})  # 成功時のリダイレクト先を指定

    return render(request, 'admin/confirmation.html', {'employee': employee})


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


def confirmation_re(request):
    employee = Employee.objects.get(empid=request.POST.get('empid'))

    if request.method == 'GET':
        employee = Employee.objects.filter(empid=request.POST.get('empid'))
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
        return render(request,'henkou.html', {'employee': employee})  # 成功時のリダイレクト先を指定

    return render(request, 'reception/confirmation_re.html', {'employee': employee})


def string_to_date(date_string: str) -> date:
    try:
        # 日付文字列をdatetime部ジェクトに
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        # datetimeオブジェクトをdateオブジェクトに変換
        return date_obj.date()
    except ValueError:
        # 日付文字列のフォーマットが不正な場合
        raise ValueError("Incorrect date format, should be YYYY-MM-DD")


def patient_registration(request):
    if request.method == 'GET':
        patient = Patient.objects.all()
        return render(request, 'reception/patient.registration.html', {'patient': patient})

    if request.method == 'POST':
        patid = request.POST.get('patid')
        patfname = request.POST.get('patfname')
        patlname = request.POST.get('patlname')
        hokenmei = request.POST.get('hokenmei')
        hokenexp = request.POST.get('hokenexp')

        # チェックリスト
        required_fields = [patid, patfname, patlname, hokenmei, hokenexp]
        if not all(required_fields):
            messages.error(request, 'すべての項目を入力してください。')
            return render(request, 'reception/patient.registration.html')

        # 日付文字列をdateオブジェクトに変換
        try:
            hokenexp = string_to_date(hokenexp)
        except ValueError as e:
            messages.error(request, str(e))
            return render(request, 'reception/patient.registration.html')

        # 現在のUTC日付を取得
        today = timezone.now().date()

        if Patient.objects.filter(patid=patid).exists():
            messages.error(request, 'このIDはすでに登録してあります。')
        elif hokenexp >= today:
            patient = Patient(
                patid=patid, patfname=patfname,
                patlname=patlname, hokenmei=hokenmei,
                hokenexp=hokenexp
            )
            patient.save()
            messages.success(request, '患者が登録されました。')
            return render(request, 'toroku.success.html')
        else:
            messages.error(request, '有効期限が過ぎています。')

    return render(request, 'reception/patient.registration.html')


def patient_listr(request):
    if request.method == 'GET':
        patients = Patient.objects.all()
        return render(request, 'reception/patient.management.html', {'patients': patients})


def confirmation_pat(request):
    patient = Patient.objects.get(patid=request.POST.get('patid'))

    if request.method == 'GET':
        patient = Patient.objects.filter(patid=request.POST.get('patid'))
        return render(request, 'reception/confirmation_pat.html', {'patient': patient})

    if request.method == 'POST':
        new_hokenmei = request.POST.get('newhokenmei')
        new_hokenexp = request.POST.get('newhokenexp')

        # 入力が空かどうかをチェック
        if not new_hokenmei or not new_hokenexp:
            messages.error(request, '変更する保険証情報を入力してください。')
            return render(request, 'reception/confirmation_pat.html', {'patient': patient})

        # フォームが有効な場合、データベースを更新
        patient.hokenmei = new_hokenmei
        patient.hokenexp = new_hokenexp
        patient.save()

        messages.success(request, '患者の保険証情報が更新されました。')
        return render(request, 'toroku.success.html', {'patient': patient})  # 成功時のリダイレクト先を指定

    return render(request, 'reception/confirmation_pat.html', {'patient': patient})


def patient_expired(request):
    # 現在のUTC日付を取得
    today = timezone.now().date()
    # 有効期限を過ぎた患者をフィルタリング
    patients = Patient.objects.filter(hokenexp__lt=today)
    # 結果をテンプレートに渡して表示
    return render(request, 'reception/patient.search.html', {'patients': patients})


def patient_search(request):
    if 'cartlist' in request.session:
        del request.session['cartlist']
    if request.method == 'GET':
        patients = Patient.objects.all()
        return render(request, 'doctor/patient.search.html', {'patients': patients})
    elif request.method == 'POST':
        lname = request.POST.get('patlname')
        if lname:
            patients = Patient.objects.filter(patlname=lname)
        else:
            patients = Patient.objects.none()

        return render(request, 'doctor/patient.search.html', {'patients': patients})


def drug_selection(request):
    medicines = Medicine.objects.all()
    treatments = Treatment.objects.all()
    patient = Patient.objects.get(patid=request.POST['patid'])
    return render(request, 'doctor/drug.administration.html', {
        'patient': patient,
        'medicines': medicines,
        'treatments': treatments,
    })


def add_drug(request):
    medicines = Medicine.objects.all()
    patient = Patient.objects.get(patid=request.POST['patid'])
    if 'cartlist' in request.session:
        cart = request.session['cartlist']
    else:
        cart = []

    if request.method == 'POST':
        patid = request.POST.get('patid')

        for medicine in range(medicines.count()):
            cart_drug = {
                'empid': request.session['empid'],
                'patid': patid,
                'quantity': request.POST.get(f'quantity{medicine + 1}'),
                'medicinename': medicines[medicine].medicinename,
                'date': timezone.now().isoformat(),
            }
            cart.append(cart_drug)

        request.session['cartlist'] = cart
    return render(request, 'doctor/cart_drug.html', {'patient': patient, 'medicines': medicines, 'cart': cart})


def deletion_drug(request):
    medicines = Medicine.objects.all()
    patient = Patient.objects.get(patid=request.POST['patid'])
    cart = request.session['cartlist']

    if request.method == 'POST':
        index = request.POST.get('index')
        cart.pop(int(index)-1)

        request.session['cartlist'] = cart
    return render(request, 'doctor/cart_drug.html', {'patient': patient, 'medicines': medicines, 'cart': cart})


def treatment_confirmed(request):
    if 'cartlist' in request.session:
        cart = request.session['cartlist']
        medicines = Medicine.objects.all()

        for aa in cart:
            # 患者インスタンスを取得する
            patid = aa['patid']
            patient = Patient.objects.get(patid=patid)

            # 従業員インスタンスを取得する
            empid = aa['empid']
            employee = Employee.objects.get(empid=empid)

            date_obj = datetime.fromisoformat(aa['date'])

            # Treatmentインスタンスを作成して保存する
            treatment = Treatment(
                empid=employee,
                patid=patient,
                quantity=aa['quantity'],
                medicinename=aa['medicinename'],
                date=date_obj,
            )
            treatment.save()
            messages.success(request, '患者への薬剤処置が確定されました。')

        # cartlistが存在する場合にのみ削除
        del request.session['cartlist']
    else:
        messages.error(request, 'カート情報が見つかりませんでした。')

    # 処置が成功または失敗した場合のリダイレクト先
    return render(request, 'drug_success.html')


def patient_search2(request):
    return render(request, 'doctor/patient.search2.html', {'treatment': Treatment.objects.all()})


def patient_pasthistory(request, patid):
    patient = get_object_or_404(Patient, patid=patid)

    treatments = Treatment.objects.filter(patient=patient).select_related('medicine')
    if not treatments:
        messages.error(request, 'この患者は処置されていません')
    return render(request, 'doctor/patient_pasthistory.html', {'patient': patient, 'treatments': treatments})


def error_page(request):
    return render(request, 'error_page.html')


def shiire_success(request):
    return render(request, 'shiire_success.html')


def employee_success(request):
    return render(request, 'employee_success.html')


def main(request):
    return render(request, 'main.html')
