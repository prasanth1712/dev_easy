from django import forms
import pandas as pd
class fileupload(forms.Form):
    file = forms.FileField(required=False)


def load_file(model,cols,file):
    data = pd.read_excel(file)
    data.columns = cols
    print('2')
    data = data.to_dict('records')
    return data