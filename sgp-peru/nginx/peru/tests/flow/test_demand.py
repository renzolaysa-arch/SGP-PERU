from demand.models import DemandsCategories, DemandsStatus, DemandsTheme, KeyWords, Topic, Demands, Note, ProcessesManager, Reception, Channels, Negotiation, ProviderDemand
from demand.models import Transfer, Transfers, Preparation, Preparations, Evaluation, Evaluations, DocumentDefinitionObjetives, ParticipationDemand
from users.models import Functionary, User
from content.models import Documents
from tests.flow.test_inventory import *
from tests.flow.test_project import *
from tests.flow.test_provider import *
import pytest
import re
from faker import Faker
import random
from datetime import date, datetime, timedelta

fake = Faker()


@pytest.fixture
def category_demand_factory(db):
    def factory(**kwargs):
        kwargs.setdefault("name", random.choice(
            ['Empleo', 'Economía', 'Desempleo']))
        # same for other fields
        return DemandsCategories.on_site.create(**kwargs)
    return factory


@pytest.fixture
def status_demand_factory(db):
    def factory(**kwargs):
        kwargs.setdefault("name", random.choice(['Activo', 'Inactivo']))
        # same for other fields
        return DemandsStatus.on_site.create(**kwargs)
    return factory


@pytest.fixture
def theme_demand_factory(db):
    def factory(**kwargs):
        kwargs.setdefault("name", fake.job())
        # same for other fields
        return DemandsTheme.on_site.create(**kwargs)
    return factory


@pytest.fixture
def keywords_demand_factory(db):
    def factory(**kwargs):
        kwargs.setdefault("name", fake.bs())
        # same for other fields
        return KeyWords.on_site.create(**kwargs)
    return factory


@pytest.fixture
def topic_demand_factory(db):
    def factory(**kwargs):
        kwargs.setdefault("name", fake.cryptocurrency_code())
        # same for other fields
        return Topic.on_site.create(**kwargs)
    return factory


@pytest.fixture
def functionary_demand(db):
    def factory(**kwargs):
        email = fake.email()
        functionary = Functionary.objects.create(
            user=User.objects.create_user(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password="Ariadna00$",
                username=email,
                email=email,
                is_staff=False,
                is_active=True,
            ),
        )
        return functionary
    return factory


@pytest.fixture
def demand_factory(functionary_demand, inventory_factory, project_factory, category_demand_factory, status_demand_factory, theme_demand_factory, entity_factory, topic_demand_factory, keywords_demand_factory):
    def factory(**kwargs):
        today = datetime.today()
        end_date = today + timedelta(days=30)
        keywords = keywords_demand_factory()
        kwargs.setdefault("functionary", functionary_demand())
        kwargs.setdefault("inventory", inventory_factory())
        kwargs.setdefault("project", project_factory())
        kwargs.setdefault("title", fake.job())
        kwargs.setdefault("description", fake.paragraph(nb_sentences=1))
        kwargs.setdefault("use", random.choice(
            ['Realizar validación', 'Conformar un registro base', 'Estadística experimental']))
        kwargs.setdefault("time", random.choice(
            ['1 mes', '2 meses', '3 meses', '11 meses']))
        kwargs.setdefault("product", fake.paragraph(nb_sentences=1))
        kwargs.setdefault("status", status_demand_factory())
        kwargs.setdefault("category", category_demand_factory())
        kwargs.setdefault("theme", theme_demand_factory())
        kwargs.setdefault("provider_entity", entity_factory())
        kwargs.setdefault("topic", topic_demand_factory())
        kwargs.setdefault(
            "finish_date", fake.date_between_dates(today, end_date))
        kwargs.setdefault("file_demand", fake.file_name(extension='.pdf'))
        kwargs.setdefault("process", random.choice(
            ['re', 'ne', 'tr', 'pr',  'ev']))
        kwargs.setdefault("type", random.choice(['ex', 'in']))

        demand = Demands.on_site.create(**kwargs)
        demand.key_words.add(keywords)
        return demand
    return factory


@pytest.mark.django_db
def test_demand_factory(db, demand_factory):
    demand = demand_factory()
    print("registro solicitud", demand.id, demand.title)
    assert demand.id == 1


