import random
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datacenter.models import Lesson
from datacenter.models import Schoolkid
from datacenter.models import Commendation
from datacenter.models import Subject
from datacenter.models import Mark
from datacenter.models import Chastisement


def fix_marks(schoolkid):
    try:
        child = Schoolkid.objects.get(full_name__contains=schoolkid)
    except ObjectDoesNotExist:
        print("Такой ученик отсутствует")
        return
    except MultipleObjectsReturned:
        print("Исправьте ФИО ученика")
        return
    Mark.objects.filter(schoolkid__id=child.id,
                        points__in=[2, 3]).update(points=5)


def remove_chastisements(schoolkid):
    try:
        child = Schoolkid.objects.filter(full_name__contains=schoolkid)
    except ObjectDoesNotExist:
        print("Такой ученик отсутствует")
        return
    except MultipleObjectsReturned:
        print("Исправьте ФИО ученика")
        return
    chastisements = Chastisement.objects.filter(schoolkid=child)
    chastisements.delete()


def create_commendation(schoolkid, lesson):
    commendations = [
                    "Молодец!",
                    "Отлично!",
                    "Хорошо!",
                    "Гораздо лучше, чем я ожидал!",
                    "Ты меня приятно удивил!",
                    "Великолепно!",
                    "Прекрасно!",
                    "Ты меня очень обрадовал!",
                    "Именно этого я давно ждал от тебя!",
                    "Сказано здорово – просто и ясно!",
                    "Ты, как всегда, точен!",
                    "Очень хороший ответ!",
                    "Талантливо!",
                    "Ты сегодня прыгнул выше головы!",
                    "Я поражен!",
                    "Уже существенно лучше!",
                    "Потрясающе!",
                    "Замечательно!",
                    "Прекрасное начало!",
                    "Так держать!"]
    commendation = random.choice(commendations)
    try:
        child = Schoolkid.objects.get(full_name__contains=schoolkid)
    except ObjectDoesNotExist:
        print("Такой ученик отсутствует")
        return
    except MultipleObjectsReturned:
        print("Исправьте ФИО ученика")
        return
    education_year = child.year_of_study
    group = child.group_letter
    try:
        subject = Subject.objects.get(title=lesson,
                                      year_of_study=education_year)
    except ObjectDoesNotExist:
        print("Такой предмет отсутствует")
        return
    last_lesson = Lesson.objects.filter(
        year_of_study=education_year,
        group_letter=group, subject=subject).order_by('-date').first()
    lesson_teacher = last_lesson.teacher
    lesson_date = last_lesson.date
    Commendation.objects.create(text=commendation, created=lesson_date,
                                schoolkid=child, subject=subject,
                                teacher=lesson_teacher)
