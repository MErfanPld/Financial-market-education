from django.contrib.auth import get_user_model
from django.db.models import Count

User = get_user_model()

duplicates = User.objects.values('phone_number').annotate(count=Count('id')).filter(count__gt=1)

for dup in duplicates:
    phone = dup['phone_number']
    users = User.objects.filter(phone_number=phone).order_by('id')
    print(f"پاکسازی شماره تکراری: {phone}, تعداد رکوردها: {users.count()}")

    for u in users[1:]:
        print(f"حذف رکورد: {u.id} - {u.get_full_name()}")
        u.delete()

print("پاکسازی رکوردهای تکراری تمام شد.")