@pytest.fixture
def note_demand_factory(db, demand_factory, functionary_demand):
    def factory(**kwargs):
        kwargs.setdefault("demand", demand_factory())
        kwargs.setdefault("commentary", fake.paragraph(nb_sentences=1))
        kwargs.setdefault("functionary", functionary_demand())

        note_demand = Note.on_site.create(**kwargs)
        return note_demand
    return factory


@pytest.mark.django_db
def test_note_demand_factory(db, note_demand_factory):
    demand = note_demand_factory()
    print("Comentario", demand.id, demand.commentary)
    assert demand.id == 1


@pytest.fixture
def documents_demand_factory(db, functionary_demand):
    def factory(**kwargs):
        user = functionary_demand()
        kwargs.setdefault("title", "asdasdas")
        kwargs.setdefault("document", fake.file_name(extension='pdf'))
        kwargs.setdefault("assigned_to", user.user)
        kwargs.setdefault("requires_approval", random.choice([True, False]))
        kwargs.setdefault("approved", random.choice([True, False]))
        kwargs.setdefault("comment", fake.paragraph(nb_sentences=1))
        # same for other fields
        document = Documents.on_site.create(**kwargs)
        document.copy_to.add(user.user)
        return document
    return factory


@pytest.fixture
def reception_demand_factory(db, status_demand_factory, demand_factory, documents_demand_factory):
    def factory(**kwargs):
        date_demand_validation = datetime.today()
        date_verification_completeness = date_demand_validation + \
            timedelta(days=15)
        date_tentative_presentation = date_demand_validation + \
            timedelta(days=20)
        date_demand_presentation = date_demand_validation + timedelta(days=30)
        date_demand_finalized = date_demand_validation + timedelta(days=40)
        time_demand_finalized = date_demand_finalized - date_demand_validation
        kwargs.setdefault("demand", demand_factory())
        kwargs.setdefault("date_demand_validation", date_demand_validation)
        kwargs.setdefault("date_verification_completeness",
                          date_verification_completeness)
        kwargs.setdefault("date_demand_notification",
                          date_verification_completeness)
        kwargs.setdefault("date_tentative_presentation",
                          date_tentative_presentation)
        kwargs.setdefault("date_demand_presentation", date_demand_presentation)
        kwargs.setdefault("status_demand_validation", status_demand_factory())
        kwargs.setdefault("status_demand_notification",
                          status_demand_factory())
        kwargs.setdefault("comment", fake.paragraph(nb_sentences=1))
        kwargs.setdefault("demand_subprocess", random.choice(
            ['demand-validation', 'verification-completeness', 'demand-notification', 'technical-committee-presentation']))
        kwargs.setdefault("demand_assessment",
                          random.choice(['1', '2', '3', '4']))
        kwargs.setdefault("date_demand_presentation", date_demand_presentation)
        kwargs.setdefault("comment_revision", fake.paragraph(nb_sentences=1))
        kwargs.setdefault("punctual_need", random.choice(['Si', 'No']))
        kwargs.setdefault("full_justification", random.choice(['Si', 'No']))
        kwargs.setdefault("approval_instance", random.choice(['Si', 'No']))
        kwargs.setdefault("date_demand_finalized", date_demand_finalized)
        kwargs.setdefault("date_demand_finalized", time_demand_finalized)
        kwargs.setdefault("comment_finalized", fake.paragraph(nb_sentences=1))

        reception_demand = Reception.on_site.create(**kwargs)
        reception_demand.doc_verification_completeness.add(
            documents_demand_factory())
        reception_demand.doc_committee_presentation.add(
            documents_demand_factory())
        return reception_demand
    return factory


@pytest.mark.django_db
def test_reception_demand_factory(db, reception_demand_factory):
    reception = reception_demand_factory()
    print("Reception", reception.id, "Fecha: ",
          reception.date_verification_completeness, reception.comment)
    assert reception.id == 1


@pytest.fixture
def chanel_demand_factory(db):
    def factory(**kwargs):
        kwargs.setdefault("title", random.choice(
            ['WebService', 'FTP', 'Correo',  'Drive']))

        return Channels.objects.create(**kwargs)
    return factory


