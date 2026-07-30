from content.models import News, Tags, Letter, Vocabulary, FAQs, Testimony
from weblog.models import ThemeThread, CommentThread
from users.models import User, Functionary
import pytest
import re
from faker import Faker
import random
fake = Faker()

@pytest.mark.django_db
def test_new_creation(db):
    tag = Tags.on_site.create(
        name_tag= random.choice(['Empleo', 'Gobierno', 'Economía']),
        type_color_choice = random.choice(['red', 'blue', 'grey'])
    )
    new = News.on_site.create(
            type_choice = random.choice(['New', 'C.E']),
            title = fake.first_name(),
            previous_description = fake.paragraph(nb_sentences=1),
            author = fake.first_name(),
            description_uno = fake.paragraph(nb_sentences=5), 
            description_dos = fake.paragraph(nb_sentences=5),
            main_image_new_desk = fake.file_extension(category='image'),
            main_image_new_mob = fake.file_extension(category='image')
        )
    new.tag_asociate.add(tag)
    assert new.id == 1


@pytest.mark.django_db
def test_glosary_creation(db):
    letter_value = Letter.on_site.create(
        name_letter= random.choice(['A', 'B', 'C']),
    )
    vocabulary = Vocabulary.on_site.create(
            letter = letter_value,
            word = fake.first_name(),
            meaning = fake.paragraph(nb_sentences=1),
        )
    assert vocabulary.id == 1

@pytest.mark.django_db
def test_faqs_creation(db):
    fag = FAQs.on_site.create(
            name_question_faqs = fake.paragraph(nb_sentences=1),
            response_faqs = fake.paragraph(nb_sentences=3),
        )
    assert fag.id == 1

@pytest.mark.django_db
def test_testimony_creation(db):
    email = fake.email()  
    user = User.objects.create_user(
        first_name = fake.first_name(),
        last_name = fake.last_name(),
        password="Ariadna00$",
        username=email,
        email=email,
        is_staff=False,
        is_active=True,
    )
    testimony = Testimony.on_site.create(
            user_testimony = user,
            logo = fake.file_extension(category='image'),
            title = "Lorem Ipsum is simply dummy text of the",
            video_image = fake.file_extension(category='image'),
            video_testimony = "https://youtu.be/q8ZzKsDbg3k", 
            description_testimony = fake.paragraph(nb_sentences=3)
        )
    assert testimony.id == 1


@pytest.mark.django_db
def test_binacle_creation(db):
    email = fake.email()
    functionary = Functionary.objects.create(
            user = User.objects.create_user(
                first_name = fake.first_name(),
                last_name = fake.last_name(),
                password="Ariadna00$",
                username=email,
                email=email,
                is_staff=False,
                is_active=True,
                ),
        )
    assert functionary.id ==1

    theme_thread = ThemeThread.on_site.create(
        name_thread= fake.job(),
        content_thread = fake.paragraph(nb_sentences=1),
        user_functionary_created = functionary,
    )
    comments = CommentThread.on_site.create(
            threadt_to_comment = theme_thread,
            commentary = fake.paragraph(nb_sentences=1),
            functionary_commented = functionary,
        )
    assert comments.id == 1

