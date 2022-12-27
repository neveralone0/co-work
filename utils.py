from kavenegar import *


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('33754361327133504272566C31703870745164656A6C4E5879483030676E377449742F43556836443339303D')
        params = {'sender': '1000596446',
                  'receptor': '09127637509',
                  'message': f'{code}'}
        response = api.sms_send(params)
        print('=R=========')
        print(response)
    except APIException as e:
        print('=1=========')
        print(e)
    except HTTPException as e:
        print('=2=========')
        print(e)
    pass
