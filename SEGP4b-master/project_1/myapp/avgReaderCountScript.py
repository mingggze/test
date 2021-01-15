from mendeley import Mendeley
from datetime import datetime #current date and time
from bs4 import BeautifulSoup
import requests

def all_subset(query):
    from itertools import combinations
    subset = []
    if len(query) > 2 and len(query) < 3:
        for i in set(combinations(query, r=2)):
            subset.append(i)
        for i in set(combinations(query, r=1)):
            subset.append(i)
    elif len(query) < 2:
        for i in set(combinations(query, r=1)):
            subset.append(i)
    else:
        for i in set(combinations(query, r=1)):
            subset.append(i)
    return subset

def avgRCSList(queryList):
    client_id = "8910"
    client_secret = "OxP464bB5roU81GH"
    avgRCS =0
    curryear = datetime.now().year #get the current year
    mendeley = Mendeley(client_id=client_id, client_secret=client_secret)
    resultList = []

    auth = mendeley.start_client_credentials_flow()
    session = auth.authenticate()
    queryList_subset = all_subset(queryList)
    for query in queryList_subset:
        x = 0
        iterCount = 0
        paperCount = 0
        avgRCS = 0
        avgyear = 0
        pages = session.catalog.advanced_search(source=query, view="stats")

        for page in pages.iter(page_size=100):
            if iterCount == 1000:
                break
            if curryear - page.year <= 0:
                x += 0
            else:
                x += page.reader_count / (curryear - page.year)
                paperCount += 1
            iterCount += 1
            avgyear += page.year #calculate average year of publications

        avgyear = avgyear / iterCount
        avgRCS = round((x / paperCount),2)
        resultList.append(avgRCS)
        print(str(query) + ": " + str(avgRCS) + " | published: " + str(paperCount) + " | avgyear: " + str(round(avgyear)))

        results = {
           
            'subset':queryList_subset,
            'marks':resultList,
            'zipped':zip(queryList_subset,resultList),
        }

    return results
    
def categoryscraper(cat):
    
    """
    
    category={
        "Business, Economic & Management":"bus",
        "Chemical & Material Sciences":"chm",
        "Engineering & Computer Science":"eng",
        "Health & Medical Sciences":"med",
        "Humanities, Literature & Arts":"hum",
        "Life Sciences & Earth Sciences":"bio",
        "Physics & Mathematics":"phy",
        "Social Sciences":"soc"
        }

    i=0

    keys = list(category.keys())
    while(i<8):
        print(str(i+1)+": "+keys[i])
        i=i+1
"""
    temp=cat


    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    url="https://scholar.google.com/citations?view_op=top_venues&hl=en&vq="+temp #scholar url and temp is the url code for the category


    response = requests.get(url,headers=headers)#must have header to not get blocked

    soup=BeautifulSoup(response.content,'lxml')
    print(url)

    printing=False #trigger so it doesnt print menu title, (sign in, and "subcategories"

    categoriesarr= []
    #filter out tags to get number of citations and title
    for item in soup.select('a.gs_md_li',{"tabindex":"-1"}): #item is string of subcategory, parameters are tags of wanted fields(as can be seen in inspect element)
        try:
            item=item.text
            if (printing):
                categoriesarr.append(item)
            if "Subcategories" in item: #start printing data aftrer subcategories field
                printing=True
            
        except Exception as e:
            #raise e
            print('')
           
    """   
    
        catresult = {
            'array':categoriesarr
        }
    """
   
    
    return categoriesarr
    
    

