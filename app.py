import flask 
from flask import Flask, render_template
import time
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.transform import dodge
from math import pi 
import Berechnungen as calc


app = Flask(__name__)

@app.route('/home')
@app.route('/')
def index():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True) 

Lager=['Rohstofflager', 'Zwischenlager 1', 'Zwischenlager 2', 'Fertigwarenlager']
stationen=['Rohstofflager', 'Drehmaschine', 'Zwischenlager 1', 'Fräsmaschine', 'Zwischenlager 2', 'Schleifmaschine', 'Fertigwarenlager']
Produktnummern=['55101', '55102', '55103', '55104'] 


@app.route('/zeitübersicht')
def zeitübersicht():
    data = calc.liegz()
    source = ColumnDataSource(data=data)
    fig = figure(x_range=stationen, plot_height=750, x_axis_label='Bearbeitungsstation', y_axis_label='Zeit [in min]', )
    fig.vbar(x=dodge('stationen', -0.3, range=fig.x_range), width=0.1, top='55101', source=source, color='skyblue', legend_label="Welle 1")
    fig.vbar(x=dodge('stationen', -0.1, range=fig.x_range), width=0.1, top='55102', source=source, color='dodgerblue', legend_label="Welle 2")
    fig.vbar(x=dodge('stationen', 0.1, range=fig.x_range), width=0.1, top='55103', source=source, color='royalblue', legend_label="Welle 3")
    fig.vbar(x=dodge('stationen', 0.3, range=fig.x_range), width=0.1, top='55104', source=source, color='navy', legend_label="Welle 4")
    fig.x_range.range_padding = 0.1 
    fig.xgrid.grid_line_color = None
    fig.legend.location = "top_left"
    fig.legend.orientation = "horizontal"
    fig.xaxis.major_label_orientation = pi/4
  
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(fig)
    html = render_template(
        'zeitübersicht.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return html

@app.route('/About')
def about():
    
    return render_template("About.html")
    

@app.route('/wertschöpfung')
def wertschöpfung():
    wert = calc.wertsch()
    fig = figure(x_range=Produktnummern, plot_width=600, plot_height=600, x_axis_label='Produktnummer', y_axis_label='aktueller Wert [€]', )
    fig.vbar(
        x=Produktnummern,
        width=0.5,
        bottom=0,
        top=wert,
        color='navy'
    )

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(fig)
    html = render_template(
        'wertschöpfung.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return html 


@app.route('/kapitalkosten')
def kapitalkosten():
    kapitalbindungskosten=calc.lagk() 
    fig = figure(x_range=Lager, plot_width=600, plot_height=600, x_axis_label='Lager', y_axis_label='Kosten [ct]', )
    fig.vbar(
        x=Lager,
        width=0.5,
        bottom=0,
        top=kapitalbindungskosten,
        color='navy'
    )

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(fig)
    html = render_template(
        'kapitalkosten.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return html 
