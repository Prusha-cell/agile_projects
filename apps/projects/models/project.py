from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    files = models.ManyToManyField('ProjectFile', related_name='projects')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

    @property
    def count_of_files(self):
        return self.files.count()


# В приложении project создайте новую модель ProjectFile:
# ● file_name Строковое поле, максимальная длина - 120 символов)
# ● file_path Поле загрузки файлов, таргет сохранения - папка ‘documentsʼ)
# ● created_at Дата создания файла, автозаполняется при создании нового файла)
# ● Отображение объектов по полу name (магический метод __str__)
# ● Сортировка записей по дате создания в порядке убывания
# 2. В модели Project создайте новое поле files, которое будет связывать проекты и файлы связью “Многие ко
# Многимˮ, связующее поле - “projectˮ.
# 3. В модели Project добавьте динамическое поле count_of_files через декоратор @property, которое будет
# высчитывать количество файлов для проекта.


class ProjectFile(models.Model):
    file_name = models.CharField(max_length=120)
    file_path = models.FileField(upload_to='documents/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.file_name



