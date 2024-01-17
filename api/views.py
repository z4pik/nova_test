from rest_framework import generics
from .models import Document
from .serializers import DocumentSerializer
from rest_framework.response import Response
from rest_framework import status
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

class CreateDocumentView(generics.CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def create(self, request, *args, **kwargs):
        # Получение данных из запроса
        name = request.data.get('name')
        data = request.data.get('data')

        # Создание документа
        document = Document.objects.create(name=name, data=data)

        # Путь к файлу с учетными данными
        credentials_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials.json')

        # Аутентификация PyDrive
        gauth = GoogleAuth(settings_file=credentials_path)

        # Попытка загрузки ранее сохраненного токена из файла
        gauth.LoadCredentialsFile("mycreds.txt")

        # Если токен не был найден, запускаем процесс аутентификации
        if gauth.credentials is None:
            # Открываем окно с выбором аккаунта для аутентификации
            gauth.LocalWebserverAuth()

        # Сохранение токена для последующих запросов
        if gauth.credentials:
            gauth.SaveCredentialsFile("mycreds.txt")

        # Создание экземпляра GoogleDrive с авторизацией
        drive = GoogleDrive(gauth)

        # Создание файла в Google Drive
        file_drive = drive.CreateFile({'title': name})
        file_drive.Upload()

        # Загрузка данных в созданный файл
        file_drive.SetContentString(data)
        file_drive.Upload()

        # Получение ID созданного файла
        file_id = file_drive['id']

        return Response({'file_id': file_id}, status=status.HTTP_201_CREATED)
