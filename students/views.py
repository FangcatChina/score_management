# views.py
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Student, ScoreRecord, Group, User
from .forms import CustomUserCreationForm,ScoreForm, AddStudentForm, AddGroupForm, AssignStudentToGroupForm, BatchScoreForm, UpdateGroupSpecialScoreForm
def is_admin(user):
    return user.is_admin

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

@login_required
def dashboard(request):
    students = Student.objects.all()
    groups = Group.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        students = students.filter(name__icontains=search_query)
    return render(request, 'dashboard.html', {'students': students, 'groups': groups})

@login_required
def add_score(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = ScoreForm(request.POST)
        if form.is_valid():
            score = form.cleaned_data['score']
            reason = form.cleaned_data['reason']
            ScoreRecord.objects.create(
                student=student,
                user=request.user,
                score=score,
                reason=reason
            )
            student.total_score += score
            student.save()
            return redirect('dashboard')
    else:
        form = ScoreForm()
    return render(request, 'add_score.html', {'student': student, 'form': form})

@login_required
@user_passes_test(is_admin)
def add_student(request):
    if request.method == 'POST':
        form = AddStudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '学生添加成功！')
            return redirect('dashboard')
    else:
        form = AddStudentForm()
    return render(request, 'add_student.html', {'form': form})

@login_required
def view_score_records(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    records = ScoreRecord.objects.filter(student=student).order_by('-created_at')
    return render(request, 'score_records.html', {'student': student, 'records': records})

@login_required
@user_passes_test(is_admin)
def add_group(request):
    if request.method == 'POST':
        form = AddGroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '小组添加成功！')
            return redirect('dashboard')
    else:
        form = AddGroupForm()
    return render(request, 'add_group.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'账户 {username} 注册成功！可以登录了。')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def view_score_records(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    records = ScoreRecord.objects.filter(student=student).order_by('-created_at')
    return render(request, 'score_records.html', {'student': student, 'records': records})

@login_required
@user_passes_test(is_admin)
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    # 同时删除该学生的所有积分记录
    ScoreRecord.objects.filter(student=student).delete()
    student.delete()
    messages.success(request, f'学生 {student.name} 已成功删除。')
    return redirect('dashboard')
def public_ranking(request):
    # 按总分对学生进行降序排序
    students = Student.objects.all().order_by('-total_score')
    # 按总分对小组进行降序排序
    groups = Group.objects.all()
    ranked_groups = sorted(groups, key=lambda group: group.calculate_total_score(), reverse=True)
    return render(request, 'public_ranking.html', {'students': students, 'groups': ranked_groups})
@login_required
@user_passes_test(is_admin)
def update_group_special_score(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = UpdateGroupSpecialScoreForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, f'小组 {group.name} 的专项分已更新！')
            return redirect('dashboard')
    else:
        form = UpdateGroupSpecialScoreForm(instance=group)
    return render(request, 'update_group_special_score.html', {'form': form, 'group': group})

@login_required
@user_passes_test(is_admin)
def batch_assign_student_to_group(request):
    if request.method == 'POST':
        form = AssignStudentToGroupForm(request.POST)
        if form.is_valid():
            students = form.cleaned_data['students']
            group = form.cleaned_data['group']
            for student in students:
                student.group = group
                student.save()
            messages.success(request, f'学生已成功分配到小组 {group.name}！')
            return redirect('dashboard')
    else:
        form = AssignStudentToGroupForm()
    return render(request, 'batch_assign_student_to_group.html', {'form': form})

@login_required
def batch_add_score(request):
    if request.method == 'POST':
        form = BatchScoreForm(request.POST)
        if form.is_valid():
            students = form.cleaned_data['students']
            score = form.cleaned_data['score']
            reason = form.cleaned_data['reason']
            for student in students:
                ScoreRecord.objects.create(
                    student=student,
                    user=request.user,
                    score=score,
                    reason=reason
                )
                student.total_score += score
                student.save()
            messages.success(request, '学生积分已批量更新！')
            return redirect('dashboard')
    else:
        form = BatchScoreForm()
    return render(request, 'batch_add_score.html', {'form': form})
@user_passes_test(is_admin)
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    # 将该小组下的学生的 group 字段置为 None
    Student.objects.filter(group=group).update(group=None)
    group.delete()
    messages.success(request, f'小组 {group.name} 已成功删除。')
    return redirect('dashboard')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student

@csrf_exempt
def search_students(request):
    query = request.GET.get('query', '')
    students = Student.objects.filter(name__icontains=query)
    data = [{'id': student.id, 'name': student.name} for student in students]
    return JsonResponse(data, safe=False)

@login_required
@user_passes_test(is_admin)
def user_management(request):
    users = User.objects.all()
    return render(request, 'user_management.html', {'users': users})

@login_required
#@user_passes_test(is_admin)
def change_user_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if(user_id!=request.user.id):
        return redirect('dashboard')
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'用户 {user.username} 的密码已成功修改。')
            return redirect('user_management')
    else:
        form = PasswordChangeForm(user)
    return render(request, 'change_user_password.html', {'form': form, 'user': user})

@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, f'用户 {user.username} 已成功删除。')
        return redirect('user_management')
    return render(request, 'confirm_delete_user.html', {'user': user})