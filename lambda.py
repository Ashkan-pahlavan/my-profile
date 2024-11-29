
import os
import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,PUT,DELETE'
    } 

    # Den eingegebenen Text aus dem Event abrufen
    user_text = event['user_text']
    
    # Aktuelle Datum- und Uhrzeit als ID für den Eintrag verwenden
    entry_id = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    
    # AWS SDK-Clients für DynamoDB und SES initialisieren
    dynamodb = boto3.resource('dynamodb')
    ses = boto3.client('ses')
    
    from_email = os.environ['from_email']
    to_email = ['ashkoli1988@gmail.com']  # Als Liste von E-Mail-Adressen definieren
    
    # Die Tabelle auswählen, in der der Text gespeichert werden soll
    table = dynamodb.Table('user-text-profile')
    
    try:
        # Eintrag in die DynamoDB-Tabelle einfügen
        response = table.put_item(
            Item={
                'id': entry_id,  # Aktuelle Datum- und Uhrzeit als ID für den Eintrag
                'text': user_text
            }
        )
        
        # Erfolgsmeldung zurückgeben
        response_body = 'Text erfolgreich in DynamoDB gespeichert.'
        
        # E-Mail-Nachricht für Benachrichtigung vorbereiten
        subject = 'Neuer Text eingereicht'
        body = f'Ein neuer Text wurde eingereicht:\n\n{user_text}'
        sender = 'arn:aws:ses:eu-central-1:869730637141:identity/ashkoli1988@gmail.com'  # ARN der verifizierten Identität
        
        # E-Mail-Nachricht senden
        ses.send_email(
            Source=from_email,
            Destination={'ToAddresses': to_email},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}}
            }
        )
        
        # Erfolgsmeldung zurückgeben
        return {
            'statusCode': 200,
            'headers': headers,
            'body': response_body
        }
    except Exception as e:
        # Fehlermeldung zurückgeben, falls etwas schief geht
        return {
            'statusCode': 500,
            'body': f'Fehler beim Speichern des Textes in DynamoDB oder beim Senden der E-Mail: {str(e)}'
        }
