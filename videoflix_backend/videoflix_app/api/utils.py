from django.http import Http404 


def get_or_404(model,pk):

    try:
        pk = int(pk)
        instance = model.objects.get(pk=pk)
        return instance
    except ValueError:
        raise ValueError("The ID must be an integer")
    except model.DoesNotExist:
        raise Http404("Model does not exit")
