# football-league

Get results from leagues and input in MongoDB Collection

## how to use

Edit the file [config/leagues.py](config/leagues.py) and add your leagues.

```python
championships = {
    'url': 'https:////www.football-data.co.uk',
    'leagues': [{
        'uri': '/mmz4281',
        'start': [21,22],
        'division': 2,
        'countries': [{
            'country': 'England',
            'file': 'E#.csv',
            'league': ['Premier','European']
        }]
    },
    {
        'uri': '/new',
        'countries': [{
            'country':'Brazil',
            'file': 'BRA.csv',
            'league': ['Secondary'],
            'header': {
                'to': ['Liga','Data','Mandante','Visitante','GolsMandante','GolsVisitante','Resultado','OddsMandante','OddsEmpate','OddsVisitante'],
                'from': ['Country','Date','Home','Away','HG','AG','Res','PH','PD','PA']
            }
        }]
    }]
}
```

## run

`docker compose up --build --detach`

After start access http://localhost:8081 to see database.