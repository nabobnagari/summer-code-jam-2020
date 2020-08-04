from django.shortcuts import render


# Create your views here.
def homepage(request):
    """ Views to render the homepage. """

    return render(request, "home.html")

def about_us(request):
    """ Views to render the About Us page. """
    template = "about.html"
    context = about_us
    return render(request, template)
