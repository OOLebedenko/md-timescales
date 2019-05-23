from __future__ import print_function
from ipywidgets import interact, interactive, fixed, interact_manual, Textarea
from ipywidgets import Button, GridBox, Layout, ButtonStyle, Box, Label, Dropdown, FloatText, HBox, VBox
import ipywidgets as widgets
from IPython.display import display_html, clear_output
from ipywidgets import IntSlider, Output

from IPython.display import display
import os
import pandas as pd
import numpy as np
# %matplotlib inline

from matplotlib import pyplot as plt

from io import BytesIO
import base64
import glob

import plot_for_notebook
import plot_msd_for_notebook
import plot_overall_thumbling_for_notebook

class BoxFields:
    def __init__(self, protein_value):
        
        

        self.numbers_value = 1
        self.order_exp_value = 2
        self.func = None 
        self.protein_value = protein_value
        self.ansamble_value = 'NVE'
        self.water_model_value ='spce'
        self.analysis_type_value = 'autocorrelation_NH'
        
        self.numbers = widgets.IntText(
                        value = 1,
                        description="numbers:")
        
        self.order_exp = widgets.Dropdown(
                                options=[2, 3, 4],
                                value=2,
                                description='order:',
                                disabled=False,)
        self.form_item_layout = Layout(
                                        width= '99%',
                                        align_items='stretch'
                                    )
        self.form_item_layout_box = Layout(
                                        width= '50%',
                                        align_items='stretch',
                                    )
        self.water_model =  widgets.Dropdown(
        options=['spce', 'tip3p', 'tip4p-ew', 'tip4p-d'],
        value='spce',
        description='water model:',
        disabled=False,
        layout=self.form_item_layout_box)

        self.ansamble = widgets.Dropdown(
                options=['NVE', 'NPT_gamma_ln_0.01', 'NPT_gamma_ln_2', 'NVT_gamma_ln_0.01' ],
                value='NVE',
                description='ansamble:',
                layout=self.form_item_layout_box,
            )
        self.protein = widgets.Dropdown(
                options=['ubq', 'h4'],
                value=self.protein_value,
                description='protein:',
                layout=self.form_item_layout,
                dropdown_color='moccasin',
                align_items='left',
                    border='solid',
                    width='100%'
            )
        
        self.analysis_type = widgets.Dropdown(
                    options=['autocorrelation_NH','autocorrelation_CH3', 'translational diffusion', 'overall thumbling'],
                    value='autocorrelation_NH',
                    description='analysis_type:',
                    layout=Layout(width='99%', grid_area='header'),
                    align_items='center',
                            border='solid',
                            width='99%')
        
    def get_form(self):

        self.form_items = [self.protein, 
                           VBox([self.water_model, self.ansamble])]

        self.form = Box(self.form_items, layout=Layout(
                                        display='flex',
                                        flex_flow='column',
                                        border='solid 2px',
                                        align_items='stretch',
                                        width='50%'
                                    ))
        return self.form
    
    def set_func(self, func):
        self.func = func
    
    def on_value_change(self, change):
        return change['owner'].description.strip(':'), change['new']
    
    def main_change(self, change):
    
        owner_value, new_value = self.on_value_change(change)
        if owner_value == 'protein':
            self.protein_value = new_value
        elif owner_value == 'water model':
            self.water_model_value = new_value
        elif owner_value == 'ansamble':
            self.ansamble_value = new_value
        elif owner_value == 'analysis_type':
            self.analysis_type_value = new_value
        elif owner_value == 'order':
            self.order_exp_value = new_value
        elif owner_value == 'numbers':
            self.numbers_value = new_value

        if self.func:
            self.func()

        
    def observe(self):
        self.water_model.observe(self.main_change, names='value')
        self.ansamble.observe(self.main_change, names='value')
        self.protein.observe(self.main_change, names='value')
        self.analysis_type.observe(self.main_change, names='value')
        self.numbers.observe(self.main_change, names='value')
        self.order_exp.observe(self.main_change, names='value')

class GridBoxFields:
    
    def __init__(self, protein_1, protein_2):
        self.box_fields_1 = BoxFields(protein_1)
        self.box_fields_2 = BoxFields(protein_2)
        
    def set_func(self, func):
        self.func = func
        
    def get_hbox(self):
        self.hbox = HBox([self.box_fields_1.get_form(), self.box_fields_2.get_form()])
        return self.hbox        
        
    def get_gridbox(self):
        header = self.box_fields_1.analysis_type
        main = self.get_hbox()


        gridbox = GridBox(children=[header, main],
                layout=Layout(
                    grid_template_areas='''
                    "header"
                    "main "
                    ''')
               )
        return gridbox
    def observe(self):
        self.box_fields_1.observe()
        self.box_fields_2.observe()

