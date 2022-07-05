import io
from datetime import date

from django.core.mail import EmailMessage
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from carrent import settings


def calculate_cost(start_date, return_date, base_price, car_rating, user_discount, time_discount_object, car_discount=0):
    """ Takes 2 datetime.date objects base price and a multiplier (rating) and returns total cost (int)

        Mostly for order cost calculation
    """
    nr_of_days = return_date - start_date
    if 14 <= nr_of_days.days < 30:
        time_discount = time_discount_object.two_weeks_discount
    elif nr_of_days.days >= 30:
        time_discount = time_discount_object.month_discount
    else:
        time_discount = 0

    #price_per_day = int(base_price * car_rating)
    return nr_of_days.days * base_price * (car_rating - (car_rating * (car_discount / 100))) * (1 - (user_discount / 100)) * (1 - (time_discount / 100))


def send_order_confirmation_mail(recipents_email_list, order):
    host_phone_number = 111222333
    subject = f"Potwierdzenie zamowienia samochodu {order.car}"
    message = f"Witaj {order.client.first_name} {order.client.last_name} \n" \
              f"Dziekujemy za zlozenie zamowienia na wynajem auta {order.car} \n" \
              f"Rozpoczecie najmu: {order.start_date} \n" \
              f"Zwrot samochodu: {order.return_date} \n" \
              f"\n" \
              f"W razie pytan lub problemow prosimy o kontakt pod {host_phone_number}"

    senders_email = settings.EMAIL_HOST_USER
    attachment_pdf = create_pdf_from_order(message, order)
    email_temp = EmailMessage(subject, message, senders_email, recipents_email_list)
    email_temp.attach(f'order_detail_{order.id}.pdf', attachment_pdf, 'application/pdf')
    email_temp.send(fail_silently=True)


def create_pdf_from_order(message, order):
    buffer = io.BytesIO()
    temp_pdf = canvas.Canvas(buffer, pagesize=A4)

    message_lines = message.split('\n')
    base_y = 800
    temp_pdf.setFont('Times-Roman', 16)
    image_link_root = str(settings.BASE_DIR)
    image_link = image_link_root + order.car.car_image.url


    for line in message_lines:
        temp_pdf.drawString(30, base_y, line)
        base_y -= 15

    base_y -= 250
    temp_pdf.drawImage(image_link, 150, base_y, 320, 240, preserveAspectRatio=True)
    temp_pdf.drawString(30, 30, f'generated on {date.today()} by CarRental Bagniaki incorporated')
    temp_pdf.setTitle(f"Order - {order.id}")
    temp_pdf.showPage()
    temp_pdf.save()
    buffer.seek(0)
    pdf_file = buffer.getvalue()
    buffer.close()
    return pdf_file

