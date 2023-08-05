import dill
import json
import numpy as np
import requests
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from kyqlos.utils import args_type_check


class DataMonitorClient(object):
    """
    | このクラスはKyqlosサーバーにリクエストを送信するためのAPIを提供する。
    | APIの利用はKyqlos GUI Clientでアカウント登録済であることを前提とする。
    | アカウント登録後に発行されるcredentialsファイルを指定してアカウント認証を行う。
    |
    | 各メソッドの引数"thread"は、Trueが指定されるとスレッドによる非同期処理を行い、
    | 戻り値としてfeature（concurrent.futures.Future object）を返す。
    | feature.result()によりメインプロセスと同期、実行結果の取得が行われる。

    Args:
        credentials(str): credentialsファイルのパス。\
            credentialsファイルとはKyqlosサーバーのアカウント認証に必要な情報が記載されたjson形式ファイル。\
            アカウント登録後に発行される。
    """

    def __init__(self, credentials):
        self._verify_credentials(credentials)
        self.registered = False
        self.base_url = f"http://{self.host}:30000/api/{self.api_version}/data-monitoring"
        self.registration_url = self.base_url+"/monitor"
        self.dev_data_registration_url = self.base_url+"/dev-data"
        self.prod_data_registration_url = self.base_url+"/prod-data"
        self.calculate_url = self.base_url+"/calculate-metric"
        self.dev_data_id = None
        self.prod_data_ids = []
        self.thread = ThreadPoolExecutor(max_workers=1)
        self.MAX_FEATURE_SIZE = np.prod((3, 300, 300))

    def _verify_credentials(self, credential_path):
        with open(credential_path, "r") as json_file:
            credentials = json.load(json_file)
        self.host = credentials["host"]
        self.api_version = credentials["api_version"]
        self.token = credentials["credential"]

    def _register_data_monitoring(self, data_shape):
        data_shape = [int(i) for i in data_shape]
        response = requests.post(
            self.registration_url,
            headers={
                "auth": self.token
            },
            data={
                "data_shape": json.dumps(data_shape)
            }
        )
        if response.status_code == requests.codes.ok:
            data_monitoring_id = json.loads(response.content)[
                "data_monitoring_id"]
        else:
            raise Exception(
                f"Server Error: {response.content}")
        return data_monitoring_id

    def _register_development_data(self, data_monitoring_id, data):
        data_byte_str = dill.dumps(data)
        response = requests.post(
            self.dev_data_registration_url,
            headers={
                "auth": self.token
            },
            params={
                "data_monitoring_id": data_monitoring_id
            },
            files={
                "data": data_byte_str
            }
        )
        if response.status_code == requests.codes.ok:
            self.dev_data_id = json.loads(response.content)["dev_data_id"]
        else:
            raise Exception(
                f"Server Error: {response.content}")

    def _register_production_data(self, data_monitoring_id, data, latency=0.0):
        data_byte_str = dill.dumps(data)
        response = requests.post(
            self.prod_data_registration_url,
            headers={
                "auth": self.token
            },
            params={
                "data_monitoring_id": data_monitoring_id
            },
            files={
                "data": data_byte_str
            },
            data={
                "latency": latency
            }
        )
        if response.status_code == requests.codes.ok:
            self.prod_data_ids.append(json.loads(
                response.content)["prod_data_id"])
        else:
            raise Exception(
                f"Server Error: {response.content}")

    def _calculate_metric(self, data_monitoring_id, metric_name, run_async=True):
        response = requests.post(
            self.calculate_url,
            headers={
                "auth": self.token
            },
            params={
                "data_monitoring_id": data_monitoring_id
            },
            data={
                "prod_data_id": self.prod_data_ids[-1],
                "metric_name": metric_name
            }
        )
        if response.status_code == requests.codes.ok:
            response = json.loads(response.content)
            if run_async:
                return response["metric_calculation_id"]
            else:
                calc_status = None
                while calc_status != "finished":
                    calc_status = self._retrieve_metric(
                        data_monitoring_id, response["metric_calculation_id"], include_status=True)["status"]
                    if calc_status == "failed":
                        raise Exception(
                            "Error occured while calculating metric")
                    sleep(2)
                return self._retrieve_metric(
                    data_monitoring_id, response["metric_calculation_id"], include_status=True)["result"]
        else:
            raise Exception(
                f"Server Error: {response.content}")

    def _retrieve_metric(self, data_monitoring_id, metric_calculation_id, include_status=False):
        response = requests.get(
            self.calculate_url,
            headers={
                "auth": self.token
            },
            params={
                "data_monitoring_id": data_monitoring_id,
                "metric_calculation_id": metric_calculation_id
            }
        )
        if response.status_code == requests.codes.ok:
            response = json.loads(response.content)
            if include_status:
                return {"status": response["job_status"], "result": response["result"]}
            else:
                return response["result"]
        else:
            raise Exception(
                f"Server Error: {response.content}")

    def _select_process(self, thread, func, *args):
        if thread:
            future = self.thread.submit(
                func, *args)
            return future
        else:
            result = func(*args)
            return result

    def _check_axis_num(self, shape, th):
        if len(shape) < th:
            raise Exception(
                f'Axis of {shape} is too short.'
                f'The supported shape is (data_size, feature1_size, feature2_size, ..).')

    def _check_data_size(self, data_size, th):
        if data_size > th:
            raise Exception(
                f'The data size {data_size} is too long. Max size is {th}.')

    def _check_feature_size(self, shape):
        if np.prod(shape[1:]) > self.MAX_FEATURE_SIZE:
            raise Exception(
                f'The feature size {np.prod(shape[1:])} is too long. Max size is {self.MAX_FEATURE_SIZE}.')

    @ args_type_check
    def register_data_monitoring(self, data_shape: tuple, thread: bool = False):
        """
        | 新規データ監視の登録、データモニタリングID発行のリクエストを送信

        Args:
            data_shape(tuple): 登録する学習データのshape
            thread(bool): スレッドによる非同期処理
        Returns:
            データモニタリングID
        """
        self._check_axis_num(data_shape, th=2)
        self._check_data_size(data_shape[0], th=1)
        self._check_feature_size(data_shape)
        return self._select_process(thread, self._register_data_monitoring, data_shape)

    @ args_type_check
    def register_development_data(self, data_monitoring_id: str, data: np.ndarray, thread: bool = False):
        """
        学習データ登録リクエストを送信

        Args:
            data_monitoring_id(str): データモニタリングID
            data(numpy.ndarray): 学習データ時のデータ
            thread(bool): スレッドによる非同期処理
        """
        self._check_axis_num(data.shape, th=2)
        self._check_feature_size(data.shape)
        return self._select_process(thread, self._register_development_data, data_monitoring_id, data)

    @ args_type_check
    def register_production_data(
            self, data_monitoring_id: str, data: np.ndarray, latency: float = 0.0, thread: bool = False):
        """
        運用データ登録リクエストを送信

        Args:
            data_monitoring_id(str): データモニタリングID
            data(numpy.ndarray): 運用データ時のデータ
            latency(float): モデル推論時のレイテンシ
            thread(bool): スレッドによる非同期処理
        """
        self._check_axis_num(data.shape, th=2)
        self._check_data_size(data.shape[0], th=1)
        self._check_feature_size(data.shape)
        return self._select_process(thread, self._register_production_data, data_monitoring_id, data, latency)

    @ args_type_check
    def calculate_metric(self, data_monitoring_id: str, metric_name: str, run_async: bool = True, thread: bool = False):
        """
        データ変化メトリックの計算リクエストを送信

        Args:
            data_monitoring_id(str): データモニタリングID
            metric_name(str): データ変化メトリックの種類
            run_async(bool): Trueの場合はサーバーの計算終了を待たずにメトリック計算IDを返す。\
                Falseの場合はサーバーの計算終了まで待機して計算結果を返す。
            thread(bool): スレッドによる非同期処理
        Returns:
            メトリック計算ID、またはデータ変化メトリックの計算結果
        """
        return self._select_process(thread, self._calculate_metric, data_monitoring_id, metric_name, run_async)

    @ args_type_check
    def retrieve_metric(
            self, data_monitoring_id: str, metric_calculation_id: str,
            include_status: bool = False, thread: bool = False):
        """
        データ変化メトリックの計算結果取得リクエストを送信

        Args:
            data_monitoring_id(str): データモニタリングID
            metric_calculation_id(str): メトリック計算ID
            include_status(bool): 戻り値にJobステイタスを含める
            thread(bool): スレッドによる非同期処理
        Returns:
            データ変化メトリックの計算結果
        """
        return self._select_process(
            thread, self._retrieve_metric, data_monitoring_id, metric_calculation_id, include_status)
