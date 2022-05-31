from django.core.mail import send_mail
from carrent import settings


def calculate_cost(start_date, return_date, base_price, car_rating):
    """ Takes 2 datetime.date objects base price and a multiplier (rating) and returns total cost (int)

        Mostly for order cost calculation
    """
    nr_of_days = return_date - start_date
    price_per_day = int(base_price * car_rating)
    return nr_of_days.days * price_per_day


def send_order_confirmation_mail(recipents_email_list, order):
    host_phone_number = 111222333
    subject = f"Potwierdzenie zamówienia samochodu {order.car}"
    message = f"Witaj {order.client.first_name} {order.client.last_name} \n" \
              f"Dziękujemy za złożenie zamówienia na wynajem auta {order.car} \n" \
              f"Rozpoczęcie najmu: {order.start_date} \n" \
              f"Zwrot samochodu: {order.return_date} \n" \
              f"\n" \
              f"W razie pytań lub problemów prosimy o kontakt pod {host_phone_number}"

    senders_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, senders_email, recipents_email_list, fail_silently=True)
