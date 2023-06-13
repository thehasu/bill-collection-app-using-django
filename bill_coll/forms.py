from fileinput import FileInput

from django import forms

from bill_coll import models


class CityForm(forms.ModelForm):
    class Meta:
        model = models.City
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AreaForm(forms.ModelForm):
    class Meta:
        model = models.Area
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
        }


class PackageForm(forms.ModelForm):
    class Meta:
        model = models.Package
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'numberofchannels': forms.TextInput(attrs={'class': 'form-control'}),
            'numberofHDchannels': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'})
        }


class CollectionForm(forms.ModelForm):
    class Meta:
        model = models.Collection
        fields = ['user_id', 'package', 'billMonth', 'amount', 'billDate']
        widgets = {
            'user_id': forms.Select(attrs={'class': 'form-control'}),
            'package': forms.Select(attrs={'class': 'form-control'}),
            'billMonth': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'billDate': forms.DateInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'user_id': 'User',
            'package': 'Package',
            'billMonth': 'Bill Month',
            'amount': 'Bill Amount',
            'billDate': 'Bill Date (mm-dd-yyyy)'
        }


class UpdateProfile(forms.ModelForm):
    class Meta:
        model = models.Profile
        # fields = "__all__"
        fields = ['fullname', 'photo', 'city', 'area', 'package', 'address']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'package': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'area': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'photo': 'Select a new photo'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['area'].queryset = models.Area.objects.none()
        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['area'].queryset = models.Area.objects.filter(
                    city_id=city_id).order_by('name')

            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['area'].queryset = self.instance.city.area_set.order_by(
                'name')