class ImageDisplay:
    def __init__(self, protein_1, protein_2):
        self.gridbox = GridBoxFields(protein_1, protein_2)
        self.order_widget = self.gridbox.box_fields_1.order_exp
        self.numbers_widget = self.gridbox.box_fields_1.numbers
        self.out = Output()
        display(self.out)

    def get_figure_str(self,analysis="autocorrelation_NH", 
                       numbers=1, order=2, box_fields='box_fields_1'):

        handling_dir = os.path.join("D:","bioinf", "handling_stas", "handling")
        
        choice_box = {'box_fields_1': image_display.gridbox.box_fields_1,
                      'box_fields_2': image_display.gridbox.box_fields_2}
#         analysis=choice_box[box_fields].analysis_type_value
        ansamble=choice_box[box_fields].ansamble_value
        water_model=choice_box[box_fields].water_model_value
        protein=choice_box[box_fields].protein_value
        choice_analysis_path = {"autocorrelation_NH": os.path.join(handling_dir, protein, water_model, ansamble,\
                          "autocorr", "NH", "data"),
               "autocorrelation_CH3": os.path.join(handling_dir, protein, water_model, ansamble,\
                                  "autocorr", "CH3", "data"),
               "translational diffusion": os.path.join(handling_dir, protein, water_model, ansamble,\
                          "translational_diffusion","data"),
               "overall thumbling": os.path.join(handling_dir, protein, water_model, ansamble,\
                          "autocorr", "overall_tumbling", "data")}
        data_path =  choice_analysis_path[analysis]
        try:
            path_to_fit = os.path.join(data_path,"fit")
            if analysis == "translational diffusion":
                path_to_msd_fit = os.path.join(path_to_fit, "fit.csv")
                path_to_msd = os.path.join(data_path,"msd.csv")
                fig, ax = plot_msd_for_notebook.get_translation_fit(path_to_msd, path_to_msd_fit)
            elif analysis == "overall thumbling":
                path_to_fit_csv = os.path.join(data_path,"fit", "tau_1_exp.csv")
                if os.path.exists(path_to_fit_csv):
                    path_to_csv_acorr = os.path.join(data_path,"acorr")
                    plot_overall_thumbling_for_notebook.plot_acorr_fit(path_to_fit_csv, path_to_csv_acorr, numbers)
                else:
                    print("Trajectory {protein} {ansamble} {water_model} isn't ready for handling".\
                              format(protein=protein, ansamble=ansamble, water_model=water_model))
            else:
                if analysis == "autocorrelation_CH3":
                    csv_files = sorted(glob.glob(os.path.join(data_path,"acorr", "ca_alignment", "*.csv")))
                else:
                    csv_files = sorted(glob.glob(os.path.join(data_path,"acorr", "*.csv")))
                if numbers > len(csv_files):
                    numbers = len(csv_files) - 1
                path_to_accor = csv_files[numbers]
                fig, ax = plot_for_notebook.get_plot_acorr_fit(path_to_fit, path_to_accor, order, numbers)
            blob = BytesIO()
            plt.savefig(blob,format="png")
            plt.close()
            self.img1_base64 = base64.b64encode(blob.getvalue()).decode("utf-8") 
            return self.img1_base64
        except (IndexError, AssertionError):
            print("Trajectory {protein} {ansamble} {water_model} isn't ready for handling".\
                  format(protein=protein, ansamble=ansamble, water_model=water_model))
        
    
    def show_image(self):
                
        with self.out:
            clear_output(wait=True)

            
            order = self.gridbox.box_fields_1.order_exp_value
            numbers = self.gridbox.box_fields_1.numbers_value
            analysis = self.gridbox.box_fields_1.analysis_type_value
            if analysis == "translational diffusion":
                numbers = 1
            if analysis == "overall thumbling":
                if numbers > 3:
                    numbers = 3

            for ind in range(numbers):
                    display_html("""

                <table style="width:100%">
                  <tr>
                    <th></th>
                    <th></th>
                  </tr>
                  <tr>
                    <td><img src="data:image/png;base64, {img}"></td>
                    <td><img src="data:image/png;base64, {img1}"></td>
                  </tr>
                </table> 

                """.format(img=self.get_figure_str(box_fields='box_fields_1', 
                                                   analysis=analysis,
                                                   numbers=ind, order=order), 
                           img1=self.get_figure_str(box_fields='box_fields_2',
                                                    analysis=analysis,
                                                    numbers=ind, order=order)),
                           raw=True)

image_display = ImageDisplay('ubq', 'h4')
display(image_display.numbers_widget)
display(image_display.order_widget)
display(image_display.gridbox.get_gridbox())
image_display.gridbox.box_fields_1.set_func(image_display.show_image)
image_display.gridbox.box_fields_2.set_func(image_display.show_image)
image_display.gridbox.observe()
