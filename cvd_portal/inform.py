from cvd_portal.models import Patient, PatientData, Notifications
from cvd_portal.fcm import send_message
import datetime


change_observed = [False, False, False, False]


def gen_message(co, p):
    gen_msg = False
    for c in co:
        if c is True:
            gen_msg = True
    if gen_msg is False:
        return None
    else:
        message = "Patient named '" + p.name + "' suffered drastic changes in "
        if(change_observed[0] is True):
            message = message + "'weight' "
        if(change_observed[1] is True):
            message = message + "'heart-rate' "
        if(change_observed[2] is True):
            message = message + "'BP-systolic' "
        if(change_observed[3] is True):
            message = message + "'BP-diastolic' "
        message = message + "in recent few days."
        return message


def get_patient(pk):
    return Patient.objects.get(pk=pk)


def check(request):
    timestamp_to = datetime.datetime.now() - datetime.timedelta(days=8)
    p = get_patient(request.data['patient'])
    pd = PatientData.objects.filter(
        patient_id=request.data['patient'],
        time_stamp__gte=timestamp_to).order_by('-time_stamp')
    if(len(pd) == 0):
        return
    else:
        wt = int(request.data['weight'])
        hr = int(request.data['heart_rate'])
        sys = int(request.data['systolic'])
        dia = int(request.data['diastolic'])
        for d in pd:
            if(abs(d.weight-wt) >= 1):
                # print('wt')
                change_observed[0] = True
            if(abs(abs(d.heart_rate) - hr)/hr >= 0.1):
                # print('hr')
                change_observed[1] = True
            if(abs(abs(d.systolic) - sys)/sys >= 0.1):
                # print('sys')
                change_observed[2] = True
            if(abs(abs(d.diastolic) - dia)/dia >= 0.1):
                # print('dia')
                change_observed[3] = True
        doc_message = gen_message(change_observed, p)
        if(doc_message is None):
            return
        else:
            d_id = p.doctor.device.device_id
            p_id = p.device.device_id
            send_message(d_id, None, doc_message)
            patient_message = "Please visit nearest OPD"
            send_message(p_id, None, patient_message)
            Notifications(text=doc_message, doctor=p.doctor).save()
            Notifications(text=patient_message, patient=p).save()
