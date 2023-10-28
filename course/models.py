from django.db import models

from users.models import User


class Course(models.Model):
    title = models.CharField(max_length=20, verbose_name='Название')
    preview = models.ImageField(upload_to='course/', verbose_name='Превью(картинка)', null=True)
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.title}'


class Lesson(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='lesson/', verbose_name='Превью(картинка)', null=True)
    url = models.URLField(verbose_name='Ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")

    def __str__(self):
        return f'{self.title}'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name="оплаченный курс")
    lesson = models.ForeignKey('course.Lesson', on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name="оплаченный урок")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20,
                                      choices=[('cash', 'Наличные'), ('transfer', 'Перевод на счет')])

    def __str__(self):
        return f"{self.user.username} - {self.date}"


