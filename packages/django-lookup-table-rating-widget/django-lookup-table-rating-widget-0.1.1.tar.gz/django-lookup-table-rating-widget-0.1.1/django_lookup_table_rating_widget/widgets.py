from django.forms import NumberInput
from django.utils.translation import ugettext_lazy as _


class DjangoLookupTableRatingWidget(NumberInput):
    template_name = "django-lookup-table-rating-widget/django-lookup-table-rating-widget.html"

    class Media:
        css = {
            "all": [
                "django-lookup-table-rating-widget/css/django-lookup-table-rating-widget.css",
            ]
        }
        js = [
            "admin/js/vendor/jquery/jquery.js",
            "django-lookup-table-rating-widget/js/django-lookup-table-rating-widget.js",
            "admin/js/jquery.init.js"
        ]

    def __init__(self,
            scores, 
            attrs=None,
            allow_input=False,
            field_label_in_table=True,
            weight=None,
            field_label=_("Item"),
            final_score_label=_("Score"),
            scores_label=_("Rating Buttons"),
            rules_label=_("Rule"),
            weight_label=_("Weight")):
        # __init__ start...
        self.allow_input = allow_input
        self.weight = weight
        self.scores = scores
        self.field_label = field_label
        self.final_score_label = final_score_label
        self.scores_label = scores_label
        self.rules_label = rules_label
        self.weight_label = weight_label
        self.field_label_in_table = field_label_in_table
        min_value, max_value = self.get_min_max_value()
        attrs = attrs or {}
        attrs["class"] = attrs.get("class", "") + " django-lookup-table-rating-widget-input"
        attrs["min"] = min_value
        attrs["max"] = max_value
        if not self.allow_input:
            attrs["readonly"] = "readonly"
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["weight"] = self.weight
        context["rows"] = len(self.scores)
        context["first_score_line"] = self.scores[0]
        context["other_score_lines"] = self.scores[1:]
        context["field_label"] = self.field_label
        context["final_score_label"] = self.final_score_label
        context["scores_label"] = self.scores_label
        context["rules_label"] = self.rules_label
        context["weight_label"] = self.weight_label
        context["field_label_in_table"] = self.field_label_in_table
        return context

    def get_min_max_value(self):
        min_value = 2**64
        max_value = -2**64
        for score_line in self.scores:
            for score in score_line["scores"]:
                min_value = min(min_value, score)
                max_value = max(max_value, score)
        return min_value, max_value
