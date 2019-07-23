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
# 1 bericht in de Inbox is oke, want dit is waarschijnlijk de reply op het booster request

# definieer SMS contentberichten die mogen worden verwijderd
sms_content_del_oke = ['Gelukt! Je BundelBooster \nvan 1GB is geactiveerd. \nWe houden contact. \nTele2', 'Test', 'Test1']

if aantal_sms_int > 1:

    # SMS ontvangen sinds de laatste controle; we nemen even aan dat dit een bericht betreft dat we tegen de 5 GB zitten
    # dus we moeten de bundelbooster inschakelen en de SMS inbox leegmaken

    # maak de inbox leeg en verwijder alle SMS berichten
    while aantal_sms_int > 0:

        # bepaal SMS index en verwijder het bericht op basis van deze index als deze voorkomt in sms_content_del_oke
        sms = huaweisms.api.sms.get_sms(ctx, 1, 1)
        index = sms['response']['Messages']['Message'][0]['Index']

        #bepaal op basis van de content van de SMS of deze verwijderd mag worden
        sms_verwijderen = 0

        for sms_content in sms_content_del_oke:

            if sms_content == sms['response']['Messages']['Message'][0]['Content']:
                # SMS mag worden verwijderd
                sms_verwijderen = 1
            else:
                continue

        if sms_verwijderen == 1:
            #bekende SMS; deze mag worden verwijderd op basis van index
            print('Deze SMS mag worden verwijderd: ' + sms['response']['Messages']['Message'][0]['Content'])
            #print('SMS met index: {0} '.format(index))
            huaweisms.api.sms.delete_sms(ctx, index)

            # aantal SMS-jes met 1 verlagen
            aantal_sms_int -= 1

        else:
            # content van de SMS komt niet voor in de lijst met bekende SMS berichten, dus mag niet worden verwijderd
            # bundelbooster niet versturen
            # SMS content naar mobiel van Kees versturen
            huaweisms.api.sms.send_sms(ctx, '0612156835', 'Deze SMS heb ik van Tele2 ontvangen: ' + sms['response']['Messages']['Message'][0]['Content'])
            exit()

    #alle SMS-jes zijn verwijderd, activeer de bundelbooster
    huaweisms.api.sms.send_sms(ctx, '1280', 'NOG 1GB')

else:
    # niets te doen
    #print('nothing to do')
    exit()