

def legend(species_colors_dict,dragable=True):

    
    legend_temp=''
    
    
    for species in species_colors_dict.keys():
        legend_temp = legend_temp + f"<li><span style='background: {species_colors_dict[species]}; opacity: 0.75;'></span>{species}</li>"
        
    
    legend_body = f"""  
    <!doctype html>
    <html lang="en">
    <body>
    <div id='maplegend' class='maplegend' 
        style='position: absolute; z-index: 9999; background-color: rgba(255, 255, 255, 0.7);
         border-radius: 8px; padding: 10px; font-size: 11px; right: 10px; bottom: 35px; '>     
    <div class='legend-scale'>
      <ul class='legend-labels'>
          <img src="https://www.elskenecologie.nl/wp-content/themes/elsken/assets/img/logo-mobile.png" style="background:green; width:30px;height:23px;">
          <li>------------</li>
        <li><strong>Sorten</strong></li>

        {legend_temp}

        <li><strong>Functie</strong></li>
        <li><span class="fa fa-map-marker" style="color:grey" opacity: 0.75;'></span>Waarneming</li>
        <li><span class="fa fa-object-ungroup" style="color:grey" opacity: 0.75;'></span>Gebied</li>
      </ul> 
    </body>
    </html>
    """
    
    
    legend_style = """<style type='text/css'>
      .maplegend .legend-scale ul {margin: 0; padding: 0; color: #0f0f0f;}
      .maplegend .legend-scale ul li {list-style: none; line-height: 18px; margin-bottom: 1.5px;}
      .maplegend ul.legend-labels li span {float: left; height: 16px; width: 16px; margin-right: 4.5px;}
    </style>
    
    {% endmacro %}
    """
    legend_dragable = """{% macro html(this, kwargs) %}
        <!doctype html>
        <html lang="en">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>jQuery UI Draggable - Default functionality</title>
          <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
        
          <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
          <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
          
          <script>
          $( function() {
            $( "#maplegend" ).draggable({
                            start: function (event, ui) {
                                $(this).css({
                                    right: "auto",
                                    top: "auto",
                                    bottom: "auto"
                                });
                            }
                        });
        });
        
          </script>
        </head>
        """
    
    legend_normal = "{% macro html(this, kwargs) %}"

    if dragable == True:
        legend = legend_dragable + legend_body + legend_style
    else:
        legend = legend_normal + legend_body + legend_style

    return legend
