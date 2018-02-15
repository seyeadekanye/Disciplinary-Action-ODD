import os
import numpy as np
import pandas as pd
from datetime import datetime


def get_data(save=True):
	try:
		license_data = pd.read_pickle(os.getcwd() + '/data/licenses')
		fine_data = pd.read_pickle(os.getcwd() + '/data/fines')
		return license_data, fine_data
	except IOError:
		url_licenses = "https://data.delaware.gov/resource/dhqa-h9is.csv?$limit=300000"
		url_fines = "https://data.delaware.gov/resource/wqvn-hw3m.csv?$limit=6000"
		license_data = pd.read_csv(url_licenses, low_memory=False)
		fine_data = pd.read_csv(url_fines, low_memory=False)
		disciplinary_start_date = []
		for date in fine_data['disp_start']:
		    try:
		        date = date[0:10]
		        disciplinary_start_date.append(datetime.strptime(str(date),'%Y-%m-%d'))
		    except:
		        disciplinary_start_date.append(date) 
		fine_data['disp_start'] = disciplinary_start_date
		               
		license_issue_date = []
		for date in license_data['issue_date']:
		    try:
		        date = date[0:10]
		        license_issue_date.append(datetime.strptime(str(date),'%Y-%m-%d'))
		    except:
		        license_issue_date.append(date)
		license_data['issue_date'] = license_issue_date

		license_year = []
		for date in data['issue_date']:
			try:
				license_year.append(date.year)
			except error as e:
				license_year.append(date)
		license_data['licence_year'] = license_year

		disciplinary_year = []
		for date in fine_data['disp_start']:
		    try:
		        disciplinary_year.append(date.year)
		    except error as e:
		        disciplinary_year.append(date)
		fine_data['disciplinary_year'] = disciplinary_year
		if save:
			license_data.to_pickle(os.getcwd() + '/data/licenses')
			fine_data.to_pickle(os.getcwd() + '/data/fines')
			return license_data, fine_data
		else:
			return license_data, fine_data


def generate_dates_list(A,B):
	license_date_options_list = sorted([year for year in A['licence_year'].unique() if not np.isnan(year)])
	fines_date_options_list = sorted([year for year in B['disciplinary_year'].unique() if not np.isnan(year)])
	C = license_date_options_list
	D = fines_date_options_list
	dates_intersect = sorted(list(set(C).intersection(set(D))))
	dates_intersect_list = []
	for date in dates_intersect:
	   dates_intersect_list.append({'label': date, 'value': date})
	return dates_intersect_list


def generate_professions_list(A,B):
	A = A['profession_id'].unique()
	B = B['profession_id'].unique()
	professions = sorted(list(set(A).intersection(set(B))))
	professions_options = []
	for profession in professions:
	   professions_options.append({'label': profession, 'value': profession})
	num = np.random.randint(0,len(professions_options))
	return professions_options, num

