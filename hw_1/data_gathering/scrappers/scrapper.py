import logging
import requests
from .exceptions import DdeliveryAPIError
import json

logger = logging.getLogger(__name__)


class DdeliveryAPI(object):

    def __init__(self, request_timeout=20):
        """
        :param api_key: токен личного кабинета
        :param endpoint: url адрес API
        :param request_timeout: таймаут запросов к API
        """

        # DDelivery information.
        DDELIVERY_ENDPOINT = 'https://ddelivery.ru/api/'
        DDELIVERY_API_KEY = 'ktvdxoflx3jspy8j9mw9fene_hsbtmkx'

        self._api_key = DDELIVERY_API_KEY
        self._endpoint = DDELIVERY_ENDPOINT + self._api_key + '/'
        self.request_timeout = request_timeout

    def _request(self, api_method, request_method='get', params=None, data=None):
        """
        Make request.

        Example request:
            https://ddelivery.ru/api/<api_token>/<api_method>

        :param api_method:
        :param request_method:
        :param params:
        :param data:
        :return:
        """

        common_data = dict(
            method=api_method,
            token=self._api_key
        )

        if request_method == 'get':
            params = params or {}
            params.update(common_data)
        elif request_method == 'post':
            data = data or {}
            data.update(common_data)
        else:
            logger.error('DdeliveryAPI._request: Unknown request method "{}"'.format(request_method))
            raise ValueError('Unknown request method "{}"'.format(request_method))

        request_method = getattr(requests, request_method)

        try:
            url = self._endpoint + common_data["method"]

            logger.debug('REQUEST:\n\turl: {url}\n\tparams: {params}\n\tdata: {data}'.format(
                url=url,
                params=params,
                data=data
            ))
            # response = request_method(url, params=params, data=data, timeout=self.request_timeout)
            response = request_method(url, params=params, json=data, timeout=self.request_timeout)
            logger.debug('RESPONSE:\n\tstatus: {status}'.format(
                status=response.status_code,
            ))
        except requests.RequestException as e:
            logger.exception(e)
            raise DdeliveryAPIError('Http error: %s', e)

        try:
            js = json.loads(response.content.decode())
        except (TypeError, ValueError) as exc:
            logger.exception(exc)
            raise DdeliveryAPIError('Invalid response, bb down? %s', response.content[:100])

        # self._raise_exception_if_error(js_data=js)

        return js

    @staticmethod
    def _raise_exception_if_error(js_data):
        if js_data["status"] != 'ok':
            raise DdeliveryAPIError(js_data)

    def get_delivery_points(self,city_to=None):
        """
        Получение списка ПВЗ (пунктов самовывоза)

        Пример ответа:

        <code>
        [
          {
            "id": 151185,
            "name": "Невинномысск",
            "longitude": "41.946725",
            "latitude": "44.624142",
            "city_id": 123,
            "city_name": "Невинномысск",
            "delivery_company_id": 4,
            "delivery_company_name": "Boxberry",
            "type": 2,
            "description_in": "Войти в Торговый центр через первый вход",
            "description_out": "Возле остановки",
            "address": "357100, г. Невинномысск, ул. Гагарина, д. 72",
            "schedule": "пн-пт:10.00-18.00 сб:10.00-18.00",
            "is_fitting": 0,
            "is_cash": 1,
            "is_card": 0
          }
        ]
        </code>

        Получение списка ПВЗ (пунктов самовывоза)

        :param api_key - АПИ ключ интернет магазина. Обязательное поле.
        :param city_to - Город назначения. ID из справочника «Населённые пункты».

        Пример значений параметра

        <code>
        [
          {
            "id": 151184,
            "name": "г. Москва"
          },
          {
            "id": 151185,
            "name": "г. Санкт-Петербург"
          },
          {
            "id": 54,
            "name": "г. Казань, Респ. Татарстан"
          },
          {
            "id": 282,
            "name": "г. Нижний Новгород, Нижегородская обл."
          },
          {
            "id": 293,
            "name": "г. Новосибирск, Новосибирская обл."
          },
          {
            "id": 296,
            "name": "г. Омск, Омская обл."
          },
          {
            "id": 331,
            "name": "г. Ростов-на-Дону, Ростовская обл."
          },
          {
            "id": 345,
            "name": "г. Самара, Самарская обл."
          },
          {
            "id": 375,
            "name": "г. Екатеринбург, Свердловская обл."
          },
          {
            "id": 434,
            "name": "г. Челябинск, Челябинская обл."
          }
        ]

        </code>

        :param side1 - Габариты (Высота / см) Не обязательное поле.
        :param side2 - Габариты (Ширина / см) Не обязательное поле.
        :param side3 - Габариты (Длина / см) Не обязательное поле.
        """
        params = {
            "city_to": 151184,
        }

        return self._request('list/delivery-point.json', params=params)


class Scrapper(object):
    def __init__(self):
        ddelivery_client = DdeliveryAPI()
        self.ddelivery_api_client = ddelivery_client

    def scrap_process(self, storage):
        try:
            data = self.ddelivery_api_client.get_delivery_points()
        except DdeliveryAPIError as box_ex:
            logger.error('in DdeliverySetViewSet(cost_check): System error: {}'.format(box_ex))
            logger.exception(box_ex)
            raise
        except Exception as exc:
            logger.error('in DdeliverySetViewSet(create): System error: {}'.format(exc))
            logger.exception(exc)
            raise

        # save scrapped objects here
        storage.write_data(data)