@pytest.fixture
def negotiation_demand_factory(db, demand_factory, documents_demand_factory, chanel_demand_factory):
    def factory(**kwargs):
        date_demand_validation = datetime.today()
        date_demand_confirmation = date_demand_validation + timedelta(days=5)
        date_definition_objetives = date_demand_validation + timedelta(days=10)
        date_scope_validate = date_demand_validation + timedelta(days=15)
        date_structuring_agreement = date_demand_validation + \
            timedelta(days=15)
        date_agreement = date_structuring_agreement - date_demand_validation
        date_revision = date_demand_validation + timedelta(days=20)
        date_finalize = date_demand_validation + timedelta(days=25)
        kwargs.setdefault("demand", demand_factory())
        kwargs.setdefault("demand_subprocess", random.choice(
            ['demand-validation', 'provider-confirmation', 'definition-objetives-and-scope',  'scope-validation']))
        kwargs.setdefault("date_demand_validation", date_demand_validation)
        kwargs.setdefault("date_demand_confirmation", date_demand_confirmation)
        kwargs.setdefault("date_definition_objetives",
                          date_definition_objetives)
        kwargs.setdefault("date_scope_validate", date_scope_validate)
        kwargs.setdefault("status_demand_negotiation",
                          random.choice(['Aprobado', 'Rechazado']))
        kwargs.setdefault("date_structuring_agreement",
                          date_structuring_agreement)
        kwargs.setdefault("time", random.randint(1, 12))
        kwargs.setdefault("type_time", "days")
        kwargs.setdefault("channel", chanel_demand_factory())
        #kwargs.setdefault("date_agreement", date_agreement())
        kwargs.setdefault("consideration", fake.job())
        kwargs.setdefault("date_revision", date_revision)
        kwargs.setdefault("meets_expectations", random.choice(['Si', 'No']))
        kwargs.setdefault("required_documentation",
                          random.choice(['Si', 'No']))
        kwargs.setdefault("ready_sign", random.choice(['Si', 'No']))
        kwargs.setdefault("date_finalize", date_finalize)
        kwargs.setdefault("comment_finalized", fake.paragraph(nb_sentences=1))

        negotiation_demand = Negotiation.on_site.create(**kwargs)
        negotiation_demand.doc_demand_validation.add(
            documents_demand_factory())
        negotiation_demand.doc_definition_objetives.add(
            documents_demand_factory())
        negotiation_demand.doc_structuring_agreement.add(
            documents_demand_factory())
        negotiation_demand.doc_revision.add(documents_demand_factory())
        return negotiation_demand
    return factory


@pytest.mark.django_db
def test_negotiation_demand_factory(db, negotiation_demand_factory):
    negotiation = negotiation_demand_factory()
    print("Negotiation", negotiation.id, "Subproceso: ",
          negotiation.demand_subprocess, negotiation.comment_finalized)
    assert negotiation.id == 1


@pytest.fixture
def privider_demand_factory(db, negotiation_demand_factory, entity_factory):
    def factory(**kwargs):
        kwargs.setdefault("negotiation", negotiation_demand_factory())
        kwargs.setdefault("provider_entity", entity_factory())
        kwargs.setdefault("status_demand", random.choice(
            ['Aceptada', 'Pendiente', 'Rechazado']))
        kwargs.setdefault("status_record", random.choice(
            ['Disponible', 'Pendiente']))
        return ProviderDemand.on_site.create(**kwargs)
    return factory


@pytest.mark.django_db
def test_provider_demand_factory(db, privider_demand_factory):
    privider_demand = privider_demand_factory()
    print("Provider Demand", privider_demand.id, "Provider: ",
          privider_demand.provider_entity, privider_demand.negotiation)
    assert privider_demand.id == 1


@pytest.fixture
def transfer_demand_factory(db, demand_factory):
    def factory(**kwargs):
        kwargs.setdefault("demand", demand_factory())
        kwargs.setdefault("demand_process", random.choice(['ini', 'pr', 're']))
        return Transfer.on_site.create(**kwargs)
    return factory


