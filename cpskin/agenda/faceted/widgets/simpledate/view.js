/* SimpleDate Widget
*/
Faceted.SimpleDateWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.widget.show();
  this.title = jQuery('legend', this.widget).html();

  this.date = jQuery('input[name=date]', this.widget);
  this.selected = [];
  this.dateFormat = jQuery('input[name=dateFormat]', this.widget).val();
  this.language = jQuery('input[name=language]', this.widget).val();

  var date = this.date.val();
  if(date){
    this.selected = this.date;
    Faceted.Query[this.wid] = date;
  }

  var js_widget = this;
  this.date.datepicker({
    changeMonth: true,
    changeYear: true,
    dateFormat: this.dateFormat,
    onSelect: function(date, cal){
      js_widget.select_change(js_widget.date);
    }
  });

  /**
   * Make sure we can reset the date by manually deleting the date and
   * call the 'onChange' event (click outside the changed field).
   */
  this.date.change(function(){
    var date = js_widget.date.val();

    if(!date){
      js_widget.reset();
      Faceted.Form.do_query(js_widget.wid, '');
    }
  });

  // Handle clicks
  jQuery('form', this.widget).submit(function(){
    return false;
  });

  // Bind events
  jQuery(Faceted.Events).bind(Faceted.Events.QUERY_CHANGED, function(evt){
    js_widget.synchronize();
  });
  jQuery(Faceted.Events).bind(Faceted.Events.RESET, function(evt){
    js_widget.reset();
  });
};
Faceted.SimpleDateWidget.prototype = {
  select_change: function(element){
    this.do_query(element);
  },

  do_query: function(element){
    var value = this.date.val();

    /**
     * Make sure we can reset the date by manually deleting the date and
     * running the query (press enter).
     */
    if(!value){
      this.reset();
      Faceted.Form.do_query(this.wid, '');
    }

    this.selected = this.date;
    Faceted.Form.clear_errors(this.wid + '_errors', []);
    Faceted.Form.do_query(this.wid, value);
  },

  reset: function(){
    this.selected = '';
    this.date.val('');
  },

  synchronize: function(){
    var value = Faceted.Query[this.wid];
    if(!value){
      this.reset();
      return false;
    }

    var date = $.datepicker.parseDate(this.dateFormat, value);
    // Invalid date
    if(!date.getFullYear()){
      this.reset();
      return false;
    }

    // Set input
    this.date.val(value);
    this.selected = this.date;
  },

  criteria: function(){
    var html = [];
    var title = this.criteria_title();
    var body = this.criteria_body();
    if(title){
      html.push(title);
    }
    if(body){
      html.push(body);
    }
    return html;
  },

  criteria_title: function(){
    if(!this.selected){
      return '';
    }

    var link = jQuery('<a href="#">[X]</a>');
    link.attr('id', 'criteria_' + this.wid);
    link.attr('title', 'Remove ' + this.title + ' filters');
    var widget = this;
    link.click(function(evt){
      widget.criteria_remove();
      return false;
    });

    var html = jQuery('<dt>');
    html.attr('id', 'criteria_' + this.wid + '_label');
    html.append(link);
    html.append('<span>' + this.title + '</span>');
    return html;
  },

  criteria_body: function(){
    if(!this.selected){
      return '';
    }

    var widget = this;
    var html = jQuery('<dd>');
    html.attr('id', 'criteria_' + this.wid + '_entries');
    var date = this.date.val();
    date = $.datepicker.parseDate(this.dateFormat, date);

    var label = this.criteria_label(date);
    var link = jQuery('<a href="#">[X]</a>');

    link.attr('id', 'criteria_' + this.wid + '_');
    link.attr('title', 'Remove ' + label + ' filter');
    link.click(function(evt){
      widget.criteria_remove();
      return false;
    });
    var span = jQuery('<span class="faceted-simpledate-criterion">');
    span.append(link);
    jQuery('<span>').text(label).appendTo(span);
    html.append(span);
    return html;
  },

  criteria_label: function(date){
    var options = {weekday: "short",
                   year: "numeric",
                   month: "short",
                   day: "numeric"};
    var date_label = date.toLocaleDateString(this.language, options);
    return date_label;
  },

  criteria_remove: function(){
    this.reset();
    return Faceted.Form.do_query(this.wid, '');
  }
};

Faceted.initializeSimpleDateWidget = function(evt){
  jQuery('div.faceted-simpledate-widget').each(function(){
    var wid = jQuery(this).attr('id');
    wid = wid.split('_')[0];
    Faceted.Widgets[wid] = new Faceted.SimpleDateWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(Faceted.Events).bind(
    Faceted.Events.INITIALIZE,
    Faceted.initializeSimpleDateWidget);
});
