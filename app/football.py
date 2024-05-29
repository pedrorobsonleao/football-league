import os
import pymongo
import datetime
import pandas as pd

from config import leagues 

year = int(datetime.datetime.now().strftime('%y'))
header = {
    'to':['Data','Mandante','Visitante','GolsMandante','GolsVisitante','Resultado','OddsMandante','OddsEmpate','OddsVisitante'],
    'from':['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','B365H','B365D','B365A']
}

def periods(s):
    r = []

    while s[1] < year-1:
        r.append(f'{s[0]}{s[1]}')
        s[0]+=1
        s[1]+=1

    return r

def makeUrls(c):
    urls = []

    for l in c['leagues']:
        url = f'{c["url"]}{l["uri"]}'

        try:
            ps = periods(l['start'])
        except KeyError:
            ps = ['']

        for p in ps:
            d = 0

            try:
                dv = l['division']
            except KeyError:
                dv = 1

            while d < dv:
                for ct in l['countries']:
                    f = ct['file'].replace('#', str(d))
                    ct['url'] = f'{url}/{p}/{f}'.replace('//','/')
                    urls.append(ct)

                d+=1
    return urls

def getData(c):
    try:
        df = pd.read_csv(c['url'])
    except Exception as e:
        print({
            'config': c,
            'exception': e
        })

    try:
        df = df[c['header']['from']]
    except KeyError:
        df = df[header['from']]

    try:
        df.columns = c['header']['to']
    except KeyError:
        df.columns = header['to']

    df["Data"] = pd.to_datetime(df.Data, dayfirst=True)

    try:
        df['LigaParticipante'] = [c['league']] * len(df)
    except KeyError:
        True

    try:
        df['Pais'] = [c['country']] * len(df)
    except KeyError:
        True

    df.reset_index(inplace=True)
    return df.to_dict("records")

def main():
    urls = makeUrls(leagues.championships)

    collection = None
    
    try:
        conn = pymongo.MongoClient(os.environ['MONGODB_URL'])
        db = conn['football']
        collection = db['soccer']
    except KeyError as ke:
        print(f'Can\'t found {ke} environment variable!')
    except Exception as e:
        raise(e)

    for url in urls:
        data = getData(url)

        if collection == None:
            print(data)
        else:
            collection.insert_many(data)

if __name__ == '__main__':
    main()
