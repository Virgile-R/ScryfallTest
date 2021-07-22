from django import template
from django.template import Template, Context
from django.conf import settings
from django.shortcuts import render
from django.template.loader import render_to_string

templates = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["./html/"],
    }
]
settings.configure(templates)




def my_view(request):
    as_file = request.GET.get('as_file')
    t = Template('template.html')
    c = Context({"name": 'monstre test'} )
    if as_file:
        content = render_to_string(t, c)
        with open('./html/test.html', 'w') as test_file:
            test_file.write(content)

    return render(t,c)
my_view('GET')
class DndTemplate:
    def __init__(self, model, css) -> None:
        pass



    def populate_template(model, css):
        pass

    