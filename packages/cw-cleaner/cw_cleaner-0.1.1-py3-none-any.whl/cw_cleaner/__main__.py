import boto3
from datetime import datetime, timedelta
import time
import fire
from tabulate import tabulate

client = boto3.client('logs')

headers = ["creationTime", "logGroupName", "retentionInDays", "streams"]
limit = 50


def sortByFunc(type):
    def sortFunc(v):
        return v[headers.index(type)]
    return sortFunc


def timestamp_to_date(timestamp):
    epoch_time = str(timestamp)[0: 10]
    return datetime.fromtimestamp(float(epoch_time)).strftime('%m/%d/%Y - %H:%M:%S')


class CW_logs:
    def __init__(self, client):
        self.client = client


class CW_log_groups(CW_logs):

    def describe_log_groups(self, limit=limit, logGroupNamePrefix='/'):
        data = []
        response = self.client.describe_log_groups(
            limit=limit,
            logGroupNamePrefix=logGroupNamePrefix
        )
        next_token = False
        data = response["logGroups"]
        if "nextToken" in response:
            next_token = response["nextToken"]
        while next_token:
            response = self.client.describe_log_groups(
                limit=limit,
                nextToken=next_token,
                logGroupNamePrefix=logGroupNamePrefix
            )
            if "nextToken" in response:
                next_token = response["nextToken"]
            else:
                next_token = False
            data = data + response["logGroups"]

        return data

    def describe_log_groups_with_streams(self, limit=limit, logGroupNamePrefix='/'):
        data = self.describe_log_groups(
            logGroupNamePrefix=logGroupNamePrefix, limit=limit)

        for logGroup in data:
            logGroup["streams"] = self.get_streams(
                logGroupName=logGroup["logGroupName"])

        return data

    def list(self, limit=limit, logGroupNamePrefix='/'):
        data = self.describe_log_groups(
            logGroupNamePrefix=logGroupNamePrefix, limit=limit)

        return list(map(lambda x: x["logGroupName"], data))

    def get_streams(self, limit=limit, logGroupName=None, orderBy='LastEventTime', descending=True):
        response = self.client.describe_log_streams(
            logGroupName=logGroupName,
            orderBy=orderBy,
            descending=descending,
            limit=limit
        )
        return response["logStreams"]

    def delete_log_group(self, logGroupName):
        response = self.client.delete_log_group(
            logGroupName=logGroupName
        )
        return response

    def delete_log_stream(self, logGroupName, logStreamName):
        response = client.delete_log_stream(
            logGroupName=logGroupName,
            logStreamName=logStreamName
        )
        return response

    def put_retention(self, logGroupName, retentionInDays=30):
        response = self.client.put_retention_policy(
            logGroupName=logGroupName,
            retentionInDays=retentionInDays
        )
        return response

    def table(self, sortBy="creationTime", reverse=True, logGroupNamePrefix="/", limit=limit):
        data = self.describe_log_groups_with_streams(
            logGroupNamePrefix=logGroupNamePrefix, limit=limit)
        tableRows = [[timestamp_to_date(log["creationTime"]), log["logGroupName"],
                      log["retentionInDays"] if "retentionInDays" in log else "Never expire", len(log["streams"])] for log in data]
        tableRows.sort(reverse=reverse, key=sortByFunc(sortBy))
        return tabulate(tableRows, headers=headers)

    def filter(self, field, value, logGroupNamePrefix="/", limit=limit):
        data = self.describe_log_groups_with_streams(
            logGroupNamePrefix=logGroupNamePrefix, limit=limit)

        return list(map(lambda x: x["logGroupName"], filter(lambda x: True if field in x and x[field] == value else False, data)))

    def query(self, logGroupName, query="fields @timestamp, @message", startTime=int((datetime.today() - timedelta(days=14)).timestamp()), endTime=int(datetime.now().timestamp())):
        start_query_response = client.start_query(
            logGroupName=logGroupName,
            startTime=startTime,
            endTime=endTime,
            queryString=query,
        )

        response = None

        while response == None or response['status'] == 'Running':
            print('Waiting for query to complete ...')
            time.sleep(1)
            response = client.get_query_results(
                queryId=start_query_response['queryId']
            )
        table_headers = [log["field"]
                         for log in response["results"][0]]
        tableRows = [[v["value"][:50] for v in log]
                     for log in response["results"]]

        return tabulate(tableRows, headers=table_headers)


cw = CW_log_groups(client)


def main():
    fire.Fire(cw)


if __name__ == '__main__':
    fire.Fire(cw)
