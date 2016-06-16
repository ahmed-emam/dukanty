from pyfcm import FCMNotification

# PyFCM uses HTTP for sending messages
# Full API: https://github.com/olucurious/PyFCM/blob/master/pyfcm/fcm.py
# Send to single device
push_service = FCMNotification(api_key="<server_key>")

registration_id = "<device_id>"
message_title = "Dukanty"
message_body = "Your purchase is ready for pickup"
result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

# Send to multiple devices by passing a list of ids
# registration_ids = ["<device registration_id 1>", "<device registration_id 2>", ...]
# message_title = "Dukanty"
# message_body = "Your purchase is ready for pickup"
# result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)

print result