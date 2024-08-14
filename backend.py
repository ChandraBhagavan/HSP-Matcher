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

    solvents_df["Distance"] = solvents_df.apply(calculate_D, axis=1)
    
    # Filter for reasonable and average matches
    reasonable_matches = solvents_df[solvents_df["Distance"] < 4]
    average_matches = solvents_df[(solvents_df["Distance"] >= 4) & (solvents_df["Distance"] <= 8)]
    
    return reasonable_matches, average_matches

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/match', methods=['POST'])
def match():
    compound_name = request.form.get('compound_name', 'Unknown Compound')
    delta_D = float(request.form['delta_D'])
    delta_P = float(request.form['delta_P'])
    delta_H = float(request.form['delta_H'])

    polymer_hsp = (delta_D, delta_P, delta_H)
    reasonable_matches, average_matches = find_matching_solvents(polymer_hsp, data)

    return render_template('results.html', compound_name=compound_name,
                           reasonable_matches=reasonable_matches.to_html(classes='table table-striped', header="true"),
                           average_matches=average_matches.to_html(classes='table table-striped', header="true"))

if __name__ == '__main__':
    app.run(debug=True)
