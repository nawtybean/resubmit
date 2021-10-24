from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from sqlalchemy.pool import NullPool
import pandas as pd
import sqlalchemy
from sklearn import metrics


def home(request):
    context = {}
    return render(request, 'home.html', context)


class SubmitView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        engine = sqlalchemy.create_engine(
            "mssql+pyodbc://julesd:Password1@akmtntest.database.windows.net/akmtntest?DRIVER={ODBC Driver 17 for SQL Server}",
            echo=True, poolclass=NullPool)

        print('Line 25')
        data = request.data
        print(data)

        name = data["name"]
        email = data["email"]
        x = data["x"]

        x_df = pd.DataFrame(columns=['imei', 'pred'])

        imei = list(x.keys())
        pred = list(x.values())
        x_df['imei'] = imei
        x_df['pred'] = pred
        x_df['pred'] = x_df['pred'].astype('int')
        # x_df['imei'] = x_df['imei'].astype('int64')
        x_df.index = x_df['imei']
        x_df.drop('imei', axis=1, inplace=True)
        x_df

        print('x_df created')

        y = pd.read_sql_query('SELECT * FROM answer', con=engine)
        y['status'] = y['status'].astype('int')
        print('past read_sql_query')

        print('con closed')

        y.index = y['imei']
        y.drop('imei', axis=1, inplace=True)

        result = pd.concat([x_df, y], axis=1)
        print(result.head())
        print('18:43')

        score = metrics.f1_score(result['pred'], result['status'])
        print(score)

        submissions = pd.read_sql('SELECT * FROM Submissions', con=engine)
        submissions = submissions.append(
            {'ID': max(submissions['ID'] + 1), 'Name': name, 'email': email, 'score': score}, ignore_index=True)
        print('appended')

        submissions.to_sql('submissions', if_exists='replace', con=engine, index=False)

        print('complete')
        result = {'message': f'F1 Score: {score * 100}%'}
        engine.dispose()
        return Response(result)


class ScoresView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        engine = sqlalchemy.create_engine(
            "mssql+pyodbc://julesd:Password1@akmtntest.database.windows.net/akmtntest?DRIVER={ODBC Driver 17 for SQL Server}",
            echo=True)

        query = 'SELECT * FROM Submissions'

        results = pd.read_sql_query(query, con=engine)
        results = results.to_dict()

        result = {'message': results}
        engine.dispose()
        return Response(result)