@pytest.fixture
def transfers_demand_factory(db, transfer_demand_factory, chanel_demand_factory):
    def factory(**kwargs):
        kwargs.setdefault("transfer", transfer_demand_factory())
        kwargs.setdefault("channel", chanel_demand_factory())
        kwargs.setdefault("status_transfer", random.choice(
            ['Aceptada', 'Pendiente', 'Rechazado']))
        kwargs.setdefault("number_deliveries", random.randint(1, 12))
        kwargs.setdefault("date_delivery", datetime.today())
        kwargs.setdefault("frequency_delivery", random.randint(1, 12))
        kwargs.setdefault("frequency_date_delivery", datetime.today())
        kwargs.setdefault("comment", fake.paragraph(nb_sentences=1))
        kwargs.setdefault("reviewed", random.choice([True, False]))
        kwargs.setdefault("finalize", random.choice([True, False]))
        kwargs.setdefault("validate_preparation", random.choice([True, False]))
        return Transfers.on_site.create(**kwargs)
    return factory


@pytest.mark.django_db
def test_transfer_demand_factory(db, transfers_demand_factory):
    transfer = transfers_demand_factory()
    assert transfer.id == 1


@pytest.fixture
def preparation_demand_factory(db, demand_factory):
    def factory(**kwargs):
        kwargs.setdefault("demand", demand_factory())
        kwargs.setdefault("demand_process", random.choice(['ini', 'pr', 're']))

        return Preparation.on_site.create(**kwargs)
    return factory


@pytest.fixture
def preparations_demand_factory(db, preparation_demand_factory, transfers_demand_factory, documents_demand_factory, functionary_demand):
    def factory(**kwargs):
        date_consistency = datetime.today() + timedelta(days=5)
        date_standarization = date_consistency + timedelta(days=5)
        date_detection = date_standarization + timedelta(days=5)
        date_anonymization = date_detection + timedelta(days=5)
        date_revision = date_anonymization + timedelta(days=5)
        date_finalize = date_revision + timedelta(days=5)

        kwargs.setdefault("preparation", preparation_demand_factory())
        kwargs.setdefault("transfer", transfers_demand_factory())
        kwargs.setdefault("demand_subprocess", random.choice(
            ['consistency', 'standardization-normalization', 'anomaly-detection']))
        kwargs.setdefault("date_verification", datetime.today())
        kwargs.setdefault("comment", fake.paragraph(nb_sentences=1))
        kwargs.setdefault("date_consistency", date_consistency)

        kwargs.setdefault("consistency_functionary", functionary_demand())
        kwargs.setdefault("consistency_answer", random.choice([True, False]))
        kwargs.setdefault("consistency_question_1", random.randint(1, 5))
        kwargs.setdefault("consistency_question_2", random.randint(1, 5))
        kwargs.setdefault("consistency_question_3", random.randint(1, 5))
        kwargs.setdefault("date_standarization", date_standarization)

        kwargs.setdefault("standardization_functionary", functionary_demand())
        kwargs.setdefault("standardization_answer",
                          random.choice([True, False]))
        kwargs.setdefault("standarization_question_1", random.randint(1, 5))
        kwargs.setdefault("standarization_question_2", random.randint(1, 5))
        kwargs.setdefault("standarization_question_3", random.randint(1, 5))
        kwargs.setdefault("date_detection", date_detection)

        kwargs.setdefault("anomaly_functionary", functionary_demand())
        kwargs.setdefault("anomaly_answer", random.choice([True, False]))
        kwargs.setdefault("detection_question_1", random.randint(1, 5))
        kwargs.setdefault("detection_question_2", random.randint(1, 5))
        kwargs.setdefault("detection_question_3", random.randint(1, 5))
        kwargs.setdefault("date_anonymization", date_anonymization)

        kwargs.setdefault("anonymization_functionary", functionary_demand())
        kwargs.setdefault("anonymization_answer", random.choice([True, False]))
        kwargs.setdefault("anonymization_question_1", random.randint(1, 5))
        kwargs.setdefault("anonymization_question_2", random.randint(1, 5))
        kwargs.setdefault("anonymization_question_3", random.randint(1, 5))
        kwargs.setdefault("date_revision", date_revision)

        kwargs.setdefault("comment_revision", fake.paragraph(nb_sentences=1))
        kwargs.setdefault("date_finalize", date_finalize)
        kwargs.setdefault("comment_finalize", fake.paragraph(nb_sentences=1))
        kwargs.setdefault("finalize", random.choice([True, False]))

        preparations = Preparations.on_site.create(**kwargs)
        preparations.doc_consistency.add(documents_demand_factory())
        preparations.doc_standarization.add(documents_demand_factory())
        preparations.doc_anonymization.add(documents_demand_factory())
        return preparations
    return factory


