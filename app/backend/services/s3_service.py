import boto3
from botocore.exceptions import ClientError
from typing import List

BUCKET_NAME = "miwa-stack-miwafilesbucketcd77755d-j1dy7hsgswak"  # Cambia si tu bucket cambia

s3_client = boto3.client("s3")

def upload_file(file_obj, filename: str) -> str:
    """
    Sube un archivo a S3.
    :param file_obj: archivo tipo file-like (por ejemplo, de FastAPI UploadFile.file)
    :param filename: nombre con el que se guardará en S3
    :return: URL del archivo subido
    """
    try:
        s3_client.upload_fileobj(file_obj, BUCKET_NAME, filename)
        url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"
        return url
    except ClientError as e:
        raise Exception(f"Error al subir archivo: {e}")

def list_files() -> List[str]:
    """
    Lista los archivos en el bucket S3.
    :return: Lista de nombres de archivos
    """
    try:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
        if 'Contents' in response:
            return [obj['Key'] for obj in response['Contents']]
        return []
    except ClientError as e:
        raise Exception(f"Error al listar archivos: {e}")

def delete_file(filename: str) -> bool:
    """
    Borra un archivo del bucket S3.
    :param filename: nombre del archivo a borrar
    :return: True si se borró correctamente
    """
    try:
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=filename)
        return True
    except ClientError as e:
        raise Exception(f"Error al borrar archivo: {e}")
