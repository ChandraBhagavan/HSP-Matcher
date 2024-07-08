#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 12:37:59 2024

@author: kommuchandravenkatasaibhagavan
"""

from flask import Flask, request, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# Load the data
file_path = '/Users/kommuchandravenkatasaibhagavan/Desktop/HSP.xlsx'
data = pd.read_excel(file_path, sheet_name='Sheet1')

# Function to find matching solvents
def find_matching_solvents(polymer_hsp, solvents_df):
    delta_D1, delta_P1, delta_H1 = polymer_hsp

    def calculate_D(row):
        delta_D2, delta_P2, delta_H2 = row["δD Dispersion"], row["δP Polar"], row["δH Hydrogen bonding"]
        D_squared = 4 * (delta_D2 - delta_D1) ** 2 + (delta_P2 - delta_P1) ** 2 + (delta_H2 - delta_H1) ** 2
        D = D_squared ** 0.5
        return D

    solvents_df["D"] = solvents_df.apply(calculate_D, axis=1)
    solvents_df["Match Quality"] = solvents_df["D"].apply(lambda x: "Reasonable Match" if x < 4 else ("Poor Match" if x > 8 else "Average Match"))
    matching_solvents = solvents_df[["Solvent", "δD Dispersion", "δP Polar", "δH Hydrogen bonding", "D", "Match Quality"]]
    return matching_solvents

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/match', methods=['POST'])
def match():
    delta_D = float(request.form['delta_D'])
    delta_P = float(request.form['delta_P'])
    delta_H = float(request.form['delta_H'])

    polymer_hsp = (delta_D, delta_P, delta_H)
    matching_solvents = find_matching_solvents(polymer_hsp, data)

    return render_template('results.html', tables=[matching_solvents.to_html(classes='data', header="true")])

@app.route('/api/match', methods=['POST'])
def api_match():
    request_data = request.json
    delta_D = float(request_data['delta_D'])
    delta_P = float(request_data['delta_P'])
    delta_H = float(request_data['delta_H'])

    polymer_hsp = (delta_D, delta_P, delta_H)
    matching_solvents = find_matching_solvents(polymer_hsp, data)

    return jsonify(matching_solvents.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)