@pytest.mark.django_db
def test_preparation_demand_factory(db, preparation_demand_factory):
    preparation = preparation_demand_factory()
    assert preparation.id == 1


@pytest.fixture
def evaluation_demand_factory(db, documents_demand_factory, demand_factory):
    def factory(**kwargs):
        date_finalize = datetime.today() + timedelta(days=5)
        kwargs.setdefault("demand", demand_factory())
        kwargs.setdefault("demand_process", random.choice(
            ['ini', 'pr', 're', 'fi']))
        kwargs.setdefault("date_finalize", date_finalize)
        kwargs.setdefault("comment_finalize", fake.paragraph(nb_sentences=1))
        kwargs.setdefault("finalize", random.choice([True, False]))
        evaluation = Evaluation.on_site.create(**kwargs)
        evaluation.doc_evaluation.add(documents_demand_factory())
        return evaluation
    return factory


@pytest.fixture
def evaluations_demand_factory(db, evaluation_demand_factory, functionary_demand, documents_demand_factory):
    def factory(**kwargs):
        date_finalize = datetime.today() + timedelta(days=5)
        frequency_date_delivery = date.today()
        finish_date = frequency_date_delivery + timedelta(days=5)
        kwargs.setdefault("evaluation", evaluation_demand_factory())
        kwargs.setdefault("functionary", functionary_demand())
        kwargs.setdefault("date_notification", date_finalize)
        kwargs.setdefault("frequency", random.choice(
            ['2 Meses', '4 Meses', '6 Meses']))
        kwargs.setdefault("frequency_delivery", random.randint(1, 12))
        kwargs.setdefault("frequency_date_delivery", frequency_date_delivery)
        kwargs.setdefault("finish_date", finish_date)
        kwargs.setdefault("interview", fake.paragraph(nb_sentences=1))
        kwargs.setdefault("question_1", random.randint(1, 5))
        kwargs.setdefault("question_2", random.randint(1, 5))
        kwargs.setdefault("question_3", random.randint(1, 5))
        kwargs.setdefault("question_4", random.randint(1, 5))
        kwargs.setdefault("question_5", random.randint(1, 5))
        kwargs.setdefault("question_6", random.randint(1, 5))
        kwargs.setdefault("question_7", random.randint(1, 5))
        kwargs.setdefault("question_8", random.randint(1, 5))
        kwargs.setdefault("question_9", random.randint(1, 5))
        kwargs.setdefault("question_10", random.randint(1, 5))
        kwargs.setdefault("result", random.randint(1, 5))
        kwargs.setdefault("evaluation_answer", random.choice([True, False]))

        return Evaluations.on_site.create(**kwargs)
    return factory


@pytest.mark.django_db
def test_evaluations_demand_factory(db, evaluations_demand_factory):
    evaluation = evaluations_demand_factory()
    assert evaluation.id == 1


@pytest.fixture
def document_definition_demand_factory(db):
    def factory(**kwargs):

        kwargs.setdefault("name", fake.job())
        kwargs.setdefault("document", fake.file_name(extension='docx'))

        return DocumentDefinitionObjetives.on_site.create(**kwargs)
    return factory


@pytest.mark.django_db
def test_document_definition_demand_factory(db, document_definition_demand_factory):
    document_definition = document_definition_demand_factory()
    assert document_definition.id == 1


@pytest.fixture
def participation_demand_factory(db, functionary_demand, demand_factory):
    def factory(**kwargs):
        user = functionary_demand()
        kwargs.setdefault("user", user.user)
        kwargs.setdefault("demand", demand_factory())

        return ParticipationDemand.on_site.create(**kwargs)
    return factory


@pytest.mark.django_db
def test_participation_demand_factory(db, participation_demand_factory):
    participation = participation_demand_factory()
    assert participation.id == 1
