from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import RegisterForm


@login_required
def profile_view(request: HttpRequest):
    orders = request.user.orders.all()
    for order in orders:
        for item in order.items.all():
            item.total_price = item.quantity * item.price
    return render(request, 'profile.html', {'orders': orders})


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)