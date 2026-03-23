from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not email or not message:
            messages.error(request, 'All fields are required.')
            return redirect('contact')

        # Save to database
        ContactMessage.objects.create(name=name, email=email, message=message)

        try:
            # ✅ SEND MAIL TO YOU (ADMIN)
            send_mail(
                subject=f'New Contact Message from {name}',
                message=f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['anmolbajpai58@gmail.com'],  # ✅ YOUR EMAIL
                fail_silently=False,
            )

            # ✅ SEND CONFIRMATION TO USER
            send_mail(
                subject='Thank you for reaching out!',
                message=(
                    f'Hi {name},\n\n'
                    'Thank you for your message! I have received it and will get back to you shortly.\n\n'
                    'Best regards,\nAnmol Bajpai'
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

        except Exception as e:
            print("EMAIL ERROR:", e)

        messages.success(request, 'Your message has been sent!')
        return redirect('contact')

    return render(request, 'contact.html')