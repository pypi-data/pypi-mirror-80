;!(function($){
    $.fn.django_lookup_table_rating_widget = function(){
        return this.each(function(){
            var table = $(this);
            var label_slot = table.find(".django-lookup-table-rating-widget-label");
            var help_slot = table.find(".django-lookup-table-rating-widget-help");
            var final_score_slot = table.find(".django-lookup-table-rating-widget-final-score");
            var final_score_input = table.find(".django-lookup-table-rating-widget-input");
            var set_selected_class = function(){
                var init_value = final_score_input.val();
                table.find(".django-lookup-table-rating-widget-score").removeClass("django-lookup-table-rating-widget-selected-score");
                table.find(".django-lookup-table-rating-widget-score").each(function(index, element){
                    var a = $(element).attr("data-value");
                    if(a == init_value){
                        $(element).addClass("django-lookup-table-rating-widget-selected-score");
                    }
                });
            };
            var check_value_limit = function(){
                var value = parseInt(final_score_input.val());
                var min_value = parseInt(final_score_input.attr("min"));
                var max_value = parseInt(final_score_input.attr("max"));
                if(isNaN(value)){
                    final_score_input.val("");
                }
                if(value < min_value){
                    final_score_input.val(min_value);
                }
                if(value > max_value){
                    final_score_input.val(max_value);
                }
            };
            table.parents(".form-row").find(".errorlist").appendTo(final_score_slot);
            table.prevAll("label").appendTo(label_slot);
            if(table.nextAll(".help").length > 0){
                table.nextAll(".help").appendTo(help_slot);
            }else{
                $('<div class="help"></div>').appendTo(help_slot);
            }
            table.find(".django-lookup-table-rating-widget-score").click(function(){
                var value = $(this).attr("data-value");
                final_score_input.val(value);
                set_selected_class();
            });
            final_score_input.change(function(){
                check_value_limit();
                set_selected_class();
            });
            set_selected_class();
        });
    };

    $(document).ready(function(){
        $(".django-lookup-table-rating-widget-field-label-in-table").django_lookup_table_rating_widget();
    });
})(jQuery);