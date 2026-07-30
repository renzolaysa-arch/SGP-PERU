from content.models import Visitor
import re
from datetime import datetime
from django.http import JsonResponse




def analytics(get_response):
    def middleware(request):
        # Código que se ejecutará antes del llamado a la vista.

        def get_ip(request):
            address = request.META.get('HTTP_X_FORWARDED_FOR')
            if address:
                ip = address.split(',')[-1].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')
            return ip

        def save_data(ip, type_user, path, name_model_visited, code_model_visited):

            # funcionalidad para obtener el modelo y el id
            u = Visitor(ip_user=ip, rol_visited=type_user, url_visited=path,
                        type_model_visited=name_model_visited, id_model_visited=code_model_visited)

            result = Visitor.on_site.filter(
                ip_user=ip, rol_visited=type_user, type_model_visited=name_model_visited, id_model_visited=code_model_visited)
            ##calcular el tiempo para que permita guardar de nuevo la visita luego de una hora
            date_format_str = '%d/%m/%Y %H:%M:%S.%f'
            date_2 = datetime.now()
            date_now = date_2.strftime(date_format_str)

            def calculate_hours(prov):
                date_create = prov.created_date.strftime(date_format_str)
                start = datetime.strptime(date_create, date_format_str)
                end = datetime.strptime(date_now, date_format_str)
                diff = end - start
                diff_in_hours = int(diff.total_seconds() / 3600)
                if diff_in_hours > 1:
                    try:
                        u.save()

                    except Exception as rollbackException:
                        return JsonResponse({'fail': 'True'})               
            if result.count() > 1:
                for prov in result:
                    calculate_hours(prov)
            else:
                try:
                    u.save()   
                except:
                    print("")
        ip = get_ip(request)
        path = request.path
        name_model_visited = ""
        code_model_visited = ""
        type_user = request.user.id

        # if "/noticias/" in path or "/lista-noticias/" in path:
        #     name_model_visited = "Noticias"
        #     if re.findall(r'/([0-9]+)', path):
        #         code_model_visited = re.findall(r'/([0-9]+)', path)
        #         for item in code_model_visited:
        #             code_model_visited = item
        #     save_data(ip, type_user, path,
        #               name_model_visited, code_model_visited)
        # elif "/contenido-academico/" in path or "/lista-contenido-academico/" in path:
        #     name_model_visited = "Contenido Educativo"
        #     if re.findall(r'/([0-9]+)', path):
        #         code_model_visited = re.findall(r'/([0-9]+)', path)
        #         for item in code_model_visited:
        #             code_model_visited = item
        #     save_data(ip, type_user, path,
        #               name_model_visited, code_model_visited)
        # elif "/lista-proveedores/" in path or "/proveedor/" in path:
        #     name_model_visited = "ProviderEntity"
        #     if re.findall(r'/([0-9]+)', path):
        #         code_model_visited = re.findall(r'/([0-9]+)', path)
        #         for item in code_model_visited:
        #             code_model_visited = item
        #     save_data(ip, type_user, path,
        #               name_model_visited, code_model_visited)
        # elif "/lista-proyectos/" in path or "/proyecto/" in path:
        #     name_model_visited = "Project"
        #     if re.findall(r'/([0-9]+)', path):
        #         code_model_visited = re.findall(r'/([0-9]+)', path)
        #         for item in code_model_visited:
        #             code_model_visited = item
        #     save_data(ip, type_user, path,
        #               name_model_visited, code_model_visited)
        if "/detalle-inventario/" in path:
            name_model_visited = "Registros Administrativos"
            if re.findall(r'/([0-9]+)', path):
                code_model_visited = re.findall(r'/([0-9]+)', path)
                for item in code_model_visited:
                    code_model_visited = item
            save_data(ip, type_user, path,
                      name_model_visited, code_model_visited)

        response = get_response(request)
        return response
    return middleware
