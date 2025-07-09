from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from apps.tasks.choices.statuses import Statuses
from apps.tasks.choices.priority import Priority
from apps.projects.models.project import Project
from apps.tasks.utils.set_end_of_month import calculate_end_of_month


class Tag(models.Model):
    name = models.CharField(max_length=20, validators=[MinLengthValidator(4)])

    def __str__(self):
        return self.name


# В приложении tasks создайте новую модель Task:
# ● name (строковое поле, максимальное значение - 120 символов)
# ● description (большое строковое поле, обязательно к заполнению)
# ● status (строковое поле, максимальное значение - 15 символов, выбор из готовых полей через Enum класс Statuses,
# значение по умолчанию - NEW)
# ● priority Цифровое маленькое поле, возможность выбора из готовых значений через Enum класс Priority, значение
# по умолчанию - MEDIUM)
# ● project (связующее ForeignKey поле к модели Project. При удалении проекта все задачи должны удаляться, поле
# для проектов - ‘tasksʼ)
# ● tags (связующее ManyToMany поле к модели Tag, поле для тегов - ‘tasksʼ)
# ● created_at (поле даты и времени. Автоматическое заполнение при создании записи)
# ● updated_at (поле даты и времени. Автоматическое заполнение при создании и обновлении записи)
# ● deleted_at (поле даты и времени, может быть пустым)
# ● deadline (поле даты и времени, обязательно к заполнению. По умолчанию должен быть расчёт последнего дня
# текущего месяца при создании записи)
# ● assignee (связующее ForeignKey поле к модели User от django. Защита от удаления, поле для пользователя -
# ‘tasksʼ, у задачи может не быть назначенного пользователя)
# 2. Добавьте строковое отображение задач в формате: “название задачи, статусˮ.
# 3. Добавьте сортировку по дедлайн дате в порядке убывания.
# 4. Добавьте уникальность по полям name и project.


class Task(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(null=False, blank=False)
    status = models.CharField(
        max_length=15,
        choices=Statuses.choices(),
        default=Statuses.NEW.value
    )
    priority = models.SmallIntegerField(
        choices=Priority.choices(),
        default=Priority.MEDIUM[0]
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    tags = models.ManyToManyField(Tag, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(default=calculate_end_of_month)
    assignee = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='tasks',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-deadline']
        unique_together = ('name', 'project')

    def __str__(self):
        return f"{self.name}, status: {self.status}"
