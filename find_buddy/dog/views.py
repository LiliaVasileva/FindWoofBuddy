from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from find_buddy.dog.forms import DogCreateForm, DogEditForm, DogDeleteForm
from find_buddy.dog.models import Dog


class DogsTemplateView(TemplateView):
    template_name = 'dog/profile-dogs-page.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        dogs = list(Dog.objects.filter(user=self.request.user))

        context.update({
            'dogs': dogs,
        })
        return context


class DogCreateView(CreateView):
    form_class = DogCreateForm
    template_name = 'dog/dog-create-page.html'

    def get_success_url(self):
        return reverse_lazy('dog details')

    # this way we define the pet to be created for the currant user
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class DogEditView(UpdateView):
    model = Dog
    form_class = DogEditForm
    template_name = 'dog/dog-edit-page.html'

    def get_success_url(self):
        return reverse_lazy('dog details')


# class DogDeleteView(DeleteView):
#     form_class = DogDeleteForm
#     template_name = 'dog/dog-delete-page.html'
#
#     def get_success_url(self):
#         return reverse_lazy('dog details')


def dog_delete_view(request, pk):
    dog = Dog.objects.get(pk=pk)
    if request.method == 'POST':
        form = DogDeleteForm(request.POST, request.FILES, instance=dog)
        if form.is_valid():
            form.save()
            return redirect('dog details')
    else:
        form = DogDeleteForm(instance=dog)
    context = {
        'form': form,
        'dog': dog,
    }
    return render(request, 'dog/dog-delete-page.html', context)
