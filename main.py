from linkedin import linkedin
from indeed import indeed
from angel_list import angel_list


# replace variables here.
SEARCH_TERMS = 'junior developer'
LOCATION = 'USA'
JOB_COUNT = 25
regex = '|'
INCLUDE = ['javascript', 'python']
INCLUDE = str(regex.join(INCLUDE))
EXCLUDE = ['degree', 'years']
EXCLUDE = str(regex.join(EXCLUDE))

class Parameters:
    def __init__(self, search_terms, location, job_count, include, exclude) -> None:
        self.search_terms = SEARCH_TERMS
        self.location = LOCATION
        self.job_count = JOB_COUNT
        self.include = INCLUDE
        self.exclude = EXCLUDE

def run_scrapers():
    linkedin()
    indeed()
    angel_list()

run_scrapers()

if (linkedin_data > 0 and indeed_data > 0 and angel_data > 0):
        job_data = linkedin_data.append(indeed_data, angel_data)
        print('--- merged data below ---')
elif (linkedin_data == 0 and indeed_data > 0 and angel_data > 0):
    job_data = indeed_data.append(angel_data)
    # print(f'using excluded filter only. cannot merge in:{inlen}, ex: {exlen}')
elif (linkedin_data > 0 and indeed_data == 0 and angel_data > 0):
    job_data = linkedin_data.append(angel_data)
    # print(f'using included filter only. cannot merge inc:{inlen}, exc: {exlen}')
elif (linkedin_data > 0 and indeed_data > 0 and angel_data == 0):
    job_data = linkedin_data.append(indeed_data)
    # print(f'using included filter only. cannot merge inc:{inlen}, exc: {exlen}')
else:
    job_data = 0
    print('data not available or no jobs within parameter combo')

job_data.to_csv("jobs.csv", index=False)