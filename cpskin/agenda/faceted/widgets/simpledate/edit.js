FacetedEdit.SimpleDateWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');

  this.date = jQuery('input[name=date]', this.widget);
  this.dateFormat = jQuery('input[name=dateFormat]', this.widget).val();

  var js_widget = this;
  this.date.datepicker({
    changeMonth: true,
    changeYear: true,
    dateFormat: this.dateFormat,
    onSelect: function(date, cal){
      js_widget.set_default(date);
    }
  });

  this.date.change(function(){
    js_widget.set_default(this);
  });

};

FacetedEdit.SimpleDateWidget.prototype = {
  set_default: function(element){
    var date = this.date.val();
    if(!date){
      return;
    }
    var value = $.datepicker.parseDate(this.dateFormat, date);
    var query = {};
    query.redirect = '';
    query.updateCriterion_button = 'Save';
    query.cid = this.wid;
    query[this.wid + '_default'] = value;

    jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_START, {msg: 'Saving ...'});
    jQuery.post(FacetedEdit.BASEURL + '@@faceted_configure', query, function(data){
      jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_STOP, {msg: data});
    });
  }
};

FacetedEdit.initializeSimpleDateWidget = function(){
  jQuery('div.faceted-simpledate-widget').each(function(){
      var wid = jQuery(this).attr('id');
      wid = wid.split('_')[0];
      FacetedEdit.Widgets[wid] = new FacetedEdit.SimpleDateWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(FacetedEdit.Events).bind(
    FacetedEdit.Events.INITIALIZE_WIDGETS,
    FacetedEdit.initializeSimpleDateWidget);
});
