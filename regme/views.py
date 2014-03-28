from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import UserCreationForm, UserActivationForm


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('registered')

    def form_valid(self, form):
        form.save()
        return FormView.form_valid(self, form)

register = RegisterView.as_view()


class RegisteredView(TemplateView):
    template_name = 'registration/registered.html'

registered = RegisteredView.as_view()


class ActivateView(FormView):
    template_name = 'registration/activate.html'
    form_class = UserActivationForm
    success_url = reverse_lazy('activated')

    def form_valid(self, form):
        form.save()
        return FormView.form_valid(self, form)

    def get(self, request, *args, **kwargs):
        form = self.get_form_class()(kwargs)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def post(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)

activate = ActivateView.as_view()


class ActivatedView(TemplateView):
    template_name = 'registration/activated.html'

activated = ActivatedView.as_view()
