from django import forms

class CrudyForm(forms.ModelForm):

    class Meta:
        model = None
        fields = []
        readonly_fields = ()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in self.Meta.readonly_fields:
                field.widget.attrs['disabled'] = 'true'
                field.required = False

    def clean(self):
        cleaned_data = super().clean()
        for field in self.Meta.readonly_fields:
            cleaned_data[field] = getattr(self.instance, field)
        return cleaned_data
