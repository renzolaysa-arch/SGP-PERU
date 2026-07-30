from datetime import timedelta
from demand.models import (Reception, Transfer,
                           Negotiation, Transfers, Preparation, Preparations, Evaluation, Evaluations)


def calculate_process_board(id_demand):
    reception = Reception.on_site.get(demand=id_demand)
    process_board = {
        "url_reception": None,
        "porcent_reception": 0,
        "status_reception": "",
        "url_negotiation": None,
        "porcent_negotiation": 0,
        "status_negotiation": "",
        "url_transfer": None,
        "porcent_transfer": 0,
        "status_transfer": "",
        "url_preparation": None,
        "porcent_preparation": 0,
        "status_preparation": "",
        "url_evaluation": None,
        "porcent_evaluation": 0,
        "status_evaluation": "",
    }

    try:
        negotiation = Negotiation.on_site.get(demand=id_demand)
    except Negotiation.DoesNotExist:
        negotiation = None

    try:
        transfer = Transfer.on_site.get(demand=id_demand)
    except Transfer.DoesNotExist:
        transfer = None

    try:
        preparation = Preparation.on_site.get(demand=id_demand)
    except Preparation.DoesNotExist:
        preparation = None

    try:
        evaluation = Evaluation.on_site.get(demand=id_demand)
    except Evaluation.DoesNotExist:
        evaluation = None

    ## reception ##
    ## reception ini ##
    if reception.demand_process == 'ini':
        process_board["url_reception"] = '/solicitud/' + \
            str(id_demand)+'/recepcion/inicio/'
        process_board["porcent_reception"] = 13
        process_board["status_reception"] = 'ini'

    ## reception pr ##
    elif reception.demand_process == 'pr':
        process_board["url_reception"] = '/solicitud/' + \
            str(id_demand)+'/recepcion/proceso/'
        if reception.demand_subprocess == 'demand-validation':
            process_board["porcent_reception"] = 31
        if reception.demand_subprocess == 'verification-completeness':
            process_board["porcent_reception"] = 37
        if reception.demand_subprocess == 'demand-notification':
            process_board["porcent_reception"] = 43
        if reception.demand_subprocess == 'technical-committee-presentation':
            process_board["porcent_reception"] = 50
        process_board["status_reception"] = 'pr'

    ## reception re ##
    elif reception.demand_process == 're':
        process_board["url_reception"] = '/solicitud/' + \
            str(id_demand)+'/recepcion/revision/'
        process_board["porcent_reception"] = 63
        process_board["status_reception"] = 're'

    ## reception fi ##
    elif reception.demand_process == 'fi':
        process_board["url_reception"] = '/solicitud/' + \
            str(id_demand)+'/recepcion/finalizado/'
        process_board["porcent_reception"] = 88
        process_board["status_reception"] = 'fi'

    ## negotiation ##
    if negotiation:
        process_board["porcent_reception"] = 100

        ## negotiation ini ##
        if negotiation.demand_process == 'ini':
            process_board["url_negotiation"] = '/solicitud/' + \
                str(id_demand)+'/relacionamiento/inicio/'
            process_board["porcent_negotiation"] = 13
            process_board["status_negotiation"] = 'ini'

        ## negotiation pr ##
        elif negotiation.demand_process == 'pr':
            process_board["url_negotiation"] = '/solicitud/' + \
                str(id_demand)+'/relacionamiento/proceso/'
            if negotiation.demand_subprocess == 'demand-validation':
                process_board["porcent_negotiation"] = 30
            if negotiation.demand_subprocess == 'provider-confirmation':
                process_board["porcent_negotiation"] = 35
            if negotiation.demand_subprocess == 'definition-objetives-and-scope':
                process_board["porcent_negotiation"] = 40
            if negotiation.demand_subprocess == 'scope-validation':
                process_board["porcent_negotiation"] = 45
            if negotiation.demand_subprocess == 'structuring-of-the-agreement':
                process_board["porcent_negotiation"] = 50
            process_board["status_negotiation"] = 'pr'

        ## negotiation re ##
        elif negotiation.demand_process == 're':
            process_board["url_negotiation"] = '/solicitud/' + \
                str(id_demand)+'/relacionamiento/revision/'
            process_board["porcent_negotiation"] = 63
            process_board["status_negotiation"] = 're'

        ## negotiation fi ##
        elif negotiation.demand_process == 'fi':
            process_board["url_negotiation"] = '/solicitud/' + \
                str(id_demand)+'/relacionamiento/finalizado/'
            process_board["porcent_negotiation"] = 88
            process_board["status_negotiation"] = 'fi'

    ## transfer ##
    if transfer:
        process_board["porcent_negotiation"] = 100

        ## transfer ini ##
        if transfer.demand_process == 'ini':
            process_board["url_transfer"] = '/solicitud/' + \
                str(id_demand)+'/transferencia/inicio/'
            process_board["status_transfer"] = 'ini'

        ## transfer pr ##
        elif transfer.demand_process == 'pr':
            process_board["url_transfer"] = '/solicitud/' + \
                str(id_demand)+'/transferencia/proceso/'
            process_board["status_transfer"] = 'pr'

        ## transfer re ##
        elif transfer.demand_process == 're':
            process_board["url_transfer"] = '/solicitud/' + \
                str(id_demand)+'/transferencia/revision/'
            process_board["status_transfer"] = 're'

        ## transfer fi ##
        elif transfer.demand_process == 'fi':
            process_board["url_transfer"] = '/solicitud/' + \
                str(id_demand)+'/transferencia/finalizado/'
            process_board["status_transfer"] = 'fi'

        cant_frequency = calculate_frequency_delivery(
            negotiation.date_agreed, negotiation.date_agreement, negotiation.time)
        try:
            cant_deliveries = Transfers.on_site.filter(transfer=transfer).distinct('frequency_delivery').count()
        except:
            cant_deliveries = 0
        
        if cant_frequency == 0:
            process_board["porcent_transfer"] = 0
        else:
            process_board["porcent_transfer"] = int(
                (cant_deliveries * 100) / cant_frequency)

    if preparation:
        ## preparation ini ##
        if preparation.demand_process == 'ini':
            process_board["url_preparation"] = '/solicitud/' + \
                str(id_demand)+'/preparacion/inicio/'
            process_board["porcent_preparation"] = 25
            process_board["status_preparation"] = 'ini'

        ## preparation pr ##
        elif preparation.demand_process == 'pr':
            process_board["url_preparation"] = '/solicitud/' + \
                str(id_demand)+'/preparacion/proceso/'
            process_board["porcent_preparation"] = 50
            process_board["status_preparation"] = 'pr'

        ## preparation re ##
        elif preparation.demand_process == 're':
            process_board["url_preparation"] = '/solicitud/' + \
                str(id_demand)+'/preparacion/revision/'
            process_board["porcent_preparation"] = 75
            process_board["status_preparation"] = 're'

        ## preparation fi ##
        elif preparation.demand_process == 'fi':
            process_board["url_preparation"] = '/solicitud/' + \
                str(id_demand)+'/preparacion/finalizado/'
            process_board["porcent_preparation"] = 100
            process_board["status_preparation"] = 'fi'
            
        try:
            cant_transfert = Transfers.on_site.filter(transfer=transfer).count()
        except:
            cant_transfert = 0
            
        try:
            cant_preparation = Preparations.on_site.filter(preparation=preparation, finalize=True).count()
        except:
            cant_preparation = 0
        
        if cant_preparation == 0:
            process_board["porcent_preparation"] = 0
        else:
            process_board["porcent_preparation"] = int(
                (cant_preparation * 100) / cant_transfert)

    ## evaluation ##
    if evaluation:

        ## evaluation ini ##
        if evaluation.demand_process == 'ini':
            process_board["url_evaluation"] = '/solicitud/' + \
                str(id_demand)+'/evaluacion/inicio/'
            process_board["status_evaluation"] = 'ini'

        ## evaluation pr ##
        elif evaluation.demand_process == 'pr':
            process_board["url_evaluation"] = '/solicitud/' + \
                str(id_demand)+'/evaluacion/proceso/'
            process_board["status_evaluation"] = 'pr'

        ## evaluation re ##
        elif evaluation.demand_process == 're':
            process_board["url_evaluation"] = '/solicitud/' + \
                str(id_demand)+'/evaluacion/revision/'
            process_board["status_evaluation"] = 're'

        ## evaluation fi ##
        elif evaluation.demand_process == 'fi':
            process_board["url_evaluation"] = '/solicitud/' + \
                str(id_demand)+'/evaluacion/finalizado/'
            process_board["status_evaluation"] = 'fi'

        cant_evaluation = Evaluations.on_site.filter(
            evaluation=evaluation).count()
        cant_answers = Evaluations.on_site.filter(
            evaluation=evaluation, evaluation_answer="True").count()

        if cant_evaluation == 0:
            process_board["porcent_evaluation"] = 0
        else:
            process_board["porcent_evaluation"] = int(
                (cant_answers * 100) / cant_evaluation)

    return process_board


def calculate_frequency_delivery(date_agreed, date_agreement, time):
    cont = 0
    day = 0
    frequency = date_agreed

    while frequency <= date_agreement:
        date_frequency = date_agreed + timedelta(days=day)
        day = day + time
        cont = cont + 1
        frequency = date_frequency

    return cont-1
