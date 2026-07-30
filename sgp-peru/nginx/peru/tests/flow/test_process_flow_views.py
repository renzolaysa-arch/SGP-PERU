from django.test import RequestFactory, TestCase
from django.test.client import Client
from django.urls import reverse
from faker import Faker
from django.contrib.auth.models import User, Group
from users.models import Functionary, Unit_Central
from datetime import datetime, timedelta
from demand.models import *
from projects.models import *
from inventory.models import *
from providers.models import *
import pytest
import random
fake = Faker()


class DemandTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Unit central
        email = "test_unit_central@test.com"
        self.unit_central = Unit_Central.objects.create(
            user=User.objects.create_user(
                password="Ariadna00$",
                username=email,
                email=email,
                is_staff=False,
                is_active=True,
            ),
        )
        self.group = Group.objects.create(name='Unidad Central')
        self.unit_central.user.groups.add(self.group)

        # Functionary
        email = "test_functionary@test.com"
        self.functionary = Functionary.objects.create(
            user=User.objects.create_user(
                password="Ariadna00$",
                username=email,
                email=email,
                is_staff=False,
                is_active=True,
            ),
        )
        self.group = Group.objects.create(name='Funcionario')
        self.functionary.user.groups.add(self.group)

        # Project
        self.tags_project = TagsProject.on_site.create(name_tag_project=fake.company(
        ), type_color_choice=random.choice(['red', 'blue', 'orange', 'gray']))
        self.category_project = CategoryProject.on_site.create(
            name_category_project=fake.company())
        self.related_statistical = RelatedStatistical.on_site.create(
            name=fake.company())
        self.theme_project = ThemeProject.on_site.create(
            name_theme_project=fake.company())
        self.state_project = StateProject.on_site.create(
            state_project=fake.company())
        self.project = Project.on_site.create(
            name=fake.paragraph(nb_sentences=1),
            objetive_project=fake.paragraph(nb_sentences=1),
            category_project=self.category_project,
            area_in_charge=fake.paragraph(nb_sentences=1),
            functionary_project=self.functionary,
            related_statistical_research=fake.company(),
            related_statistical=self.related_statistical,
            theme_project=self.theme_project,
            state_project=self.state_project,
        )

        # Provider
        self.provider_sector = ProviderSector.objects.create(
            name=fake.company())
        self.provider_type = ProviderType.objects.create(name=fake.company())
        self.provider_status = ProviderStatus.objects.create(
            name=fake.company())
        self.provider_entity = ProviderEntity.on_site.create(
            name='Entidad Test CDI',
            identification_number=random.randint(1000, 1050),
            description=fake.last_name(),
            sector=self.provider_sector,
            type=self.provider_type,
            image=fake.file_extension(category='image'),
            domain=fake.company(),
            status=self.provider_status
        )

        # Inventory
        self.inventory_theme = InventoryTheme.on_site.create(
            name_theme_inventory=fake.company())
        self.inventory_thematic = InventoryThematic.on_site.create(
            name_thematic_inventory=fake.company())
        self.inventory_status = InventoryStatus.on_site.create(
            name=fake.company())
        self.type_format_sampledata = TypeFormatSampleData.on_site.create(
            type_format='pdf')
        self.transfer_medium_sampledata = TransferMediumSampleData.on_site.create(
            transfer_medium=fake.company())
        self.tags_sampledata = TagsSampleData.on_site.create(
            tags_sample_data=fake.company())
        self.variables_sampledata = VariablesSampleData.on_site.create(
            variables_sample_data=fake.company())
        self.inventory = Inventory.on_site.create(
            title=fake.paragraph(nb_sentences=1),
            objective=fake.paragraph(5),
            inventory_theme_asociate=self.inventory_theme,
            inventory_thematic_asociate=self.inventory_thematic,
            use_laws_decrees=random.choice(['C.P', 'L', 'D.N']),
            document_choice=random.choice(['M.D', 'D.D', 'D.S']),
            nomenclature_choice=random.choice(['Si', 'No']),
            method_collections_choice=random.choice(['F.F', 'F.E', 'D.C']),
            frequency_choice=random.choice(['F.F', 'F.E', 'D.C']),
            processing_choice=random.choice(['E', 'A', 'R']),
            record_choice=random.choice(['S', 'N']),
            dependence_name=fake.bs(),
            director_name=fake.first_name(),
            security_choice=random.choice(
                ['Backups', 'Aislamiento del servidor', 'Utilización de perfiles']),
            information_stored_choice=random.choice(['Si', 'No']),
            information_choice=random.choice(
                ['Anual', 'Semestral', 'Bimensual', 'Trimestral']),
            type_format_data_asociate=self.type_format_sampledata,
            file_example_sample_data=fake.file_name(
                extension=self.type_format_sampledata),
            transfer_medium_data_asociate=self.transfer_medium_sampledata,
            entity_provider=self.provider_entity,
        )

        # Demand
        today = datetime.today()
        end_date = today + timedelta(days=30)
        self.demands_categories = DemandsCategories.on_site.create(
            name='Category')
        self.demands_status = DemandsStatus.on_site.create(name='Activo')
        self.demands_theme = DemandsTheme.on_site.create(name=fake.job())
        self.key_words = KeyWords.on_site.create(name=fake.job())
        self.topic = Topic.on_site.create(name=fake.job())
        self.demand = Demands.on_site.create(
            functionary=self.functionary,
            inventory=self.inventory,
            project=self.project,
            title=fake.job(),
            description=fake.paragraph(nb_sentences=1),
            use=random.choice(
                ['Realizar validación', 'Conformar un registro base', 'Estadística experimental']),
            use_other=fake.company(),
            time=random.choice(['1 mes', '2 meses', '3 meses', '11 meses']),
            product=fake.paragraph(nb_sentences=1),
            status=self.demands_status,
            category=self.demands_categories,
            theme=self.demands_theme,
            provider_entity=self.provider_entity,
            topic=self.topic,
            finish_date=fake.date_between_dates(today, end_date),
            file_demand=fake.file_name(extension='.pdf'),
            process='re',
            type='ex',
        )
        self.note = Note.on_site.create(
            demand=self.demand,
            commentary=fake.paragraph(nb_sentences=1),
            functionary=self.functionary,
        )

        # Reception
        self.reception = Reception.on_site.create(
            demand=self.demand,
        )

        # Transfer
        self.channels = Channels.objects.create(title='FTP')

    def test_create_demand(self):
        print("Solcictudes creadas:", Demands.on_site.all().count())
        print("Notificaciones creadas:", Notification.on_site.all().count())
        print("MP Recepcion creadas:", Reception.on_site.all().count())
        self.client.login(username="test_functionary@test.com",
                          password='Ariadna00$')
        url = reverse("demand:demand_create")
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)
        assert "form" in response.context
        response = self.client.post(reverse("demand:demand_create"), data={
            "title": fake.job(),
            "inventory": 1,
            "project": 1,
            "description": fake.paragraph(nb_sentences=1),
            "use": 'ca',
            "use_other": fake.company(),
            "time": '2',
            "product": fake.paragraph(nb_sentences=1),
            "category": 1,
            "status": 1,
            "theme": 1,
            "topic": 1,
            "file_demand": fake.file_name(extension='.pdf'),
            "functionary": 1,
            "form_id": "demandCreateForm",
        }, kwargs={})

        assert response.status_code == 302
        print("url", url, " :", response)
        print("Solcictudes creadas:", Demands.on_site.all().count())
        print("Notificaciones creadas:", Notification.on_site.all().count())
        print("MP Recepcion creadas:", Reception.on_site.all().count())

    def test_process_reception(self):
        date_demand_validation = datetime.today()
        date_tentative_presentation = date_demand_validation + \
            timedelta(days=20)
        date_agreed = date_demand_validation + \
            timedelta(days=40)
        date_agreement = date_agreed + timedelta(days=3)

        # LOGIN
        self.client.login(username="test_unit_central@test.com",
                          password='Ariadna00$')

        # -----------------------RECEPCION---------------------------- #
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>RECEPCION<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

        # -----------------------INICIO---------------------------- #
        # GET
        print("----------------------------------------------GET INICIO----------------------------------------------")
        url = reverse("demand:process_reception", kwargs={'id_demand': 1})
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)

        # POST
        print("----------------------------------------------POST INICIO----------------------------------------------")
        url = reverse("demand:process_reception", kwargs={'id_demand': 1})
        form_data = {'form_id': 'process_reception'}
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # VERIFICACION
        self.demand.refresh_from_db()
        self.reception.refresh_from_db()
        self.assertEqual(self.reception.demand_process, 'pr')
        self.assertEqual(self.reception.demand_subprocess, 'demand-validation')
        self.assertEqual(self.demand.process, 're')

        # PRINT
        print("SALIDA INICIO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        reception = Reception.on_site.get(demand=demand)
        print(reception.demand_process)
        print(reception.demand_subprocess)

        # -----------------------PROCESO---------------------------- #
        # GET
        print("----------------------------------------------GET PROCESO----------------------------------------------")
        url = reverse("demand:process_reception_process",
                      kwargs={'id_demand': 1})
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)

        # POST
        print("----------------------------------------------POST PROCESO----------------------------------------------")
        url = reverse("demand:process_reception_process",
                      kwargs={'id_demand': 1})
        form_data = {
            "status_demand_validation": "do",
            'form_id': 'formStep1'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST PROCESO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        reception = Reception.on_site.get(demand=demand)
        print(reception.demand_process)
        print(reception.demand_subprocess)

        # POST
        print("----------------------------------------------POST PROCESO----------------------------------------------")
        url = reverse("demand:process_reception_process",
                      kwargs={'id_demand': 1})
        form_data = {
            "demand_assessment": "5",
            'form_id': 'formStep2'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST PROCESO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        reception = Reception.on_site.get(demand=demand)
        print(reception.demand_process)
        print(reception.demand_subprocess)

        # POST
        print("----------------------------------------------POST PROCESO----------------------------------------------")
        url = reverse("demand:process_reception_process",
                      kwargs={'id_demand': 1})
        form_data = {
            "status_demand_notification": "do",
            "date_tentative_presentation": date_tentative_presentation,
            "comment": fake.paragraph(nb_sentences=1),
            'form_id': 'formStep3'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST PROCESO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        reception = Reception.on_site.get(demand=demand)
        print(reception.demand_process)
        print(reception.demand_subprocess)

        # POST
        print("----------------------------------------------POST PROCESO----------------------------------------------")
        url = reverse("demand:process_reception_process",
                      kwargs={'id_demand': 1})
        form_data = {
            'form_id': 'formStep4'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST PROCESO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        reception = Reception.on_site.get(demand=demand)
        print(reception.demand_process)
        print(reception.demand_subprocess)

        # -----------------------REVISION---------------------------- #
        # GET
        print("----------------------------------------------GET REVISION----------------------------------------------")
        url = reverse("demand:process_reception_revision",
                      kwargs={'id_demand': 1})
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)

        # POST
        print("----------------------------------------------POST REVISION----------------------------------------------")
        url = reverse("demand:process_reception_revision",
                      kwargs={'id_demand': 1})
        form_data = {
            'status_demand_validation': 'Y',
            'demand_assessment': 'Y',
            'status_demand_notification': 'Y',
            'date_tentative_presentation': 'Y',
            'comment': fake.paragraph(nb_sentences=1),
            'form_id': 'formReview'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST REVISION")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        reception = Reception.on_site.get(demand=demand)
        print(reception.demand_process)

        # -----------------------FINALIZADO---------------------------- #
        # GET
        print("----------------------------------------------GET FINALIZADO----------------------------------------------")
        url = reverse("demand:process_reception_finalize",
                      kwargs={'id_demand': 1})
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)

        # POST
        print("----------------------------------------------POST FINALIZADO----------------------------------------------")
        url = reverse("demand:process_reception_finalize",
                      kwargs={'id_demand': 1})
        form_data = {
            'status_demand_validation': 'Y',
            'demand_assessment': 'Y',
            'status_demand_notification': 'Y',
            'date_tentative_presentation': 'Y',
            'comment': fake.paragraph(nb_sentences=1),
            'form_id': 'formReview'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST FINALIZADO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        reception = Reception.on_site.get(demand=demand)
        print(reception.demand_process)

        # -----------------------NEGOCIACION---------------------------- #
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>NEGOCIACION<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

        # -----------------------INICIO---------------------------- #
        # GET
        print("----------------------------------------------GET INICIO----------------------------------------------")
        url = reverse("demand:process_negotiation",
                      kwargs={'id_demand': 1})
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)

        # POST
        print("----------------------------------------------POST INICIO----------------------------------------------")
        url = reverse("demand:process_negotiation", kwargs={'id_demand': 1})
        form_data = {
            'multilist': 'Entidad Test CDI',
            'form_id': 'beginRelationForm'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST INICIO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        negotiation = Negotiation.on_site.get(demand=demand)
        print(negotiation.demand_process)
        provider_demand = ProviderDemand.on_site.filter(negotiation=negotiation).count()
        print("Proveedor seleccionado: ", provider_demand)

        # -----------------------PROCESO---------------------------- #
        # GET
        print("----------------------------------------------GET PROCESO----------------------------------------------")
        url = reverse("demand:process_negotiation_process",
                      kwargs={'id_demand': 1})
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)

        # POST
        print("----------------------------------------------POST PROCESO----------------------------------------------")
        url = reverse("demand:process_negotiation_process",
                      kwargs={'id_demand': 1})
        form_data = {
            'state-demand-1': 'do',
            'state-reception-1': 'do',
            'form_id': 'formStep1'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST PROCESO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        negotiation = Negotiation.on_site.get(demand=demand)
        print(negotiation.demand_process)
        print(negotiation.demand_subprocess)

        # POST
        print("----------------------------------------------POST PROCESO----------------------------------------------")
        url = reverse("demand:process_negotiation_process",
                      kwargs={'id_demand': 1})
        form_data = {
            'selected-agreement': 1,
            'form_id': 'formStep2'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST PROCESO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        negotiation = Negotiation.on_site.get(demand=demand)
        print(negotiation.demand_process)
        print(negotiation.demand_subprocess)

        # POST
        print("----------------------------------------------POST PROCESO----------------------------------------------")
        url = reverse("demand:process_negotiation_process",
                      kwargs={'id_demand': 1})
        form_data = {
            'form_id': 'formStep3'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST PROCESO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        negotiation = Negotiation.on_site.get(demand=demand)
        print(negotiation.demand_process)
        print(negotiation.demand_subprocess)

        # POST
        print("----------------------------------------------POST PROCESO----------------------------------------------")
        url = reverse("demand:process_negotiation_process",
                      kwargs={'id_demand': 1})
        form_data = {
            'status_demand_negotiation': 'do',
            'form_id': 'formStep4'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST PROCESO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        negotiation = Negotiation.on_site.get(demand=demand)
        print(negotiation.demand_process)
        print(negotiation.demand_subprocess)

        # POST
        print("----------------------------------------------POST PROCESO----------------------------------------------")
        url = reverse("demand:process_negotiation_process",
                      kwargs={'id_demand': 1})
        form_data = {
            'date_agreed': date_agreed.strftime('%Y-%m-%d'),
            'time': '1',
            'date_agreement': date_agreement.strftime('%Y-%m-%d'),
            'consideration': 'Capacitacion',
            'form_id': 'formStep5'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST PROCESO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        negotiation = Negotiation.on_site.get(demand=demand)
        print(negotiation.demand_process)
        print(negotiation.demand_subprocess)

        # -----------------------REVISION---------------------------- #
        # GET
        print("----------------------------------------------GET REVISION----------------------------------------------")
        url = reverse("demand:process_negotiation_revision",
                      kwargs={'id_demand': 1})
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)

        # POST
        print("----------------------------------------------POST REVISION----------------------------------------------")
        url = reverse("demand:process_negotiation_revision",
                      kwargs={'id_demand': 1})
        form_data = {
            'meets_expectations': 'Y',
            'required_documentation': 'Y',
            'ready_sign': 'Y',
            'form_id': 'formReview'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST PROCESO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        negotiation = Negotiation.on_site.get(demand=demand)
        print(negotiation.demand_process)

        # -----------------------FINALIZADO ---------------------------- #
        # GET
        print("----------------------------------------------GET FINALIZADO----------------------------------------------")
        url = reverse("demand:process_negotiation_finalize",
                      kwargs={'id_demand': 1})
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)

        # POST
        print("----------------------------------------------POST FINALIZADO----------------------------------------------")
        url = reverse("demand:process_negotiation_finalize",
                      kwargs={'id_demand': 1})
        form_data = {
            'comment_finalized': fake.paragraph(nb_sentences=1),
            'form_id': 'formFinalizedRelation'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST PROCESO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        negotiation = Negotiation.on_site.get(demand=demand)
        print(negotiation.demand_process)

        # -----------------------TRANSFERENCIA---------------------------- #
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>TRANSFERENCIA<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

        # -----------------------INICIO---------------------------- #
        # GET
        print("----------------------------------------------GET INICIO----------------------------------------------")
        url = reverse("demand:process_transfer",
                      kwargs={'id_demand': 1})
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)

        # POST
        print("----------------------------------------------POST INICIO----------------------------------------------")
        url = reverse("demand:process_transfer", kwargs={'id_demand': 1})
        form_data = {
            'transfer': 1,
            'channel': 1,
            'status_transfer': 'ac',
            'number_deliveries': 'Entrega 1',
            'date_delivery': date_agreed.strftime('%Y-%m-%d'),
            'frequency_delivery': '1@'+date_agreed.strftime('%Y-%m-%d'),
            'comment': fake.paragraph(nb_sentences=1),
            'form_id': 'beginRelationForm'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST INICIO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        transfer = Transfer.on_site.get(demand=demand)
        print(transfer.demand_process)
        print("MP transfers creadas:", Transfers.on_site.all().count())

        # -----------------------PROCESO---------------------------- #
        # GET
        print("----------------------------------------------GET PROCESO----------------------------------------------")
        url = reverse("demand:process_transfer_process",
                      kwargs={'id_demand': 1})
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)

        # POST
        print("----------------------------------------------POST PROCESO----------------------------------------------")
        url = reverse("demand:process_transfer_process",
                      kwargs={'id_demand': 1})
        form_data = {
            'form_id': 'formStep1'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST PROCESO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        transfer = Transfer.on_site.get(demand=demand)
        print(transfer.demand_process)

        # -----------------------REVISION---------------------------- #
        # GET
        print("----------------------------------------------GET REVISION----------------------------------------------")
        url = reverse("demand:process_transfer_revision",
                      kwargs={'id_demand': 1})
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)

        # POST
        print("----------------------------------------------POST REVISION----------------------------------------------")
        url = reverse("demand:process_transfer_revision",
                      kwargs={'id_demand': 1})
        form_data = {
            'review': 1,
            'date_review': date_agreed.strftime('%Y-%m-%d'),
            'hour_review': date_agreed.strftime('%H:%M'),
            "open_base": "Y",
            "expected_size": "Y",
            "meets_terms": "Y",
            "approve_reception_bd": "Y",
            "comment_review": fake.paragraph(nb_sentences=1),
            'form_id': 'formReview'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST REVISION")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        transfer = Transfer.on_site.get(demand=demand)
        print(transfer.demand_process)

        # -----------------------FINALIZADO---------------------------- #
        # GET
        print("----------------------------------------------GET FINALIZADO----------------------------------------------")
        url = reverse("demand:process_transfer_finalize",
                      kwargs={'id_demand': 1})
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)

        # POST
        print("----------------------------------------------POST FINALIZADO----------------------------------------------")
        url = reverse("demand:process_transfer_finalize",
                      kwargs={'id_demand': 1})
        form_data = {
            'finalize': 1,
            'finalized-date-transfer': date_agreed.strftime('%Y-%m-%d'),
            'finalized-hour-transfer': date_agreed.strftime('%H:%M'),
            "finalize_comment": fake.paragraph(nb_sentences=1),
            'form_id': 'formFinalizedTransfer-1'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST FINALIZADO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        transfer = Transfer.on_site.get(demand=demand)
        print(transfer.demand_process)

        # POST
        print("----------------------------------------------POST FINALIZADO----------------------------------------------")
        url = reverse("demand:process_transfer_finalize",
                      kwargs={'id_demand': 1})
        form_data = {
            'form_id': 'finalizeTransferContinue'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST FINALIZADO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        transfer = Transfer.on_site.get(demand=demand)
        print(transfer.demand_process)

        # -----------------------PREPARARCION---------------------------- #
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>PREPARARCION<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

        # -----------------------INICIO---------------------------- #
        # GET
        print("----------------------------------------------GET INICIO----------------------------------------------")
        url = reverse("demand:process_preparation",
                      kwargs={'id_demand': 1})
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)

        # POST
        print("----------------------------------------------POST INICIO----------------------------------------------")
        url = reverse("demand:process_preparation", kwargs={'id_demand': 1})
        form_data = {
            'transfer': 1,
            'date': date_agreed.strftime('%Y-%m-%d'),
            'hour': date_agreed.strftime('%H:%M'),
            'coments': fake.paragraph(nb_sentences=1),
            'form_id': 'beginPreparationForm'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST INICIO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        preparation = Preparation.on_site.get(demand=demand)
        preparations = Preparations.on_site.get(preparation=preparation)
        print(preparation.demand_process)
        print(preparations.demand_subprocess)
        print("MP preparations creadas:", Preparations.on_site.all().count())

        # -----------------------PROCESO---------------------------- #
        # GET
        print("----------------------------------------------GET PROCESO----------------------------------------------")
        url = reverse("demand:process_preparation_process",
                      kwargs={'id_demand': 1})
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)

        # POST
        print("----------------------------------------------POST PROCESO----------------------------------------------")
        url = reverse("demand:process_preparation_process",
                      kwargs={'id_demand': 1}) + '?preparation=1'
        form_data = {
            'consistency_functionary': 1,
            'form_id': 'formStep1'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST PROCESO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        preparation = Preparation.on_site.get(demand=demand)
        preparations = Preparations.on_site.get(preparation=preparation)
        print(preparation.demand_process)
        print(preparations.demand_subprocess)

        # POST
        print("----------------------------------------------POST PROCESO----------------------------------------------")
        url = reverse("demand:process_preparation_process",
                      kwargs={'id_demand': 1}) + '?preparation=1'
        form_data = {
            'standardization_functionary': 1,
            'form_id': 'formStep2'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST PROCESO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        preparation = Preparation.on_site.get(demand=demand)
        preparations = Preparations.on_site.get(preparation=preparation)
        print(preparation.demand_process)
        print(preparations.demand_subprocess)

        # POST
        print("----------------------------------------------POST PROCESO----------------------------------------------")
        url = reverse("demand:process_preparation_process",
                      kwargs={'id_demand': 1}) + '?preparation=1'
        form_data = {
            'anomaly_functionary': 1,
            'form_id': 'formStep3'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST PROCESO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        preparation = Preparation.on_site.get(demand=demand)
        preparations = Preparations.on_site.get(preparation=preparation)
        print(preparation.demand_process)
        print(preparations.demand_subprocess)

        # POST
        print("----------------------------------------------POST PROCESO----------------------------------------------")
        url = reverse("demand:process_preparation_process",
                      kwargs={'id_demand': 1}) + '?preparation=1'
        form_data = {
            'anonymization_functionary': 1,
            'form_id': 'formStep4'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST PROCESO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        preparation = Preparation.on_site.get(demand=demand)
        preparations = Preparations.on_site.get(preparation=preparation)
        print(preparation.demand_process)
        print(preparations.demand_subprocess)

        # -----------------------REVISION---------------------------- #
        # GET
        print("----------------------------------------------GET REVISION----------------------------------------------")
        url = reverse("demand:process_preparation_revision",
                      kwargs={'id_demand': 1})
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)

        # POST
        print("----------------------------------------------POST REVISION----------------------------------------------")
        url = reverse("demand:process_preparation_revision",
                      kwargs={'id_demand': 1}) + '?preparation=1'
        form_data = {
            'date': date_agreed.strftime('%Y-%m-%d'),
            'hour': date_agreed.strftime('%H:%M'),
            'question_1': 'Respuesta 1',
            'question_2': 'Respuesta 1',
            'question_3': 'Respuesta 1',
            'coments': fake.paragraph(nb_sentences=1),
            'form_id': 'formReview'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST REVISION")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        preparation = Preparation.on_site.get(demand=demand)
        print(preparation.demand_process)


        # -----------------------FINALIZADO---------------------------- #
        # GET
        print("----------------------------------------------GET FINALIZADO----------------------------------------------")
        url = reverse("demand:process_preparation_finalize",
                      kwargs={'id_demand': 1})
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)

        # POST
        print("----------------------------------------------POST FINALIZADO----------------------------------------------")
        url = reverse("demand:process_preparation_finalize",
                      kwargs={'id_demand': 1}) + '?preparation=1'
        form_data = {
            'date_finalize': date_agreed.strftime('%Y-%m-%d'),
            'hour_finalize': date_agreed.strftime('%H:%M'),
            'coments_finalize': fake.paragraph(nb_sentences=1),
            'form_id': 'formFinalize'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST FINALIZADO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        preparation = Preparation.on_site.get(demand=demand)
        print(preparation.demand_process)

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>EVALUACION<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

        # -----------------------INICIO---------------------------- #
        # GET
        print("----------------------------------------------GET INICIO----------------------------------------------")
        url = reverse("demand:process_evaluation",
                      kwargs={'id_demand': 1})
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)

        # POST
        print("----------------------------------------------POST INICIO----------------------------------------------")
        url = reverse("demand:process_evaluation", kwargs={'id_demand': 1})
        form_data = {
            'evaluation_functionary': 1,
            'date_notification': date_agreed.strftime('%Y-%m-%d'),
            'finish_date': (date_agreed + timedelta(days=61)).strftime('%Y-%m-%d'),
            'evaluation_frequency': 2,
            'form_id': 'evaluation_init'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST INICIO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        evaluation = Evaluation.on_site.get(demand=demand)
        print(evaluation.demand_process)
        print("MP evaluations creadas:", Evaluations.on_site.all().count())
        
        # -----------------------PROCESO---------------------------- #
        # GET
        print("----------------------------------------------GET PROCESO----------------------------------------------")
        url = reverse("demand:process_evaluation_process",
                      kwargs={'id_demand': 1})
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)

        # POST
        print("----------------------------------------------POST PROCESO----------------------------------------------")
        url = reverse("demand:process_evaluation_process", kwargs={'id_demand': 1})
        form_data = {
            'coments_interview': fake.paragraph(nb_sentences=1),
            'id_evaluation':1,
            'form_id': 'formInterview'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST PROCESO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        evaluation = Evaluation.on_site.get(demand=demand)
        print(evaluation.demand_process)
        print("MP evaluations creadas:", Evaluations.on_site.all().count())
        
        # -----------------------REVISION---------------------------- #
        # GET
        print("----------------------------------------------GET REVISION----------------------------------------------")
        url = reverse("demand:process_evaluation_revision",
                      kwargs={'id_demand': 1})
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)

        # POST
        print("----------------------------------------------POST REVISION----------------------------------------------")
        url = reverse("demand:process_evaluation_revision", kwargs={'id_demand': 1})
        form_data = {
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST REVISION")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        evaluation = Evaluation.on_site.get(demand=demand)
        print(evaluation.demand_process)
        print("MP evaluations creadas:", Evaluations.on_site.all().count())
        
        # -----------------------FINALIZADO---------------------------- #
        # GET
        print("----------------------------------------------GET FINALIZADO----------------------------------------------")
        url = reverse("demand:process_evaluation_finalize",
                      kwargs={'id_demand': 1})
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)

        # POST
        print("----------------------------------------------POST FINALIZADO----------------------------------------------")
        url = reverse("demand:process_evaluation_finalize", kwargs={'id_demand': 1})
        form_data = {
            'coments_finalize': fake.paragraph(nb_sentences=1),
            'form_id': 'formFinalize'
        }
        response = self.client.post(url, data=form_data)
        assert response.status_code == 302
        print("url", url, " :", response)

        # PRINT
        print("SALIDA POST FINALIZADO")
        demand = Demands.on_site.get(pk=1)
        print(demand.process)
        evaluation = Evaluation.on_site.get(demand=demand)
        print(evaluation.demand_process)
        print("MP evaluations creadas:", Evaluations.on_site.all().count())
        
    