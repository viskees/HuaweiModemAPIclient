import huaweisms.api.user
import huaweisms.api.wlan
import huaweisms.api.sms

ctx = huaweisms.api.user.quick_login('admin', 'raadjenooit', modem_host='192.168.177.254')
# print(ctx)

# haal het totaal aantal SMS berichten op in alle boxen
aantal_sms = huaweisms.api.sms.sms_count(ctx)

# bepaal het aantal berichten in de inbox en converteer naar integer
aantal_sms_int = int(aantal_sms['response']['LocalInbox'])

# bepaal of er SMS berichten zijn ontvangen en als er een bericht is, verwijder dit bericht en stuur een 1 GB Booster SMS naar Tele2

if aantal_sms_int > 0:

    # SMS ontvangen sinds de laatste controle; we nemen even aan dat dit een bericht betreft dat we tegen de 5 GB zitten
    # dus we moeten de bundelbooster inschakelen en de SMS inbox leegmaken

    # maak de inbox leeg en verwijder alle SMS berichten
    while aantal_sms_int > 0:

        # bepaal SMS index en verwijder het bericht op basis van deze index
        sms = huaweisms.api.sms.get_sms(ctx, 1, 1)
        index = sms['response']['Messages']['Message'][0]['Index']

        # verwijder SMS op basis van index
        #print('SMS met index: {0} '.format(index))
        huaweisms.api.sms.delete_sms(ctx, index)

        # aantal SMS-jes met 1 verlagen
        aantal_sms_int -= 1


    #alle SMS-jes zijn verwijderd, activeer de bundelbooster
    huaweisms.api.sms.send_sms(ctx, '1280', 'NOG 1GB')

else:
    # niets te doen
    #print('nothing to do')
    exit()