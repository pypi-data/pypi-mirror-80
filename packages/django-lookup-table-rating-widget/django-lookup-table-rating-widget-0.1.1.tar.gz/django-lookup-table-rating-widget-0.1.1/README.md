# django-lookup-table-rating-widget

A django rating widget with a lookup-table for score-making rules.

## Install

```shell
pip install django-lookup-table-rating-widget
```

## Usage

**pro/settings.py**

**Note:**

- We used template of django-lookup-table-rating-widget, so we NEED add django_lookup_table_rating_widget in INSTALLED_APPS.

```python
INSTALLED_APPS = [
    ...
    'django_lookup_table_rating_widget',
    ...
]
```

**app/admin.py**

```python

from django.contrib import admin
from django.utils.lorem_ipsum import sentence
from django_lookup_table_rating_widget.widgets import DjangoLookupTableRatingWidget
from django import forms
from .models import Book

s1_scores = [
    {
        "scores": [1, 2],
        "rule": "<b>Bad</b>. " + sentence(),
    },{
        "scores": [3, 4],
        "rule": "<b>Not bad</b>. " + sentence(),
    },{
        "scores": [5, 6],
        "rule": "<b>Good</b>. " + sentence(),
    },{
        "scores": [7, 8],
        "rule": "<b>Very Good</b>." + sentence(),
    },{
        "scores": [9, 10],
        "rule": "<b>Excellent</b>." + sentence(),
    }
]

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = []
        widgets = {
            "s1": DjangoLookupTableRatingWidget(s1_scores, field_label_in_table=False, weight=15),
            "s2": DjangoLookupTableRatingWidget(s1_scores, allow_input=True),
            "s3": DjangoLookupTableRatingWidget(s1_scores),
            "s4": DjangoLookupTableRatingWidget(s1_scores),
        }

class BookAdmin(admin.ModelAdmin):
    form = BookForm
    list_display = ["title"]

    fieldsets = [
        (None, {
            "fields": ["title"]
        }),
        ("Score 1 & 2", {
            "fields": ["s1", "s2"],
        }),
        ("Score 3 & 4", {
            "fields": ["s3", "s4"],
        })
    ]

admin.site.register(Book, BookAdmin)

```

## Widget Init Parameters

- `scores`: required.
    - It's a list of map. The map always contains `scores` and `rule` item. `scores` is a list of rating buttons, and the `rule` is a string of rule description. HTML `rule` is accepted.
- `allow_input`: optional, default to False.
    - If allow_input=True, the final score input is allowed to input.
    - If allow_input=False, the final score input is readonly.
- `field_label_in_table`: optional, default True.
    - If field_label_in_table=True, we use jquery to move field's label and help into the table.
    - If field_label_in_table=False, we keep the field's label and help at thire original position.
- `weight`: optional, default None.
    - weight means the field weight in full rating form.
    - If not provides, we will remove the weight column.
- `field_label`: optional, default to _("Item").
- `final_score_label`: optional, default to _("Score").
- `scores_label`: optional, default to _("Rating Buttons").
- `rules_label`: optional, default to _("Rule").
- `weight_label`: _("Weight").
    - All lables are used to render the rating table header.

## Releases

### v0.1.1 2020/09/25

- No depends on django_static_jquery3.
- Add license file.

### v0.1.0 2020/03/18

- First release.

