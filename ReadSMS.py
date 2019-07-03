import huaweisms.api.user
import huaweisms.api.wlan
import huaweisms.api.sms

ctx = huaweisms.api.user.quick_login('admin', 'raadjenooit', modem_host='192.168.177.254')
#print(ctx)

#haal het totaal aantal SMS berichten op in alle boxen
aantal_sms = huaweisms.api.sms.sms_count(ctx)

#bepaal het aantal berichten in de inbox en converteer naar integer
aantal_sms_int = int(aantal_sms['response']['LocalInbox'])
print('aantal SMS-jes in de inbox: {0}'.format(aantal_sms_int))

#print de SMS berichten
print(huaweisms.api.sms.get_sms(ctx, 1, 1))