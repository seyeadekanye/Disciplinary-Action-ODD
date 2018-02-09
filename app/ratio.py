# import pandas as pd

def fine_license_ratio(license_data, fine_data, column_name1=None, column_name2=None,year=None):
	"""Get ratio of fines to licenses issued in a given year

	Parameters:
	-----------
	license_data: DataFrame
	    Any subset of the Professional and Occupational Licensing dataframe
	fine_data: DataFrame
    	Any subset of the Disciplinary Actions dataframe
    year: int
    	Year to use to subset your data
	column_name1: Series
    	Column containing years in license_data dataset
	column_name2: Series
    	Column containing years in fine_data dataset

	Returns:
	--------
	tuple
    	A tuple with license percentage as the first entry and fine percentage as the second
    	(year, ratio)
	"""
	
	int(year)
	str(column_name1)
	str(column_name2)

	if year not in license_data[column_name1].unique() or year not in fine_data[column_name2].unique():
		raise Exception(str(year) + " not a valid year for this dataset" + "\n----------------------------------------")
		return "No Data for " + str(year)
	else:
		license_data = license_data[license_data[column_name1]==year]
		fine_data = fine_data[fine_data[column_name2]==year]
	try:
		license_count = len(license_data)
		fine_count = len(fine_data)
		fine_percentage = fine_count/license_count * 100
		license_percentage = 100 - fine_percentage
		return license_percentage, fine_percentage, license_count, fine_count
	except ZeroDivisionError:
		print("Hmmm...It looks like there is are no licenses yet for the year " + str(year))


def profession_fine_license_ratio(license_data, fine_data, profession, profession_column_license, 
	profession_column_fine, column_name1=None, column_name2=None,year=None):
	"""Get ratio of fines to licenses issued in a given year

	Parameters:
	-----------
	license_data: DataFrame
	    Any subset of the Professional and Occupational Licensing dataframe
	fine_data: DataFrame
    	Any subset of the Disciplinary Actions dataframe
	profession: str
    	Profession to get out of your grouped data
	profession_column_license: str
    	Column name of professions in Occupational Licensing dataframe
	profession_column_fine: str
    	Column name of professions in Disciplinary Actions dataframe dataframe
    year: int
    	Year to use to subset your data
	column_name1: Series
    	Column containing years in license_data dataset
	column_name2: Series
    	Column containing years in fine_data dataset

	Returns:
	--------
	tuple
    	A tuple with license percentage as the first entry and fine percentage as the second
    	(license_percentage, fine_percentage)
	"""
	
	int(year)
	str(column_name1)
	str(column_name2)
	str(profession)
	grouped_license_data = license_data.groupby(profession_column_license)
	grouped_fine_data = fine_data.groupby(profession_column_fine)
	license_profession_df = grouped_license_data.get_group(profession)
	fine_profession_df = grouped_fine_data.get_group(profession)

	if year in license_profession_df[column_name1].unique() and year not in fine_profession_df[column_name2].unique():
		return 100, 0
	else: 
		license_ratio, fine_ratio, license_count, fine_count = fine_license_ratio(license_data=license_profession_df, fine_data=fine_profession_df,
			column_name1=column_name1, column_name2=column_name2,year=year)
		return license_ratio, fine_ratio, license_count, fine_count








# license_data = pd.read_pickle('licenses')
# fine_data = pd.read_pickle('fines')

# x,y = profession_fine_license_ratio(license_data=license_data, fine_data=fine_data, 
# profession='Nursing', profession_column_license='profession_id',
# profession_column_fine='profession_id', column_name1='licence_year',
# column_name2='disciplinary_year', year=2017)

# print(x,y)






